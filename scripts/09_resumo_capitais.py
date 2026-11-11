"""Junta as distâncias de todas as capitais (saídas do script 03) e faz o resumo por capital.

Uso: cd scripts && ../.venv/bin/python 09_resumo_capitais.py
Saídas:
  dados/processados/resumo_distancias_capitais.csv
  figuras/exploracao/13_renda_distancia_capitais.png
  figuras/exploracao/14_densidade_renda_todas.png
"""
from importlib import import_module
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import estilo
from estilo import AZUL, LARANJA, TEXTO, TEXTO_2, CMAP_AZUL

d03 = import_module("03_distancias_capital")
ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dados/processados/distancias"
FIG = ROOT / "figuras/exploracao"
QUARTIS = ["Q1", "Q2", "Q3", "Q4"]
# Ligação ao nó mais próximo acima disso = sem acesso viário mapeado (ilhas, áreas rurais ribeirinhas)
LIGACAO_MAX_M = 2000


def gini(valores, pesos):
    """Gini ponderado (0 = todos à mesma distância; perto de 1 = muito desigual)."""
    ordem = np.argsort(valores)
    x, w = np.asarray(valores)[ordem], np.asarray(pesos)[ordem]
    acum_w = np.cumsum(w) / w.sum()
    acum_xw = np.cumsum(x * w) / (x * w).sum()
    area = np.sum((acum_xw[1:] + acum_xw[:-1]) / 2 * np.diff(acum_w)) + acum_xw[0] * acum_w[0] / 2
    return 1 - 2 * area


def media(d):
    return np.average(d.d_m, weights=d.populacao) / 1000


def carregar(sufixo):
    capitais = pd.read_csv(ROOT / "dados/processados/capitais_resumo.csv")
    por_slug = {d03.slug(c): c for c in capitais.municipio}
    partes = []
    for arq in sorted(DIST.glob(f"*_{sufixo}_setores.csv")):
        nome = arq.name.removesuffix(f"_{sufixo}_setores.csv")
        d = pd.read_csv(arq, dtype={"CD_SETOR": str})
        d["capital"] = por_slug.get(nome, nome)
        partes.append(d)
    todos = pd.concat(partes)
    habitados = todos[todos.populacao > 0]
    sem_acesso = habitados.ligacao_m > LIGACAO_MAX_M
    excluidos = (habitados.populacao[sem_acesso].groupby(habitados.capital[sem_acesso]).sum()
                 / habitados.groupby("capital").populacao.sum() * 100).fillna(0)
    hab = habitados[~sem_acesso & np.isfinite(habitados.d_m)].copy()
    hab.attrs["pct_excluida"] = excluidos
    # Quartis calculados dentro de cada capital (planejamento, seção 6.1)
    hab["q_renda"] = hab.groupby("capital").renda_media.transform(lambda r: pd.qcut(r, 4, labels=QUARTIS))
    hab["q_dens"] = hab.groupby("capital").densidade.transform(lambda r: pd.qcut(r, 4, labels=QUARTIS))
    hab["d_rel"] = hab.d_m / hab.groupby("capital").apply(
        lambda d: np.average(d.d_m, weights=d.populacao), include_groups=False).reindex(hab.capital).to_numpy()
    return hab


def resumo(hab):
    linhas = []
    for capital, d in hab.groupby("capital"):
        q = d.groupby("q_renda", observed=True)
        linhas.append({
            "capital": capital, "setores": len(d), "populacao": d.populacao.sum(),
            "dist_media_km": media(d), "gini_dist": gini(d.d_m, d.populacao),
            "dist_Q1_renda_km": media(q.get_group("Q1")), "dist_Q4_renda_km": media(q.get_group("Q4")),
            "dist_favela_km": media(d[d.favela]) if d.favela.any() else np.nan,
            "dist_nao_favela_km": media(d[~d.favela]),
        })
    r = pd.DataFrame(linhas).set_index("capital")
    r["razao_Q1_Q4"] = r.dist_Q1_renda_km / r.dist_Q4_renda_km
    r["pct_pop_sem_acesso_viario"] = hab.attrs["pct_excluida"].reindex(r.index).fillna(0)
    return r


