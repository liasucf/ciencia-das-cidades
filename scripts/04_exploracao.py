"""Análise exploratória: figuras para entender os dados antes das análises principais.

Uso: .venv/bin/python scripts/04_exploracao.py
Saídas em figuras/exploracao/. As explicações de cada figura estão em exploracao.md.
"""
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LogNorm
from scipy import stats

import estilo
from estilo import AZUL, LARANJA, NEUTRO, TEXTO_2, CMAP_AZUL, CMAP_LARANJA

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "dados/processados"
FIG = ROOT / "figuras/exploracao"
LIMIAR_DENSIDADE = 1500
SALARIO_MINIMO_2022 = 1212
RNG = np.random.default_rng(42)


def ccdf(valores, pesos=None):
    """P(X >= x) ponderada; devolve x ordenado e a fração acumulada a partir do topo."""
    valores = np.asarray(valores, float)
    pesos = np.ones_like(valores) if pesos is None else np.asarray(pesos, float)
    ordem = np.argsort(valores)
    x, w = valores[ordem], pesos[ordem]
    cauda = np.cumsum(w[::-1])[::-1] / w.sum()
    return x, cauda


def nome_curto(municipio):
    return municipio.split(" - ")[0]


def fig_pa_por_capital(cap):
    cap = cap.sort_values("populacao_2022")
    cap["por_100mil"] = cap.n_pa / cap.populacao_2022 * 1e5
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 7.5), sharey=True)
    y = np.arange(len(cap))
    a.barh(y, cap.n_pa, color=AZUL, height=0.7)
    a.set_yticks(y, [f"{nome_curto(m)} ({p / 1e6:.1f} mi)" for m, p in zip(cap.municipio, cap.populacao_2022)])
    a.set_title("(a) Pronto-atendimentos por capital")
    a.set_xlabel("número de unidades (tipo 73 do CNES)")
    for yi, n in zip(y, cap.n_pa):
        a.text(n + 0.6, yi, str(n), va="center", fontsize=8, color=TEXTO_2)
    b.barh(y, cap.por_100mil, color=AZUL, height=0.7)
    b.set_title("(b) Por 100 mil habitantes")
    b.set_xlabel("unidades por 100 mil habitantes")
    for yi, v in zip(y, cap.por_100mil):
        b.text(v + 0.02, yi, f"{v:.2f}", va="center", fontsize=8, color=TEXTO_2)
    for ax in (a, b):
        ax.grid(axis="y", visible=False)
    fig.suptitle("Capitais ordenadas pela população (Censo 2022)", x=0.01, ha="left", fontsize=10, color=TEXTO_2)
    fig.savefig(FIG / "01_pa_por_capital.png")
    plt.close(fig)


def ajuste_loglog(x, y, n_boot=2000):
    lx, ly = np.log10(x), np.log10(y)
    beta, logA = np.polyfit(lx, ly, 1)
    boot = []
    for _ in range(n_boot):
        i = RNG.integers(0, len(lx), len(lx))
        if np.ptp(lx[i]) > 0:
            boot.append(np.polyfit(lx[i], ly[i], 1)[0])
    return beta, logA, np.percentile(boot, [2.5, 97.5])


def fig_lei_escala_previa(cap):
    usa = cap[cap.n_pa > 0]
    beta, logA, ic = ajuste_loglog(usa.populacao_2022.to_numpy(), usa.n_pa.to_numpy())
    fig, ax = plt.subplots(figsize=(7, 5.5))
    ax.scatter(usa.populacao_2022, usa.n_pa, s=46, color=AZUL, edgecolor="white", linewidth=1.2, zorder=3)
    xs = np.logspace(np.log10(usa.populacao_2022.min()) - 0.05, np.log10(usa.populacao_2022.max()) + 0.05, 50)
    ax.plot(xs, 10 ** logA * xs ** beta, color=LARANJA, label=f"ajuste: β = {beta:.2f} (IC 95% {ic[0]:.2f}–{ic[1]:.2f})")
    # Referência β = 1 passando pelo ponto médio dos dados
    meio = 10 ** np.mean(np.log10(usa.populacao_2022)), 10 ** np.mean(np.log10(usa.n_pa))
    ax.plot(xs, meio[1] * (xs / meio[0]), color=TEXTO_2, linestyle="--", linewidth=1.2, label="referência β = 1")
    for _, r in usa.iterrows():
        if r.municipio.split(" - ")[0] in {"São Paulo", "Rio de Janeiro", "Boa Vista", "Palmas", "Manaus",
                                          "Porto Alegre", "Salvador", "Vitória", "Campo Grande"}:
            ax.annotate(nome_curto(r.municipio), (r.populacao_2022, r.n_pa), xytext=(5, -3),
                        textcoords="offset points", fontsize=8, color=TEXTO_2)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("população (Censo 2022)")
    ax.set_ylabel("número de pronto-atendimentos")
    ax.set_title("Prévia de L1: unidades × população nas capitais")
    ax.legend(loc="upper left")
    ax.text(0.99, 0.02, f"{len(usa)} capitais; Aracaju (0 unidades) fora do log", transform=ax.transAxes,
            ha="right", fontsize=8, color=TEXTO_2)
    fig.savefig(FIG / "02_lei_escala_previa.png")
    plt.close(fig)
    return beta, ic


