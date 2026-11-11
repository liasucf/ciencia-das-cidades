"""Monta a tabela de setores censitários das 27 capitais com população, área, situação e renda.

Entradas:
  dados/ibge/censo2022/BR_setores_CD2022.csv                         (malha com atributos, Censo 2022)
  dados/ibge/censo2022/Agregados_por_setores_renda_responsavel_BR.csv (renda do responsável, Censo 2022)
  dados/processados/capitais_resumo.csv                              (saída do script 01)
Saídas:
  dados/processados/setores_capitais.csv
  dados/processados/setores_capitais_resumo.csv
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CENSO = ROOT / "dados/ibge/censo2022"
OUT = ROOT / "dados/processados"

# Limiar urbano da Aula 5, slide 5 (critério EU-OECD para centro urbano)
LIMIAR_DENSIDADE = 1500  # hab/km²


def main():
    capitais = pd.read_csv(OUT / "capitais_resumo.csv", dtype={"co_ibge7": str})

    setores = pd.read_csv(CENSO / "BR_setores_CD2022.csv", dtype=str, encoding="utf-8-sig")
    setores = setores[setores.CD_MUN.isin(capitais.co_ibge7)]
    setores = setores[["CD_SETOR", "CD_MUN", "NM_MUN", "NM_UF", "SITUACAO", "CD_SIT", "CD_TIPO",
                       "AREA_KM2", "NM_CONCURB", "v0001"]].rename(columns={"v0001": "populacao"})
    setores["AREA_KM2"] = pd.to_numeric(setores.AREA_KM2, errors="coerce")
    setores["populacao"] = pd.to_numeric(setores.populacao, errors="coerce")

    renda = pd.read_csv(CENSO / "Agregados_por_setores_renda_responsavel_BR.csv", sep=";",
                        dtype=str, encoding="latin1", na_values=["X", "."])
    renda = renda[["CD_SETOR", "V06004", "V06006"]].rename(
        columns={"V06004": "renda_media", "V06006": "renda_mediana"})
    for c in ["renda_media", "renda_mediana"]:
        renda[c] = pd.to_numeric(renda[c], errors="coerce")

    s = setores.merge(renda, on="CD_SETOR", how="left")
    s["densidade"] = s.populacao / s.AREA_KM2
    s["favela"] = s.CD_TIPO == "1"
    s["acima_limiar"] = s.densidade >= LIMIAR_DENSIDADE
    s.to_csv(OUT / "setores_capitais.csv", index=False)

    habitados = s[s.populacao > 0]
    g = habitados.groupby("NM_MUN")
    resumo = pd.DataFrame({
        "setores_habitados": g.size(),
        "populacao": g.populacao.sum(),
        "pct_pop_rural_ibge": g.apply(lambda d: d.populacao[d.SITUACAO == "Rural"].sum() / d.populacao.sum() * 100, include_groups=False),
        "pct_pop_abaixo_1500": g.apply(lambda d: d.populacao[~d.acima_limiar].sum() / d.populacao.sum() * 100, include_groups=False),
        "pct_pop_favela": g.apply(lambda d: d.populacao[d.favela].sum() / d.populacao.sum() * 100, include_groups=False),
        "pct_setores_com_renda": g.renda_media.apply(lambda r: r.notna().mean() * 100),
        "renda_mediana_dos_setores": g.renda_mediana.median(),
    }).round(1).sort_values("populacao", ascending=False)
    resumo.to_csv(OUT / "setores_capitais_resumo.csv")

    pd.set_option("display.width", 220)
    print(resumo.to_string())
    print(f"\nSetores habitados nas capitais: {len(habitados)}; "
          f"com renda: {habitados.renda_media.notna().sum()}")


if __name__ == "__main__":
    main()
