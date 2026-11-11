"""Figuras da rede viária e do resultado do Dijkstra para uma capital (rodar depois do script 03).

Uso: cd scripts && ../.venv/bin/python 06_figuras_rede.py "Fortaleza - CE"
Saídas em figuras/exploracao/ (10 a 12).
"""
import sys
from importlib import import_module
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import osmnx as ox
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
from scipy.sparse.csgraph import dijkstra

import estilo
from estilo import AZUL, LARANJA, VERDE_AGUA, NEUTRO, TEXTO, TEXTO_2, CMAP_AZUL, RAMPA_AZUL

d03 = import_module("03_distancias_capital")
ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figuras/exploracao"

CLASSES = {
    "principal": ({"motorway", "trunk", "primary", "motorway_link", "trunk_link", "primary_link"}, AZUL, 1.3),
    "secundária": ({"secondary", "tertiary", "secondary_link", "tertiary_link"}, LARANJA, 0.8),
    "local": (None, "#a9a7a0", 0.25),
}


def classe(highway):
    hw = highway[0] if isinstance(highway, list) else highway
    for nome, (tipos, _, _) in CLASSES.items():
        if tipos is None or hw in tipos:
            return nome


def carregar(capital):
    nome = d03.slug(capital)
    G = ox.load_graphml(ROOT / f"dados/osm/{nome}_drive.graphml")
    G = ox.truncate.largest_component(G, strongly=True)
    setores_csv = pd.read_csv(ROOT / f"dados/processados/distancias/{nome}_drive_setores.csv",
                              dtype={"CD_SETOR": str, "CO_CNES": str})
    cap = pd.read_csv(ROOT / "dados/processados/capitais_resumo.csv", dtype={"co_ibge7": str}).set_index("municipio")
    uf = capital.split(" - ")[1]
    geo = gpd.read_file(ROOT / f"dados/ibge/setores_gpkg/{uf}_setores_CD2022.gpkg",
                        where=f"CD_MUN='{cap.loc[capital, 'co_ibge7']}'", columns=["CD_SETOR"])
    crs_m = geo.estimate_utm_crs()
    setores = geo.to_crs(crs_m).merge(setores_csv, on="CD_SETOR")
    G = ox.project_graph(G, to_crs=crs_m)
    pa = pd.read_csv(ROOT / "dados/processados/pa_capitais_corrigido.csv", dtype={"CO_CNES": str})
    pa = pa[pa.municipio == capital]
    pa = gpd.GeoDataFrame(pa, geometry=gpd.points_from_xy(pa.lon, pa.lat), crs="EPSG:4326").to_crs(crs_m)
    return nome, G, setores, pa


def fig_rede(capital, nome, G, setores, pa):
    arestas = ox.graph_to_gdfs(G, nodes=False)
    arestas["classe"] = arestas.highway.map(classe)
    comp_km = arestas.groupby("classe").length.sum() / 1000
    mao_unica = arestas.oneway.astype(bool).mean()
    fig, ax = plt.subplots(figsize=(11, 10))
    setores.dissolve().boundary.plot(ax=ax, color=TEXTO_2, linewidth=0.8, linestyle="--")
    for nome_c in ["local", "secundária", "principal"]:
        _, cor, lw = CLASSES[nome_c]
        arestas[arestas.classe == nome_c].plot(ax=ax, color=cor, linewidth=lw)
    pa.plot(ax=ax, color=VERDE_AGUA, markersize=80, edgecolor="white", linewidth=1.5, zorder=4, marker="P")
    ax.set_axis_off()
    ax.set_title(f"{capital}: rede viária para carro (OpenStreetMap) e pronto-atendimentos", loc="left")
    rotulos = {"principal": "vias principais", "secundária": "vias secundárias", "local": "vias locais"}
    leg = [Line2D([], [], color=CLASSES[c][1], linewidth=max(CLASSES[c][2] * 2, 1.2),
                  label=f"{rotulos[c]} ({comp_km.get(c, 0):,.0f} km)")
           for c in ["principal", "secundária", "local"]]
    leg += [Line2D([], [], marker="P", linestyle="", markersize=11, color=VERDE_AGUA, label="pronto-atendimento"),
            Line2D([], [], color=TEXTO_2, linestyle="--", label="limite do município")]
    ax.legend(handles=leg, loc="lower left")
    ax.text(0.99, 0.01, f"{G.number_of_nodes():,} interseções (nós), {G.number_of_edges():,} trechos (arestas); "
            f"{mao_unica:.0%} dos trechos são de mão única", transform=ax.transAxes, ha="right", fontsize=8,
            color=TEXTO_2)
    fig.savefig(FIG / f"10_rede_{nome}.png")
    plt.close(fig)


