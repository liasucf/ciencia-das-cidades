"""Figura didática: o que o Dijkstra multi-fonte faz numa malha de ruas pequena.

Usa a mesma montagem de matriz invertida e a mesma chamada do scripts/03_distancias_capital.py.
Uso: .venv/bin/python scripts/05_esquema_dijkstra.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.lines import Line2D
from scipy.sparse.csgraph import dijkstra

import estilo
from estilo import AZUL, LARANJA, TEXTO, TEXTO_2
from importlib import import_module

grafo_para_matriz_invertida = import_module("03_distancias_capital").grafo_para_matriz_invertida

ROOT = Path(__file__).resolve().parents[1]


def malha_exemplo():
    """Grade 4 x 5 de quarteirões; uma avenida de mão única; comprimentos em metros."""
    G = nx.MultiDiGraph()
    rng = np.random.default_rng(3)
    pos = {}
    for i in range(4):
        for j in range(5):
            pos[(i, j)] = (j * 150 + rng.uniform(-15, 15), i * 120 + rng.uniform(-15, 15))
    mao_unica = {((1, j), (1, j + 1)) for j in range(4)}  # avenida da linha 1: só para a direita
    for (i, j), (x, y) in pos.items():
        for di, dj in [(0, 1), (1, 0)]:
            v = (i + di, j + dj)
            if v not in pos:
                continue
            comp = round(float(np.hypot(pos[v][0] - x, pos[v][1] - y)))
            G.add_edge((i, j), v, length=comp)
            if ((i, j), v) not in mao_unica:
                G.add_edge(v, (i, j), length=comp)
    return G, pos, mao_unica


def main():
    estilo.aplicar()
    G, pos, mao_unica = malha_exemplo()
    pas = [(0, 0), (3, 4)]
    cor_pa = {pas[0]: AZUL, pas[1]: LARANJA}

    M, nos, idx = grafo_para_matriz_invertida(G)
    dist, _, origem = dijkstra(M, directed=True, indices=[idx[p] for p in pas], min_only=True,
                               return_predecessors=True)
    mais_proximo = {n: nos[origem[idx[n]]] for n in nos}

    fig, (a, b) = plt.subplots(1, 2, figsize=(13, 5.2))
    for ax in (a, b):
        ax.set_aspect("equal")
        ax.set_axis_off()
        for u, v, d in G.edges(data=True):
            (x0, y0), (x1, y1) = pos[u], pos[v]
            ax.plot([x0, x1], [y0, y1], color="#c9c7c0", linewidth=3, zorder=1, solid_capstyle="round")
        for u, v in mao_unica:
            (x0, y0), (x1, y1) = pos[u], pos[v]
            ax.annotate("", xy=(x0 + 0.62 * (x1 - x0), y0 + 0.62 * (y1 - y0)),
                        xytext=(x0 + 0.38 * (x1 - x0), y0 + 0.38 * (y1 - y0)),
                        arrowprops={"arrowstyle": "-|>", "color": TEXTO, "lw": 1.6}, zorder=2)

    # (a) A entrada: ruas com comprimento, interseções e os dois PAs
    for u, v, d in G.edges(data=True):
        if (v, u) in G.edges and u > v:
            continue
        (x0, y0), (x1, y1) = pos[u], pos[v]
        a.text((x0 + x1) / 2, (y0 + y1) / 2 + 9, f"{d['length']}", fontsize=7, color=TEXTO_2, ha="center")
    for n, (x, y) in pos.items():
        a.scatter(x, y, s=40, color="white", edgecolor=TEXTO_2, linewidth=1.2, zorder=3)
    for p in pas:
        a.scatter(*pos[p], s=260, marker="P", color=cor_pa[p], edgecolor="white", linewidth=1.5, zorder=4)
    a.set_title("(a) Entrada: ruas (comprimento em m), interseções e 2 PAs")

    # (b) A saída: distância até o PA mais próximo e qual é ele
    for n, (x, y) in pos.items():
        c = cor_pa[mais_proximo[n]]
        b.scatter(x, y, s=330, color=c, edgecolor="white", linewidth=1.5, zorder=3)
        b.text(x, y, f"{dist[idx[n]]:.0f}", fontsize=7, color="white", ha="center", va="center",
               fontweight="bold", zorder=4)
    for p in pas:
        b.scatter(*pos[p], s=520, marker="P", color=cor_pa[p], edgecolor=TEXTO, linewidth=1.5, zorder=5)
    b.set_title("(b) Saída: metros até o PA mais próximo (cor = qual PA)")
    b.legend(handles=[
        Line2D([], [], marker="o", linestyle="", markersize=10, color=AZUL, label="mais perto do PA azul"),
        Line2D([], [], marker="o", linestyle="", markersize=10, color=LARANJA, label="mais perto do PA laranja"),
        Line2D([], [], marker=r"$\rightarrow$", linestyle="", markersize=12, color=TEXTO, label="rua de mão única"),
    ], loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=3)
    fig.tight_layout()
    saida = ROOT / "figuras/exploracao/09_esquema_dijkstra.png"
    fig.savefig(saida)
    print(saida.relative_to(ROOT))


if __name__ == "__main__":
    main()
