"""Conta os pronto-atendimentos ativos (tipo 73 do CNES) em cada uma das 27 capitais.

Todo estabelecimento ativo do tipo 73 ("Pronto Atendimento") entra, seja UPA, PA, AMA 24h, SPA etc.
As colunas `atende_sus` e `nome_tem_upa` permitem recortes depois.

Entradas:
  dados/cnes/cnes_estabelecimentos.csv  (OpenDataSUS, CSV nacional do CNES)
  dados/ibge/pop2022.json               (IBGE, agregado 4709, variável 93: população residente 2022)
Saídas:
  dados/processados/pa_capitais.csv     (uma linha por pronto-atendimento nas capitais, com coordenadas)
  dados/processados/capitais_resumo.csv (uma linha por capital: população e contagens)
"""
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CNES = ROOT / "dados/cnes/cnes_estabelecimentos.csv"
POP = ROOT / "dados/ibge/pop2022.json"
OUT = ROOT / "dados/processados"

# Capitais identificadas pelo nome do IBGE ("Município - UF"), não por código digitado à mão
CAPITAIS = [
    "Porto Velho - RO", "Rio Branco - AC", "Manaus - AM", "Boa Vista - RR", "Belém - PA",
    "Macapá - AP", "Palmas - TO", "São Luís - MA", "Teresina - PI", "Fortaleza - CE",
    "Natal - RN", "João Pessoa - PB", "Recife - PE", "Maceió - AL", "Aracaju - SE",
    "Salvador - BA", "Belo Horizonte - MG", "Vitória - ES", "Rio de Janeiro - RJ",
    "São Paulo - SP", "Curitiba - PR", "Florianópolis - SC", "Porto Alegre - RS",
    "Campo Grande - MS", "Cuiabá - MT", "Goiânia - GO", "Brasília - DF",
]

TIPO_PRONTO_ATENDIMENTO = "73"
NOME_UPA = r"\bUPA\b|UPA ?24|UNIDADE DE PRONTO ATENDIMENTO|UNIDADE PRONTO ATENDIMENTO"


def carregar_populacao():
    serie = json.loads(POP.read_text())[0]["resultados"][0]["series"]
    pop = pd.DataFrame(
        {"co_ibge7": s["localidade"]["id"], "municipio": s["localidade"]["nome"],
         "populacao_2022": int(s["serie"]["2022"])}
        for s in serie
    )
    pop["co_ibge6"] = pop.co_ibge7.str[:6]
    cap = pop[pop.municipio.isin(CAPITAIS)].copy()
    faltando = set(CAPITAIS) - set(cap.municipio)
    if faltando:
        sys.exit(f"Capitais não encontradas no IBGE: {faltando}")
    return cap


def carregar_pronto_atendimentos():
    df = pd.read_csv(CNES, sep=";", dtype=str, encoding="latin1")
    df = df[(df.TP_UNIDADE == TIPO_PRONTO_ATENDIMENTO) & df.CO_MOTIVO_DESAB.isna()].copy()
    nome = df.NO_FANTASIA.fillna("") + " | " + df.NO_RAZAO_SOCIAL.fillna("")
    df["nome_tem_upa"] = nome.str.contains(NOME_UPA, regex=True)
    df["atende_sus"] = df.CO_AMBULATORIAL_SUS == "SIM"
    df["24h"] = df.DS_TURNO_ATENDIMENTO.str.startswith("ATENDIMENTO CONTINUO DE 24 HORAS", na=False)
    df["lat"] = pd.to_numeric(df.NU_LATITUDE, errors="coerce")
    df["lon"] = pd.to_numeric(df.NU_LONGITUDE, errors="coerce")
    df["tem_coordenada"] = df.lat.notna() & df.lon.notna() & (df.lat != 0)
    return df


def main():
    cap = carregar_populacao()
    pa = carregar_pronto_atendimentos()
    pa = pa[pa.CO_IBGE.isin(cap.co_ibge6)].merge(
        cap[["co_ibge6", "municipio"]], left_on="CO_IBGE", right_on="co_ibge6")

    g = pa.groupby("municipio")
    resumo = cap.set_index("municipio")[["co_ibge7", "populacao_2022"]].join([
        g.size().rename("n_pa"),
        g.atende_sus.sum().rename("n_pa_sus"),
        g["24h"].sum().rename("n_pa_24h"),
        g.nome_tem_upa.sum().rename("n_nome_upa"),
        g.tem_coordenada.sum().rename("n_com_coord"),
    ]).fillna(0)
    for c in ["n_pa", "n_pa_sus", "n_pa_24h", "n_nome_upa", "n_com_coord"]:
        resumo[c] = resumo[c].astype(int)
    resumo = resumo.sort_values("populacao_2022", ascending=False)

    OUT.mkdir(parents=True, exist_ok=True)
    pa[["CO_CNES", "municipio", "NO_FANTASIA", "DS_ESFERA_ADMINISTRATIVA", "DS_TURNO_ATENDIMENTO",
        "atende_sus", "24h", "nome_tem_upa", "NO_LOGRADOURO", "NU_ENDERECO", "NO_BAIRRO", "CO_CEP",
        "NU_LATITUDE", "NU_LONGITUDE", "lat", "lon", "tem_coordenada"]].to_csv(
        OUT / "pa_capitais.csv", index=False)
    resumo.to_csv(OUT / "capitais_resumo.csv")

    pd.set_option("display.width", 200)
    print(resumo.to_string())
    print(f"\nTotal de pronto-atendimentos nas capitais: {resumo.n_pa.sum()} "
          f"(SUS: {resumo.n_pa_sus.sum()}, 24h: {resumo.n_pa_24h.sum()}, "
          f"com coordenadas: {resumo.n_com_coord.sum()})")


if __name__ == "__main__":
    main()
