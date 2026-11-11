"""Distância pela rua de cada setor censitário até o pronto-atendimento mais próximo (seção 5 do planejamento).

Uso:
  .venv/bin/python scripts/03_distancias_capital.py "Fortaleza - CE" [--rede drive|walk] [--so-sus]

Entradas:
  dados/processados/capitais_resumo.csv, setores_capitais.csv (scripts 01 e 02), pa_capitais_corrigido.csv (script 07)
  dados/ibge/setores_gpkg/<UF>_setores_CD2022.gpkg (baixado do IBGE se não existir)
  Rede viária do OpenStreetMap (extrato regional do Geofabrik, recortado e guardado em dados/osm/)
Saídas:
  dados/processados/distancias/<capital>_<rede>[_sus]_setores.csv     (uma linha por setor)
  dados/processados/distancias/<capital>_<rede>[_sus]_comunidades.csv (uma linha por pronto-atendimento)
  figuras/validacao/<capital>_<rede>[_sus].png                        (mapa para conferência)
"""
import argparse
import unicodedata
import urllib.request
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import osmnx as ox
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "dados/processados"
GPKG_DIR = ROOT / "dados/ibge/setores_gpkg"
OSM_DIR = ROOT / "dados/osm"
GPKG_URL = ("https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios/"
            "malha_com_atributos/setores/gpkg/UF/{uf}/{uf}_setores_CD2022.gpkg")

FAIXA_BORDA_M = 5000      # folga em volta do limite municipal (seção 5, passo 1)
LIGACAO_SUSPEITA_M = 500  # ligações ponto -> nó acima disso são marcadas para conferência
CD_SIT_AGUA = "9"         # setores "Massas de água" ficam de fora

# Rampa sequencial azul (referência do guia de visualização), clara -> escura
RAMPA_AZUL = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]


def slug(texto):
    s = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return s.split(" - ")[0].lower().replace(" ", "_")


def carregar_setores(capital, cd_mun, crs):
    uf = capital.split(" - ")[1]
    gpkg = GPKG_DIR / f"{uf}_setores_CD2022.gpkg"
    if not gpkg.exists():
        GPKG_DIR.mkdir(parents=True, exist_ok=True)
        print(f"Baixando {gpkg.name} do IBGE...")
        urllib.request.urlretrieve(GPKG_URL.format(uf=uf), gpkg)
    setores = gpd.read_file(gpkg, where=f"CD_MUN='{cd_mun}'", columns=["CD_SETOR", "CD_SIT", "AREA_KM2"])
    setores = setores[setores.CD_SIT != CD_SIT_AGUA].to_crs(crs)

    atributos = pd.read_csv(PROC / "setores_capitais.csv", dtype={"CD_SETOR": str},
                            usecols=["CD_SETOR", "populacao", "densidade", "renda_media", "favela"])
    return setores.merge(atributos, on="CD_SETOR", how="left")


# Extratos regionais do Geofabrik (o servidor Overpass costuma ficar sobrecarregado)
REGIAO_DA_UF = {**dict.fromkeys(["AC", "AM", "AP", "PA", "RO", "RR", "TO"], "norte"),
                **dict.fromkeys(["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"], "nordeste"),
                **dict.fromkeys(["DF", "GO", "MS", "MT"], "centro-oeste"),
                **dict.fromkeys(["ES", "MG", "RJ", "SP"], "sudeste"),
                **dict.fromkeys(["PR", "RS", "SC"], "sul")}
PBF_URL = "https://download.geofabrik.de/south-america/brazil/{regiao}-latest.osm.pbf"

# Mesmos filtros de via que o osmnx usa para network_type="drive" e "walk"
EXCLUI_HIGHWAY = {
    "drive": {"abandoned", "bridleway", "bus_guideway", "construction", "corridor", "cycleway", "elevator",
              "escalator", "footway", "no", "path", "pedestrian", "planned", "platform", "proposed", "raceway",
              "razed", "rest_area", "service", "services", "steps", "track"},
    "walk": {"abandoned", "bus_guideway", "construction", "cycleway", "motorway", "motorway_link", "no",
             "planned", "platform", "proposed", "raceway", "razed", "rest_area", "services"},
}


