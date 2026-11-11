"""Confere e corrige as coordenadas dos pronto-atendimentos do CNES.

Para cada unidade:
  1. Bairros esperados: o bairro do endereço no CNES e o bairro que aparece no nome da unidade
     (ex.: "UPA Cristo Redentor"), ambos procurados na malha de bairros do IBGE (Censo 2022).
     Onde a malha não tem bairros, usa subdistritos (Brasília, Goiânia) ou distritos (São Paulo).
  2. Classificação pela menor distância da coordenada a um bairro esperado: ok (dentro), perto (até 1,5 km),
     suspeita (mais longe), fora_do_municipio, ou sem_area_esperada (nenhum bairro esperado na malha).
     Também marca coordenada_compartilhada: unidades de bairros diferentes a menos de 100 m uma da outra
     (sinal de coordenada genérica, como a sede da secretaria ou o centro da cidade).
  3. Para suspeita, fora_do_municipio, coordenada_compartilhada e sem_area_esperada, busca no Nominatim
     (OpenStreetMap) pelo endereço, pelo CEP e pelo nome da unidade:
       - resultado a até 500 m da coordenada original (1 km em sem_area_esperada) -> original confirmada;
       - resultado no município e perto de um bairro esperado -> usa o resultado;
       - erro grosseiro (compartilhada, fora do município ou a mais de 5 km do bairro) sem resultado aceito
         -> ponto dentro do bairro esperado, marcado como aproximado;
       - senão -> mantém a original e marca para revisão manual.
  4. Correções manuais em dados/correcoes_manuais.csv (CO_CNES, lat, lon, nota) têm a palavra final.

Uso: .venv/bin/python scripts/07_conferir_coordenadas.py
Saídas:
  dados/processados/conferencia_coordenadas.csv  (diagnóstico de cada unidade)
  dados/processados/pa_capitais_corrigido.csv    (mesmas colunas de pa_capitais.csv, com lat/lon corrigidas)
"""
import json
import re
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

import geopandas as gpd
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "dados/processados"
GPKG_DIR = ROOT / "dados/ibge/setores_gpkg"
CACHE = PROC / "geocodificacao_cache.json"
MANUAIS = ROOT / "dados/correcoes_manuais.csv"

LIMITE_PERTO_M = 1500
LIMITE_FORA_M = 200
LIMITE_CONFIRMA_M = 500
LIMITE_COMPARTILHADA_M = 100
LIMITE_GROSSEIRO_M = 5000
BAIRROS_GENERICOS = {frozenset({"CENTRO"})}  # aparecem em nomes de unidade sem indicar o bairro
NOMINATIM = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "ciencia-de-cidades-trabalho-academico/1.0"

ABREVIACOES = {"CONJ": "CONJUNTO", "JD": "JARDIM", "JARD": "JARDIM", "PQ": "PARQUE", "VL": "VILA",
               "STA": "SANTA", "STO": "SANTO", "N": "NOSSA", "SRA": "SENHORA", "RES": "RESIDENCIAL",
               "NUC": "NUCLEO", "HAB": "HABITACIONAL", "SETOR": "SETOR", "CJ": "CONJUNTO", "LUIZ": "LUIS"}
IGNORAR = {"I", "II", "III", "IV", "V", "BAIRRO", "DE", "DA", "DO", "DOS", "DAS", "E"}


def tokens(nome):
    if not isinstance(nome, str):
        return frozenset()
    s = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode().upper()
    s = re.sub(r"[^A-Z0-9 ]", " ", s)
    return frozenset(ABREVIACOES.get(t, t) for t in s.split() if t not in IGNORAR)


def mesmo_bairro(a, b):
    ta, tb = tokens(a), tokens(b)
    return bool(ta) and bool(tb) and (ta <= tb or tb <= ta)


def geocodificar(endereco, cache):
    """Consulta o Nominatim (1 requisição por segundo, com cache em disco)."""
    chave = json.dumps(endereco, sort_keys=True, ensure_ascii=False)
    if chave in cache:
        return cache[chave]
    url = NOMINATIM + "?" + urllib.parse.urlencode({**endereco, "format": "jsonv2", "limit": 1})
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    time.sleep(1.1)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            res = json.load(r)
        cache[chave] = [float(res[0]["lat"]), float(res[0]["lon"])] if res else None
    except Exception as e:  # rede fora do ar: não grava no cache para tentar de novo depois
        print(f"  falha no Nominatim: {e}")
        return None
    return cache[chave]