def fig_renda(hab):
    com_renda = hab[hab.renda_media.notna()]
    fig, axs = plt.subplots(1, 3, figsize=(14, 4.4))
    a, b, c = axs
    bins = np.logspace(np.log10(200), np.log10(60000), 60)
    a.hist(com_renda.renda_media, bins=bins, weights=com_renda.populacao / 1e6, color=AZUL)
    a.set_xscale("log")
    a.set_xlabel("renda média do responsável no setor (R$, escala log)")
    a.set_ylabel("população (milhões)")
    a.set_title("(a) Renda média dos setores")
    a.axvline(SALARIO_MINIMO_2022, color=TEXTO_2, linestyle="--", linewidth=1)
    a.text(SALARIO_MINIMO_2022 / 1.08, a.get_ylim()[1] * 0.92, "salário mínimo\n2022", fontsize=8,
           color=TEXTO_2, ha="right")

    x, cauda = ccdf(com_renda.renda_media, com_renda.populacao)
    b.loglog(x, cauda, color=AZUL)
    b.set_xlabel("renda média do setor, x (R$)")
    b.set_ylabel("P(renda ≥ x), ponderada pela população")
    b.set_title("(b) Distribuição acumulada complementar")

    med = hab.renda_mediana.dropna()
    c.hist(med, bins=np.arange(0, 8000, 100), color=LARANJA)
    c.set_xlabel("renda MEDIANA do setor (R$)")
    c.set_ylabel("número de setores")
    c.set_title("(c) A mediana se acumula no salário mínimo")
    frac = (med == SALARIO_MINIMO_2022).mean()
    c.text(0.97, 0.9, f"{frac:.0%} dos setores têm\nmediana = R$ 1.212", transform=c.transAxes, ha="right",
           fontsize=8.5, color=TEXTO_2)
    fig.tight_layout()
    fig.savefig(FIG / "03_renda_distribuicao.png")
    plt.close(fig)


def fig_renda_por_capital(hab):
    d = hab[hab.renda_media.notna()]
    ordem = d.groupby("NM_MUN").renda_media.median().sort_values().index
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.boxplot([d.loc[d.NM_MUN == m, "renda_media"] for m in ordem], orientation="horizontal",
               showfliers=False, widths=0.6, patch_artist=True,
               boxprops={"facecolor": "#cde2fb", "edgecolor": AZUL}, medianprops={"color": AZUL, "linewidth": 2},
               whiskerprops={"color": TEXTO_2}, capprops={"color": TEXTO_2})
    ax.set_yticks(range(1, len(ordem) + 1), ordem)
    ax.set_xscale("log")
    ax.set_xlabel("renda média do responsável por setor (R$, escala log)")
    ax.set_title("Renda média dos setores em cada capital")
    ax.text(0.99, 0.01, "caixa = 50% central dos setores; traço = mediana; hastes até 1,5× o intervalo interquartil",
            transform=ax.transAxes, ha="right", fontsize=7.5, color=TEXTO_2)
    ax.grid(axis="y", visible=False)
    fig.savefig(FIG / "04_renda_por_capital.png")
    plt.close(fig)