def via_entra(tags, rede):
    hw = tags.get("highway")
    if hw is None or hw in EXCLUI_HIGHWAY[rede] or tags.get("area") == "yes":
        return False
    if tags.get("access") == "private":
        return False
    if rede == "drive":
        return (tags.get("motor_vehicle") != "no" and tags.get("motorcar") != "no" and tags.get("service") not in
                {"alley", "driveway", "emergency_access", "parking", "parking_aisle", "private"})
    return tags.get("foot") != "no" and tags.get("service") != "private"


def baixar_rede(boundary_wgs84, nome, rede, uf):
    import osmium

    OSM_DIR.mkdir(parents=True, exist_ok=True)
    arquivo = OSM_DIR / f"{nome}_{rede}.graphml"
    if arquivo.exists():
        return ox.load_graphml(arquivo)

    regiao = REGIAO_DA_UF[uf]
    pbf = OSM_DIR / "pbf" / f"{regiao}-latest.osm.pbf"
    if not pbf.exists():
        pbf.parent.mkdir(parents=True, exist_ok=True)
        print(f"Baixando o extrato {pbf.name} do Geofabrik...")
        urllib.request.urlretrieve(PBF_URL.format(regiao=regiao), pbf)

    # Recorta do extrato as vias que tocam o retângulo do limite e grava em XML com os nós usados
    print(f"Recortando a rede '{rede}' de {pbf.name}...")
    x0, y0, x1, y1 = boundary_wgs84.bounds
    xml = OSM_DIR / f"{nome}_{rede}.osm"
    vias = (osmium.FileProcessor(str(pbf)).with_locations()
            .with_filter(osmium.filter.EntityFilter(osmium.osm.WAY))
            .with_filter(osmium.filter.KeyFilter("highway")))
    with osmium.BackReferenceWriter(str(xml), ref_src=str(pbf), overwrite=True) as escritor:
        for via in vias:
            if not via_entra(via.tags, rede):
                continue
            if any(n.location.valid() and x0 <= n.lon <= x1 and y0 <= n.lat <= y1 for n in via.nodes):
                escritor.add(via)

    G = ox.graph_from_xml(xml, bidirectional=(rede == "walk"), retain_all=True)
    G = ox.truncate.truncate_graph_polygon(G, boundary_wgs84)
    ox.save_graphml(G, arquivo)
    xml.unlink()
    return G