def conferir_capital(capital, cd_mun, pa, cache):
    uf = capital.split(" - ")[1]
    gpkg = GPKG_DIR / f"{uf}_setores_CD2022.gpkg"
    s = gpd.read_file(gpkg, where=f"CD_MUN='{cd_mun}'", columns=["CD_SETOR", "NM_BAIRRO", "NM_SUBDIST", "NM_DIST"])
    crs_m = s.estimate_utm_crs()
    s = s.to_crs(crs_m)
    municipio = s.union_all()
    # Sem bairros na malha (São Paulo, Brasília, Goiânia...), usa a divisão interna que existir
    camada = next((c for c in ["NM_BAIRRO", "NM_SUBDIST", "NM_DIST"] if s[c].nunique() > 1), None)
    if camada is None:
        bairros = gpd.GeoDataFrame({"NM_BAIRRO": []}, geometry=[], crs=crs_m)
    else:
        bairros = (s.loc[s[camada].notna(), [camada, "geometry"]].dissolve(camada).reset_index()
                   .rename(columns={camada: "NM_BAIRRO"}))
    cidade, estado = capital.split(" - ")

    bairros["tokens"] = [tokens(b) for b in bairros.NM_BAIRRO]

    pontos = gpd.GeoSeries(gpd.points_from_xy(pa.lon, pa.lat), crs="EPSG:4326", index=pa.index).to_crs(crs_m)
    compartilhada = {
        i for i in pa.index for j in pa.index
        if i != j and pontos[i].distance(pontos[j]) < LIMITE_COMPARTILHADA_M
        and not mesmo_bairro(pa.at[i, "NO_BAIRRO"], pa.at[j, "NO_BAIRRO"])
    }

    linhas = []
    for i, u in pa.iterrows():
        p = pontos[i]
        contem = bairros[bairros.contains(p)]
        bairro_coord = contem.NM_BAIRRO.iloc[0] if len(contem) else None
        nome = tokens(u.NO_FANTASIA)
        do_endereco = pd.Series([mesmo_bairro(b, u.NO_BAIRRO) for b in bairros.NM_BAIRRO],
                                index=bairros.index, dtype=bool)
        do_nome = pd.Series([bool(t) and t <= nome and t not in BAIRROS_GENERICOS for t in bairros.tokens],
                            index=bairros.index, dtype=bool)
        alvo = bairros[do_endereco | do_nome]
        bairro_nome = ", ".join(bairros.NM_BAIRRO[do_nome]) or None
        dist_bairro = alvo.distance(p).min() if len(alvo) else None
        fora = municipio.distance(p)

        if fora > LIMITE_FORA_M:
            status = "fora_do_municipio"
        elif i in compartilhada:
            status = "coordenada_compartilhada"
        elif dist_bairro is None:
            status = "sem_area_esperada"
        elif dist_bairro == 0:
            status = "ok"
        elif dist_bairro <= LIMITE_PERTO_M:
            status = "perto"
        else:
            status = "suspeita"

        lat, lon, metodo = u.lat, u.lon, "original"
        if status in {"suspeita", "fora_do_municipio", "coordenada_compartilhada", "sem_area_esperada"}:
            # Sem área esperada, o endereço é a única referência: confirma com tolerância maior
            tolerancia = LIMITE_CONFIRMA_M if status != "sem_area_esperada" else 2 * LIMITE_CONFIRMA_M
            pode_confirmar = status in {"suspeita", "sem_area_esperada"}  # nos outros, a original já é errada
            metodo = "revisar_manual"
            numero = "" if str(u.NU_ENDERECO).upper() in {"S/N", "SN", "NAN"} else f"{u.NU_ENDERECO} "
            consultas = [
                ("rua", {"street": f"{numero}{u.NO_LOGRADOURO}", "city": cidade, "state": estado, "country": "Brasil"}),
                ("cep", {"postalcode": str(u.CO_CEP), "city": cidade, "country": "Brasil"}),
                ("nome", {"q": f"{u.NO_FANTASIA}, {cidade}, {estado}, Brasil"}),
            ]
            for fonte, consulta in consultas:
                g = geocodificar(consulta, cache)
                if not g:
                    continue
                q = gpd.GeoSeries(gpd.points_from_xy([g[1]], [g[0]]), crs="EPSG:4326").to_crs(crs_m).iloc[0]
                if pode_confirmar and q.distance(p) <= tolerancia:
                    metodo = f"original_confirmada_{fonte}"
                    break
                perto_do_bairro = len(alvo) > 0 and alvo.distance(q).min() <= LIMITE_PERTO_M
                if municipio.distance(q) <= LIMITE_FORA_M and perto_do_bairro:
                    lat, lon = g
                    metodo = f"nominatim_{fonte}"
                    break
            grosseiro = (status in {"fora_do_municipio", "coordenada_compartilhada"}
                         or (dist_bairro is not None and dist_bairro > LIMITE_GROSSEIRO_M))
            if metodo == "revisar_manual" and grosseiro and len(alvo):
                # Prefere o bairro do endereço; senão, o bairro do nome
                base = alvo[do_endereco[alvo.index]] if do_endereco[alvo.index].any() else alvo
                c = gpd.GeoSeries([base.geometry.iloc[0].representative_point()], crs=crs_m).to_crs("EPSG:4326")
                lat, lon, metodo = c.y.iloc[0], c.x.iloc[0], "aproximada_pelo_bairro"
            elif metodo == "revisar_manual" and (grosseiro or status == "sem_area_esperada"):
                # Sem o bairro na malha do IBGE: procura o bairro do endereço no OpenStreetMap.
                # Em sem_area_esperada, só move se o bairro estiver a mais de 5 km (erro grosseiro).
                g = geocodificar({"q": f"{u.NO_BAIRRO}, {cidade}, {estado}, Brasil"}, cache)
                if g:
                    q = gpd.GeoSeries(gpd.points_from_xy([g[1]], [g[0]]), crs="EPSG:4326").to_crs(crs_m).iloc[0]
                    minimo = LIMITE_COMPARTILHADA_M if grosseiro else LIMITE_GROSSEIRO_M
                    if municipio.distance(q) <= LIMITE_FORA_M and q.distance(p) > minimo:
                        lat, lon, metodo = g[0], g[1], "aproximada_pelo_bairro_osm"

        movido = gpd.GeoSeries(gpd.points_from_xy([lon], [lat]), crs="EPSG:4326").to_crs(crs_m).distance(p).iloc[0]
        linhas.append({"CO_CNES": u.CO_CNES, "municipio": capital, "NO_FANTASIA": u.NO_FANTASIA,
                       "endereco": f"{u.NO_LOGRADOURO}, {u.NU_ENDERECO}, CEP {u.CO_CEP}",
                       "bairro_cnes": u.NO_BAIRRO, "bairro_no_nome": bairro_nome,
                       "bairro_da_coordenada": bairro_coord,
                       "dist_ao_bairro_esperado_m": None if dist_bairro is None else round(dist_bairro),
                       "fora_do_municipio_m": round(fora), "status": status, "metodo": metodo,
                       "lat": lat, "lon": lon, "deslocamento_m": round(movido),
                       "mapa_original": f"https://www.openstreetmap.org/?mlat={u.lat}&mlon={u.lon}#map=17/{u.lat}/{u.lon}",
                       "mapa_final": f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=17/{lat}/{lon}"})
    return linhas


def main():
    pa = pd.read_csv(PROC / "pa_capitais.csv", dtype={"CO_CNES": str, "CO_CEP": str, "NU_ENDERECO": str})
    capitais = pd.read_csv(PROC / "capitais_resumo.csv", dtype={"co_ibge7": str}).set_index("municipio")
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}

    linhas = []
    for capital, grupo in pa.groupby("municipio"):
        uf = capital.split(" - ")[1]
        if not (GPKG_DIR / f"{uf}_setores_CD2022.gpkg").exists():
            print(f"{capital}: malha de setores ainda não baixada, pulando")
            continue
        print(f"{capital}: {len(grupo)} unidades")
        linhas += conferir_capital(capital, capitais.loc[capital, "co_ibge7"], grupo, cache)
        CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=0))

    conf = pd.DataFrame(linhas)
    if MANUAIS.exists():
        man = pd.read_csv(MANUAIS, dtype={"CO_CNES": str}).set_index("CO_CNES")
        sel = conf.CO_CNES.isin(man.index)
        conf.loc[sel, "lat"] = conf.loc[sel, "CO_CNES"].map(man.lat)
        conf.loc[sel, "lon"] = conf.loc[sel, "CO_CNES"].map(man.lon)
        conf.loc[sel, "metodo"] = "manual"
    conf.to_csv(PROC / "conferencia_coordenadas.csv", index=False)

    corrigido = pa.drop(columns=["lat", "lon"]).merge(conf[["CO_CNES", "lat", "lon", "status", "metodo"]],
                                                      on="CO_CNES", how="left")
    corrigido.to_csv(PROC / "pa_capitais_corrigido.csv", index=False)

    print("\nStatus das coordenadas originais:\n" + conf.status.value_counts().to_string())
    print("\nMétodo da coordenada final:\n" + conf.metodo.value_counts().to_string())
    pd.set_option("display.width", 250)
    prob = conf[conf.metodo.str.startswith(("revisar", "aproximada", "nominatim"))]
    print("\nUnidades corrigidas ou a revisar:\n" + prob[[
        "municipio", "NO_FANTASIA", "bairro_cnes", "bairro_da_coordenada", "dist_ao_bairro_esperado_m",
        "status", "metodo", "deslocamento_m"]].to_string(index=False))


if __name__ == "__main__":
    main()