def fig_halteres(r_sus, arquivo):
    r = r_sus.sort_values("razao_Q1_Q4")
    fig, ax = plt.subplots(figsize=(8.5, 9))
    y = np.arange(len(r))
    ax.hlines(y, r.dist_Q1_renda_km, r.dist_Q4_renda_km, color="#c9c7c0", linewidth=2.5, zorder=1)
    ax.scatter(r.dist_Q1_renda_km, y, color=LARANJA, s=55, zorder=3, edgecolor="white", linewidth=1.2,
               label="25% de menor renda (Q1)")
    ax.scatter(r.dist_Q4_renda_km, y, color=AZUL, s=55, zorder=3, edgecolor="white", linewidth=1.2,
               label="25% de maior renda (Q4)")
    ax.set_yticks(y, [c.split(" - ")[0] for c in r.index])
    for yi, (_, l) in zip(y, r.iterrows()):
        ax.text(max(l.dist_Q1_renda_km, l.dist_Q4_renda_km) + 0.15, yi, f"{l.razao_Q1_Q4:.2f}",
                va="center", fontsize=8, color=TEXTO_2)
    ax.set_xlabel("distância média pela rua até o PA do SUS mais próximo (km)")
    ax.set_title("Quem mora mais longe do pronto-atendimento do SUS?\n", loc="left")
    ax.text(0, 1.01, "número = razão Q1/Q4 (abaixo de 1: os mais pobres moram mais perto); "
            "quartis de renda dentro de cada capital", transform=ax.transAxes, fontsize=8, color=TEXTO_2)
    ax.legend(loc="upper left", bbox_to_anchor=(0, -0.06), ncol=2)
    ax.grid(axis="y", visible=False)
    fig.savefig(arquivo)
    plt.close(fig)


def tabela_densidade_renda(hab):
    t = hab.groupby(["q_dens", "q_renda"], observed=True).apply(
        lambda d: np.average(d.d_rel, weights=d.populacao), include_groups=False).unstack()
    return t.iloc[::-1]


def fig_tabelas(t_todos, t_sus, arquivo):
    fig, axs = plt.subplots(1, 2, figsize=(12, 5), sharey=True, gridspec_kw={"wspace": 0.08})
    for ax, t, titulo in [(axs[0], t_todos, "(a) Todos os pronto-atendimentos"),
                          (axs[1], t_sus, "(b) Só os do SUS")]:
        im = ax.imshow(t.to_numpy(), cmap=CMAP_AZUL, vmin=0.6, vmax=1.4)
        for i in range(4):
            for j in range(4):
                v = t.iat[i, j]
                ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=10.5,
                        color="white" if v > 1.12 else TEXTO)
        ax.set_xticks(range(4), ["Q1\nmenor renda", "Q2", "Q3", "Q4\nmaior renda"])
        ax.set_yticks(range(4), ["Q4 mais denso", "Q3", "Q2", "Q1 menos denso"])
        ax.grid(False)
        ax.set_title(titulo)
    axs[1].tick_params(labelleft=False)
    fig.colorbar(im, ax=axs, label="distância média / média da própria capital", shrink=0.85)
    fig.suptitle("Densidade × renda nas 26 capitais (quartis dentro de cada capital; 1,00 = média da capital)",
                 x=0.01, ha="left", fontsize=10, color=TEXTO_2)
    fig.savefig(arquivo)
    plt.close(fig)


def main():
    estilo.aplicar()
    hab_todos, hab_sus = carregar("drive"), carregar("drive_sus")
    r_todos, r_sus = resumo(hab_todos), resumo(hab_sus)
    saida = r_todos.join(r_sus, rsuffix="_sus")
    saida.round(3).to_csv(ROOT / "dados/processados/resumo_distancias_capitais.csv")

    fig_halteres(r_sus, FIG / "13_renda_distancia_capitais.png")
    t_todos, t_sus = tabela_densidade_renda(hab_todos), tabela_densidade_renda(hab_sus)
    fig_tabelas(t_todos, t_sus, FIG / "14_densidade_renda_todas.png")

    pd.set_option("display.width", 220)
    print("Só SUS:\n" + r_sus[["dist_media_km", "gini_dist", "dist_Q1_renda_km", "dist_Q4_renda_km", "razao_Q1_Q4",
                               "dist_favela_km", "dist_nao_favela_km", "pct_pop_sem_acesso_viario"]]
          .sort_values("razao_Q1_Q4").round(2).to_string())
    print(f"\nCapitais em que os mais pobres (Q1) moram mais perto que os mais ricos (Q4), só SUS: "
          f"{(r_sus.razao_Q1_Q4 < 1).sum()} de {len(r_sus)}")
    print(f"Capitais em que a favela está mais perto, só SUS: "
          f"{(r_sus.dist_favela_km < r_sus.dist_nao_favela_km).sum()} de {r_sus.dist_favela_km.notna().sum()}")
    print("\nTabela densidade × renda, todas as capitais, só SUS:\n" + t_sus.round(2).to_string())
    print("\nTabela densidade × renda, todas as capitais, todos os PAs:\n" + t_todos.round(2).to_string())


if __name__ == "__main__":
    main()