def grafo_para_matriz_invertida(G):
    """Matriz esparsa do grafo com as arestas invertidas (v -> u), peso = comprimento em metros.

    Rodar o Dijkstra a partir dos pronto-atendimentos nessa matriz dá a distância de cada nó ATÉ
    o pronto-atendimento, respeitando as mãos de direção (seção 5, passo 3).
    """
    nos = list(G.nodes)
    idx = {n: i for i, n in enumerate(nos)}
    arestas = pd.DataFrame(
        [(idx[v], idx[u], d["length"]) for u, v, d in G.edges(data=True)],
        columns=["origem", "destino", "comprimento"])
    # Arestas paralelas: fica a mais curta. Comprimento zero viraria "sem aresta" na matriz esparsa.
    arestas = arestas.groupby(["origem", "destino"], as_index=False).comprimento.min()
    arestas["comprimento"] = arestas.comprimento.clip(lower=0.01)
    n = len(nos)
    M = coo_matrix((arestas.comprimento, (arestas.origem, arestas.destino)), shape=(n, n)).tocsr()
    return M, nos, idx


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("capital", help='nome como no IBGE, por exemplo "Fortaleza - CE"')
    parser.add_argument("--rede", default="drive", choices=["drive", "walk"])
    parser.add_argument("--so-sus", action="store_true", help="usar só pronto-atendimentos que atendem o SUS")
    args = parser.parse_args()
    capital, rede, nome = args.capital, args.rede, slug(args.capital)
    sufixo = f"{rede}_sus" if args.so_sus else rede

    capitais = pd.read_csv(PROC / "capitais_resumo.csv", dtype={"co_ibge7": str}).set_index("municipio")
    cd_mun = capitais.loc[capital, "co_ibge7"]

    # 1. Limite: união dos setores + faixa de 5 km. Tudo é feito em metros (UTM da capital).
    setores = carregar_setores(capital, cd_mun, "EPSG:4674")
    crs_m = setores.estimate_utm_crs()
    setores = setores.to_crs(crs_m)
    municipio = setores.union_all()
    limite = gpd.GeoSeries([municipio.buffer(FAIXA_BORDA_M)], crs=crs_m).to_crs("EPSG:4326").iloc[0]

    # 2. Grafo: rede viária do OSM, só a maior componente fortemente conexa (todo nó alcança todo nó).
    G = baixar_rede(limite, nome, rede, capital.split(" - ")[1])
    G = ox.truncate.largest_component(G, strongly=True)
    G = ox.project_graph(G, to_crs=crs_m)
    print(f"Rede '{rede}': {G.number_of_nodes()} nós, {G.number_of_edges()} arestas")

    # 4. Ligar pronto-atendimentos e setores ao nó mais próximo.
    pa = pd.read_csv(PROC / "pa_capitais_corrigido.csv", dtype={"CO_CNES": str})
    pa = pa[(pa.municipio == capital) & (pa.atende_sus | (not args.so_sus))].reset_index(drop=True)
    pa = gpd.GeoDataFrame(pa, geometry=gpd.points_from_xy(pa.lon, pa.lat), crs="EPSG:4326").to_crs(crs_m)
    pa["fora_do_municipio_m"] = pa.geometry.distance(municipio).round(0)
    pa["no"], pa["ligacao_m"] = ox.distance.nearest_nodes(G, pa.geometry.x, pa.geometry.y, return_dist=True)

    pontos = setores.geometry.representative_point()
    setores["no"], setores["ligacao_m"] = ox.distance.nearest_nodes(G, pontos.x, pontos.y, return_dist=True)

    # 5. Dijkstra multi-fonte no grafo invertido.
    M, nos, idx = grafo_para_matriz_invertida(G)
    fontes = pa.drop_duplicates("no")  # dois PAs no mesmo nó: o primeiro representa os dois
    dist, _, origem = dijkstra(M, directed=True, indices=[idx[n] for n in fontes.no],
                               min_only=True, return_predecessors=True)
    pa_do_no = {idx[n]: i for i, n in zip(fontes.index, fontes.no)}

    # 6. Distância do setor = rede + ligação do setor + ligação do PA.
    i_no = setores.no.map(idx).to_numpy()
    setores["pa"] = [pa_do_no.get(o) for o in origem[i_no]]
    setores["dist_rede_m"] = dist[i_no]
    setores["d_m"] = setores.dist_rede_m + setores.ligacao_m + pa.loc[setores.pa, "ligacao_m"].to_numpy()
    pa_mais_proximo = gpd.GeoSeries(pa.geometry.loc[setores.pa].to_numpy(), index=setores.index, crs=crs_m)
    setores["euclid_m"] = pontos.distance(pa_mais_proximo)
    setores["CO_CNES"] = pa.loc[setores.pa, "CO_CNES"].to_numpy()

    # 7. Comunidades de serviço: setores com o mesmo PA mais próximo.
    hab = setores[setores.populacao > 0]
    comunidades = setores.groupby("CO_CNES").agg(area_km2=("AREA_KM2", "sum"), populacao=("populacao", "sum"),
                                                n_setores=("CD_SETOR", "size"))
    comunidades["renda_media"] = hab.groupby("CO_CNES").apply(
        lambda d: np.average(d.renda_media.dropna(), weights=d.populacao[d.renda_media.notna()])
        if d.renda_media.notna().any() else np.nan, include_groups=False)
    comunidades["D"] = 1 / comunidades.area_km2
    comunidades["rho"] = comunidades.populacao / comunidades.area_km2
    comunidades = comunidades.join(pa.set_index("CO_CNES")[["NO_FANTASIA"]])

    # Conferências (seção 5)
    print(f"\n=== {capital} ===")
    print(f"Pronto-atendimentos: {len(pa)} (em nós distintos: {len(fontes)})")
    fora = pa[pa.fora_do_municipio_m > 0]
    print(f"PAs fora do limite municipal: {len(fora)} {fora[['NO_FANTASIA', 'fora_do_municipio_m']].values.tolist()}")
    print(f"Ligação dos PAs à rede (m): máx {pa.ligacao_m.max():.0f}")
    print(f"Setores: {len(setores)} (habitados: {len(hab)}, população {hab.populacao.sum():,.0f})")
    print(f"Setores com distância infinita: {np.isinf(setores.d_m).sum()}")
    susp = hab[hab.ligacao_m > LIGACAO_SUSPEITA_M]
    print(f"Setores habitados com ligação > {LIGACAO_SUSPEITA_M} m: {len(susp)} "
          f"({susp.populacao.sum() / hab.populacao.sum():.2%} da população)")
    viol = (setores.d_m + 1e-6 < setores.euclid_m).sum()
    print(f"Setores com distância de rede < linha reta (deveria ser 0): {viol}")
    w, d = hab.populacao.to_numpy(), hab.d_m.to_numpy()
    ordem = np.argsort(d)
    mediana = np.interp(0.5, np.cumsum(w[ordem]) / w.sum(), d[ordem])
    print(f"Distância média ponderada pela população: {np.average(d, weights=w) / 1000:.2f} km")
    print(f"Mediana (por pessoa): {mediana / 1000:.2f} km; máximo: {d.max() / 1000:.2f} km")
    print(f"Razão rede / linha reta (mediana): {(hab.d_m / hab.euclid_m).median():.2f}")
    q = pd.qcut(hab.renda_media, 4, labels=["Q1 (menor)", "Q2", "Q3", "Q4 (maior)"])
    previa = hab.groupby(q, observed=True).apply(
        lambda d: np.average(d.d_m, weights=d.populacao) / 1000, include_groups=False)
    print("Prévia - distância média (km) por quartil de renda:\n" + previa.round(2).to_string())

    # Saídas
    saida = PROC / "distancias"
    saida.mkdir(parents=True, exist_ok=True)
    cols = ["CD_SETOR", "populacao", "AREA_KM2", "densidade", "renda_media", "favela",
            "CO_CNES", "d_m", "dist_rede_m", "ligacao_m", "euclid_m"]
    setores[cols].to_csv(saida / f"{nome}_{sufixo}_setores.csv", index=False)
    comunidades.to_csv(saida / f"{nome}_{sufixo}_comunidades.csv")

    mapa_validacao(setores, pa, capital, rede, ROOT / "figuras/validacao" / f"{nome}_{sufixo}.png")


def mapa_validacao(setores, pa, capital, rede, arquivo):
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 9))
    hab = setores[setores.populacao > 0]
    setores[setores.populacao.fillna(0) == 0].plot(ax=ax, color="#e4e2dd", linewidth=0)
    hab.assign(d_km=hab.d_m / 1000).plot(
        ax=ax, column="d_km", cmap=LinearSegmentedColormap.from_list("azul", RAMPA_AZUL),
        linewidth=0, legend=True,
        legend_kwds={"label": "Distância pela rua até o PA mais próximo (km)", "shrink": 0.6})
    setores.dissolve("CO_CNES").boundary.plot(ax=ax, color="#2b2b2b", linewidth=0.6)
    pa.plot(ax=ax, color="#b5651d", markersize=60, edgecolor="white", linewidth=1.5, zorder=3)
    ax.set_title(f"{capital}: áreas de atendimento (contornos) e pronto-atendimentos (pontos)\n"
                 f"rede '{rede}' do OpenStreetMap", fontsize=11, loc="left")
    ax.set_axis_off()
    fig.tight_layout()
    fig.savefig(arquivo, dpi=150)
    print(f"\nMapa de validação: {arquivo.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