def fig_onda(capital, nome, G, pa):
    """Zoom em torno de um PA: cor de cada trecho = distância até o PA mais próximo (a 'onda' do Dijkstra)."""
    M, nos, idx = d03.grafo_para_matriz_invertida(G)
    pa_nos = ox.distance.nearest_nodes(G, pa.geometry.x, pa.geometry.y)
    dist, _, _ = dijkstra(M, directed=True, indices=sorted({idx[n] for n in pa_nos}), min_only=True,
                          return_predecessors=True)
    nos_gdf, arestas = ox.graph_to_gdfs(G)
    d_no = pd.Series(dist, index=nos)
    arestas = arestas.reset_index()
    arestas["d_km"] = (d_no.loc[arestas.u].to_numpy() + d_no.loc[arestas.v].to_numpy()) / 2 / 1000

    # Janela centrada entre os dois PAs mais próximos entre si, para mostrar as duas "ondas" se encontrando
    xy = np.column_stack([pa.geometry.x, pa.geometry.y])
    dists = np.linalg.norm(xy[:, None] - xy[None], axis=2) + np.eye(len(xy)) * 1e12
    i, j = np.unravel_index(dists.argmin(), dists.shape)
    centro = pa.geometry.iloc[[i, j]].union_all().centroid
    meia = max(2500, dists[i, j] / 2 + 1500)
    janela = arestas.cx[centro.x - meia:centro.x + meia, centro.y - meia:centro.y + meia]
    fig, ax = plt.subplots(figsize=(9, 9))
    # Mesma escala da figura 12 (claro = perto, escuro = longe), sem o tom mais claro, que some no fundo
    cmap = LinearSegmentedColormap.from_list("azul_visivel", RAMPA_AZUL[1:])
    janela.plot(ax=ax, column="d_km", cmap=cmap, linewidth=1.4, legend=True,
                vmin=0, vmax=janela.d_km.quantile(0.98),
                legend_kwds={"label": "distância pela rua até o PA mais próximo (km)", "shrink": 0.6})
    vis = pa.cx[centro.x - meia:centro.x + meia, centro.y - meia:centro.y + meia]
    vis.plot(ax=ax, color=LARANJA, markersize=200, edgecolor="white", linewidth=2, marker="P", zorder=4)
    for _, r in vis.iterrows():
        ax.annotate(r.NO_FANTASIA.title(), (r.geometry.x, r.geometry.y), xytext=(8, 8), textcoords="offset points",
                    fontsize=8.5, color=TEXTO)
    ax.set_xlim(centro.x - meia, centro.x + meia)
    ax.set_ylim(centro.y - meia, centro.y + meia)
    ax.set_axis_off()
    lado = 2 * meia / 1000
    ax.set_title(f"A 'onda' do Dijkstra: janela de {lado:.0f} km × {lado:.0f} km em {capital.split(' - ')[0]}\n"
                 "claro = perto do PA mais próximo; escuro = longe", loc="left")
    fig.savefig(FIG / f"11_onda_dijkstra_{nome}.png")
    plt.close(fig)


def media_pond(d, col="d_m"):
    return np.average(d[col], weights=d.populacao) / 1000


