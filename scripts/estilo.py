"""Cores e estilo comuns a todas as figuras (paleta de referência do guia de visualização)."""
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap

SUPERFICIE = "#fcfcfb"
TEXTO = "#0b0b0b"
TEXTO_2 = "#52514e"
GRADE = "#e1e0d9"
NEUTRO = "#e4e2dd"   # setores sem população / fundo de mapa

AZUL = "#2a78d6"     # série 1
LARANJA = "#eb6834"  # série 2
VERDE_AGUA = "#1baf7a"  # série 3

# Sequencial (magnitude): um tom, claro -> escuro
RAMPA_AZUL = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
RAMPA_LARANJA = ["#fde3d6", "#f9bfa2", "#f4966d", "#eb6834", "#c94f1f", "#9c3c15", "#6e2a0e"]
CMAP_AZUL = LinearSegmentedColormap.from_list("azul", RAMPA_AZUL)
CMAP_LARANJA = LinearSegmentedColormap.from_list("laranja", RAMPA_LARANJA)


def aplicar():
    mpl.rcParams.update({
        "figure.facecolor": SUPERFICIE, "axes.facecolor": SUPERFICIE, "savefig.facecolor": SUPERFICIE,
        "text.color": TEXTO, "axes.labelcolor": TEXTO_2, "xtick.color": TEXTO_2, "ytick.color": TEXTO_2,
        "axes.edgecolor": GRADE, "axes.grid": True, "grid.color": GRADE, "grid.linewidth": 0.6,
        "axes.spines.top": False, "axes.spines.right": False, "axes.titlesize": 11,
        "axes.titleweight": "bold", "axes.titlelocation": "left", "font.size": 9.5,
        "legend.frameon": False, "lines.linewidth": 2, "savefig.dpi": 150, "savefig.bbox": "tight",
    })
