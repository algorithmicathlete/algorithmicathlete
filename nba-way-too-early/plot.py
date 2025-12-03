import numpy as np
from matplotlib import image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.pyplot as plt
from utils import *

def ft_differential(df):
    fig, ax = plt.subplots(figsize=(12,6))
    fig.set_facecolor("#191919")
    ax.set_facecolor("#191919")

    ax.bar(df["TEAM_NAME"], df["FT_DIFF"], color=[nba_team_colors[nba_team_map[x]] for x in df["TEAM_NAME"]])
    ax.axhline(0, color='white', lw=0.5)

    for i, txt in enumerate(df["TEAM_NAME"]):
        top = df["FT_DIFF"].iloc[i] > 0

        ax.annotate(round(df["FT_DIFF"].iloc[i], 1), (i, df["FT_DIFF"].iloc[i]+(0.05 if top else -0.1)), ha="center", va="bottom" if top else "top", fontsize=11, color="white")

        path = f"logos/{nba_team_map[txt]}.png"
        logo = mpimg.imread(path)
        imagebox = OffsetImage(logo, zoom=0.29)
        ab = AnnotationBbox(imagebox, (i, -0.45 if top else 0.47), frameon=False)
        plt.gca().add_artist(ab)

    for spine in ax.spines.values():
        spine.set_color("#191919")

    plt.xticks([])
    plt.yticks([])

    ax.set_title("Free Throw Differential Per Game", fontweight='bold', fontsize=16, color="#CCCCCC")
    plt.tight_layout()
    plt.savefig("nbafreethrowdiff2.png", dpi=350)

def ft_win_pct(df):
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.set_facecolor("#101010")
    ax.set_facecolor("#191919")

    plt.scatter(df["FT_DIFF"], df["W_PCT"], alpha=0.1)
    for i, txt in enumerate(df["TEAM_NAME"]):
        path = f"logos/{nba_team_map[txt]}.png"
        logo = mpimg.imread(path)
        imagebox = OffsetImage(logo, zoom=0.35)
        ab = AnnotationBbox(imagebox, (df["FT_DIFF"].iloc[i], df["W_PCT"].iloc[i]), frameon=False)
        plt.gca().add_artist(ab)

    for spine in ax.spines.values():
        spine.set_color("#888888")

    ax.set_ylabel("Win %", color="#CCCCCC", fontsize=12)
    ax.set_xlabel("FT Diff Per Game", color="#CCCCCC", fontsize=12)
    x = df["FT_DIFF"]
    y = df["W_PCT"]

    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m * x + b, linewidth=1, alpha=0.4, color="white", linestyle="--")
    plt.tick_params(axis='x', colors='white')
    plt.tick_params(axis='y', colors='white')
    r = np.corrcoef(x, y)[0, 1]
    print("r =", r)

    plt.tight_layout()
    plt.savefig("nbaftdiffwinpct.png", dpi=350)