def fig_distancias(capital, nome, setores):
    hab = setores[(setores.populacao > 0)].copy()
    hab["d_km"] = hab.d_m / 1000
    fig = plt.figure(figsize=(14, 11))
    grade = fig.add_gridspec(2, 2)
    a = fig.add_subplot(grade[0, 0])
    setores[setores.populacao.fillna(0) == 0].plot(ax=a, color=NEUTRO, linewidth=0)
    hab.plot(ax=a, column="d_km", cmap=CMAP_AZUL, linewidth=0, legend=True,
             legend_kwds={"label": "km até o PA mais próximo", "shrink": 0.7})
    setores.dissolve("CO_CNES").boundary.plot(ax=a, color=TEXTO, linewidth=0.5)
    a.set_axis_off()
    a.set_title("(a) Distância por setor e áreas de atendimento")

    b = fig.add_subplot(grade[0, 1])
    b.hist(hab.d_km, bins=np.arange(0, hab.d_km.max() + 0.25, 0.25), weights=hab.populacao / 1000, color=AZUL)
    media = media_pond(hab)
    b.axvline(media, color=LARANJA, linewidth=2)
    b.text(media + 0.1, b.get_ylim()[1] * 0.92, f"média ponderada\n{media:.2f} km", color=TEXTO_2, fontsize=8.5)
    b.set_xlabel("distância pela rua até o PA mais próximo (km)")
    b.set_ylabel("população (mil pessoas)")
    b.set_title("(b) Quantas pessoas estão a cada distância")

    c = fig.add_subplot(grade[1, 0])
    hab["q_renda"] = pd.qcut(hab.renda_media, 4, labels=["Q1 (menor renda)", "Q2", "Q3", "Q4 (maior renda)"])
    cores = {"Q1 (menor renda)": LARANJA, "Q4 (maior renda)": AZUL}
    for q, d in hab.groupby("q_renda", observed=True):
        if q not in cores:
            continue
        x = np.sort(d.d_km.to_numpy())
        w = d.populacao.to_numpy()[np.argsort(d.d_km.to_numpy())]
        cauda = np.cumsum(w[::-1])[::-1] / w.sum()
        c.loglog(x, cauda, color=cores[q], label=f"{q}: média {media_pond(d):.2f} km")
    c.set_xlabel("distância, x (km)")
    c.set_ylabel("P(distância ≥ x), ponderada pela população")
    c.set_title("(c) Distribuição acumulada complementar por renda")
    c.legend(loc="lower left")

    dd = fig.add_subplot(grade[1, 1])
    hab["q_dens"] = pd.qcut(hab.densidade, 4, labels=["Q1", "Q2", "Q3", "Q4"])
    tabela = hab.groupby(["q_dens", "q_renda"], observed=True).apply(
        lambda d: np.average(d.d_m, weights=d.populacao) / (media * 1000), include_groups=False).unstack()
    tabela = tabela.iloc[::-1]
    im = dd.imshow(tabela.to_numpy(), cmap=CMAP_AZUL, vmin=0.5, vmax=1.6)
    for i in range(tabela.shape[0]):
        for j in range(tabela.shape[1]):
            v = tabela.iat[i, j]
            dd.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=10,
                    color="white" if v > 1.15 else TEXTO)
    dd.set_xticks(range(4), ["Q1\nmenor renda", "Q2", "Q3", "Q4\nmaior renda"])
    dd.set_yticks(range(4), ["Q4 mais denso", "Q3", "Q2", "Q1 menos denso"])
    dd.grid(False)
    fig.colorbar(im, ax=dd, label="distância média / média da cidade", shrink=0.8)
    dd.set_title("(d) Prévia da tabela densidade × renda (seção 6.1)")
    fig.suptitle(f"{capital}: resultado do Dijkstra", x=0.01, ha="left", fontsize=11, color=TEXTO_2)
    fig.tight_layout()
    fig.savefig(FIG / f"12_distancias_{nome}.png")
    plt.close(fig)
    print("Tabela densidade × renda (distância / média da cidade):\n" + tabela.round(2).to_string())
    print(f"Distância média por quartil de renda (km):\n"
          + hab.groupby("q_renda", observed=True).apply(media_pond, include_groups=False).round(2).to_string())
    print(f"Distância média por quartil de densidade (km):\n"
          + hab.groupby("q_dens", observed=True).apply(media_pond, include_groups=False).round(2).to_string())
    print(f"Favela: {media_pond(hab[hab.favela]):.2f} km; fora de favela: {media_pond(hab[~hab.favela]):.2f} km")


def main():
    capital = sys.argv[1] if len(sys.argv) > 1 else "Fortaleza - CE"
    estilo.aplicar()
    nome, G, setores, pa = carregar(capital)
    fig_rede(capital, nome, G, setores, pa)
    fig_onda(capital, nome, G, pa)
    fig_distancias(capital, nome, setores)


if __name__ == "__main__":
    main()
