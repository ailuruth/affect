"""Shared figure style for toy-simulation figures (reference palette from the dataviz skill, light mode)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
SURF, TXT, TXT2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"   # categorical slots 1-3 (validated all-pairs)
def setup():
    plt.rcParams.update({"figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
        "axes.edgecolor": TXT2, "axes.labelcolor": TXT, "xtick.color": TXT2, "ytick.color": TXT2, "text.color": TXT,
        "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False,
        "lines.linewidth": 2, "lines.markersize": 7, "font.size": 10, "legend.frameon": False, "figure.dpi": 150})
def save(fig, path):
    fig.tight_layout(); fig.savefig(path); plt.close(fig)