def fig_densidade(hab):
    d = hab[np.isfinite(hab.densidade) & (hab.densidade > 0)]
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 4.4))
    bins = np.logspace(0, 6, 70)
    a.hist(d.densidade, bins=bins, weights=d.populacao / 1e6, color=AZUL)
    a.set_xscale("log")
    a.axvline(LIMIAR_DENSIDADE, color=TEXTO_2, linestyle="--", linewidth=1)
    a.text(LIMIAR_DENSIDADE * 1.15, a.get_ylim()[1] * 0.92, "1.500 hab/km²\n(Aula 5)", fontsize=8, color=TEXTO_2)
    a.set_xlabel("densidade do setor (hab/km², escala log)")
    a.set_ylabel("população (milhões)")
    a.set_title("(a) Em que densidade as pessoas moram")
    x, cauda = ccdf(d.densidade, d.populacao)
    b.loglog(x, cauda, color=AZUL)
    b.set_xlabel("densidade do setor, x (hab/km²)")
    b.set_ylabel("P(densidade ≥ x), ponderada pela população")
    b.set_title("(b) Distribuição acumulada complementar")
    fig.tight_layout()
    fig.savefig(FIG / "05_densidade_distribuicao.png")
    plt.close(fig)


def fig_densidade_vs_renda(hab):
    d = hab[hab.renda_media.notna() & np.isfinite(hab.densidade) & (hab.densidade > 0)]
    rho, _ = stats.spearmanr(d.densidade, d.renda_media)
    por_capital = d.groupby("NM_MUN").apply(
        lambda g: stats.spearmanr(g.densidade, g.renda_media)[0], include_groups=False)
    fig, (a, b) = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={"width_ratios": [1.1, 1]})
    hb = a.hexbin(d.densidade, d.renda_media, xscale="log", yscale="log", gridsize=55, cmap=CMAP_AZUL,
                  mincnt=1, bins="log", linewidths=0)
    fig.colorbar(hb, ax=a, label="número de setores (escala log)")
    a.set_xlabel("densidade do setor (hab/km²)")
    a.set_ylabel("renda média do setor (R$)")
    a.set_title(f"(a) Densidade × renda, 27 capitais (Spearman = {rho:.2f})")
    a.grid(False)
    por_capital = por_capital.sort_values()
    b.barh(range(len(por_capital)), por_capital, color=[LARANJA if v < 0 else AZUL for v in por_capital], height=0.7)
    b.set_yticks(range(len(por_capital)), por_capital.index, fontsize=8)
    b.axvline(0, color=TEXTO_2, linewidth=0.8)
    b.set_xlabel("correlação de Spearman entre densidade e renda")
    b.set_title("(b) Dentro de cada capital")
    b.grid(axis="y", visible=False)
    fig.tight_layout()
    fig.savefig(FIG / "06_densidade_vs_renda.png")
    plt.close(fig)
    return rho, por_capital


def fig_favela(resumo_setores):
    r = resumo_setores.sort_values("pct_pop_favela")
    fig, ax = plt.subplots(figsize=(7, 7.5))
    ax.barh(range(len(r)), r.pct_pop_favela, color=LARANJA, height=0.7)
    ax.set_yticks(range(len(r)), r.index)
    for i, v in enumerate(r.pct_pop_favela):
        ax.text(v + 0.6, i, f"{v:.1f}%", va="center", fontsize=8, color=TEXTO_2)
    ax.set_xlabel("% da população em setores de Favela e Comunidade Urbana (IBGE)")
    ax.set_title("População em favelas e comunidades urbanas")
    ax.grid(axis="y", visible=False)
    fig.savefig(FIG / "07_favela_por_capital.png")
    plt.close(fig)


def fig_mapas_capital(capital, uf, cd_mun, pa):
    gpkg = ROOT / f"dados/ibge/setores_gpkg/{uf}_setores_CD2022.gpkg"
    s = gpd.read_file(gpkg, where=f"CD_MUN='{cd_mun}'", columns=["CD_SETOR", "CD_SIT", "CD_TIPO"])
    s = s[s.CD_SIT != "9"]
    atrib = pd.read_csv(PROC / "setores_capitais.csv", dtype={"CD_SETOR": str},
                        usecols=["CD_SETOR", "populacao", "densidade", "renda_media"])
    s = s.merge(atrib, on="CD_SETOR")
    s = s.to_crs(s.estimate_utm_crs())
    pa_c = pa[pa.municipio == capital]
    pts = gpd.GeoDataFrame(pa_c, geometry=gpd.points_from_xy(pa_c.lon, pa_c.lat), crs="EPSG:4326").to_crs(s.crs)
    hab = s[s.populacao > 0]
    vazio = s[s.populacao.fillna(0) == 0]

    fig, axs = plt.subplots(2, 2, figsize=(12, 11.5))
    (a, b), (c, d) = axs
    for ax in axs.flat:
        vazio.plot(ax=ax, color=NEUTRO, linewidth=0)
        ax.set_axis_off()
    dens = hab.densidade.clip(lower=100)
    hab.assign(dens=dens).plot(ax=a, column="dens", cmap=CMAP_AZUL, linewidth=0, legend=True,
                               norm=LogNorm(vmin=100, vmax=dens.quantile(0.99)),
                               legend_kwds={"label": "hab/km² (escala log)", "shrink": 0.6})
    a.set_title("(a) Densidade populacional por setor")
    r = hab[hab.renda_media.notna()]
    r.plot(ax=b, column="renda_media", cmap=CMAP_LARANJA, linewidth=0, legend=True,
           norm=LogNorm(vmin=r.renda_media.quantile(0.01), vmax=r.renda_media.quantile(0.99)),
           legend_kwds={"label": "renda média do responsável (R$, escala log)", "shrink": 0.6})
    b.set_title("(b) Renda média por setor")
    hab.plot(ax=c, color="#e9e7e2", linewidth=0)
    hab[hab.CD_TIPO == "1"].plot(ax=c, color=LARANJA, linewidth=0)
    c.set_title("(c) Setores de favela e comunidade urbana (laranja)")
    hab.assign(dens=dens).plot(ax=d, column="dens", cmap=CMAP_AZUL, linewidth=0, alpha=0.55,
                               norm=LogNorm(vmin=100, vmax=dens.quantile(0.99)))
    pts.plot(ax=d, color=LARANJA, markersize=70, edgecolor="white", linewidth=1.5, zorder=3)
    d.set_title(f"(d) Os {len(pts)} pronto-atendimentos sobre a densidade")
    fig.suptitle(f"{capital}: setores censitários do Censo 2022 (cinza = sem moradores)", x=0.01, ha="left",
                 fontsize=10, color=TEXTO_2)
    fig.tight_layout()
    nome = capital.split(" - ")[0].lower().replace(" ", "_")
    fig.savefig(FIG / f"08_mapas_{nome}.png")
    plt.close(fig)


def main():
    estilo.aplicar()
    FIG.mkdir(parents=True, exist_ok=True)
    cap = pd.read_csv(PROC / "capitais_resumo.csv", dtype={"co_ibge7": str})
    setores = pd.read_csv(PROC / "setores_capitais.csv", dtype={"CD_SETOR": str, "CD_MUN": str, "CD_TIPO": str})
    hab = setores[setores.populacao > 0]
    resumo_setores = pd.read_csv(PROC / "setores_capitais_resumo.csv", index_col=0)
    pa = pd.read_csv(PROC / "pa_capitais_corrigido.csv")

    fig_pa_por_capital(cap)
    beta, ic = fig_lei_escala_previa(cap)
    fig_renda(hab)
    fig_renda_por_capital(hab)
    fig_densidade(hab)
    rho, por_capital = fig_densidade_vs_renda(hab)
    fig_favela(resumo_setores)
    fig_mapas_capital("Fortaleza - CE", "CE", "2304400", pa)

    print(f"Prévia L1: β = {beta:.3f}, IC 95% bootstrap [{ic[0]:.3f}, {ic[1]:.3f}]")
    print(f"Spearman densidade × renda (todas): {rho:.3f}")
    print("Spearman por capital:\n" + por_capital.round(2).to_string())
    print(f"Renda média dos setores (ponderada pela população): "
          f"mediana R$ {hab.renda_media.median():.0f}; P10 R$ {hab.renda_media.quantile(.1):.0f}; "
          f"P90 R$ {hab.renda_media.quantile(.9):.0f}")
    print(f"Setores com mediana = R$ 1.212: {(hab.renda_mediana == SALARIO_MINIMO_2022).mean():.1%}")
    print(f"População em setores abaixo de 1.500 hab/km²: "
          f"{hab.populacao[hab.densidade < LIMIAR_DENSIDADE].sum() / hab.populacao.sum():.1%}")


if __name__ == "__main__":
    main()
