import numpy as np
from matplotlib import pyplot as plt, image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

from colors import nfl_team_colors


def gl_score_rate_bar(df):
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.set_facecolor("#000000")
    ax.set_facecolor("#111111")

    ax.bar(df["posteam"], df["gl_td_pct"]-77, color=[nfl_team_colors[x] for x in df["posteam"]])
    ax.axhline(0, color='white', lw=0.5)

    for i, txt in enumerate(df["posteam"]):
        top = df["gl_td_pct"].iloc[i] > 77

        ax.annotate(("+" if top else "")+str(int(df["gl_td_pct"].iloc[i])-77), (i, df["gl_td_pct"].iloc[i]-77 + (0.2 if top else -0.2)),  ha="center", va="bottom" if top else "top",
                    fontsize=9, color="white")

        path = f"../nfl_logos/{'lar' if txt.lower() == 'la' else txt.lower()}.png"
        logo = mpimg.imread(path)
        imagebox = OffsetImage(logo, zoom=0.28)
        ab = AnnotationBbox(imagebox, (i, 0), frameon=False,  box_alignment=(0.5, 1 if top else 0))
        plt.gca().add_artist(ab)


    for i, spine in enumerate(ax.spines.values()):
        spine.set_color("#CCCCCC")

    plt.title("Goal Line TD% Over Expected", fontweight="bold", fontsize=16, color="white")
    # plt.ylim(bottom=-3)
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()

    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    plt.savefig("goallinetdoe.png", dpi=350)

def epa_scatter(df):
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.set_facecolor("#000000")
    ax.set_facecolor("#111111")
    df["def_gl_epa"] = -df["def_gl_epa"]

    ax.scatter(df["gl_epa"], df["def_gl_epa"], alpha=0)

    ax.axvline(0, color='white', linestyle="--", lw=1, alpha=0.5)
    ax.axhline(0, color='white', linestyle="--", lw=1, alpha=0.5)

    for i, txt in enumerate(df["team"]):
        path = f"../nfl_logos/{'lar' if txt.lower() == 'la' else txt.lower()}.png"
        logo = mpimg.imread(path)
        imagebox = OffsetImage(logo, zoom=0.4)
        ab = AnnotationBbox(imagebox, (df["gl_epa"].iloc[i], df["def_gl_epa"].iloc[i]), frameon=False)
        plt.gca().add_artist(ab)

    for i, spine in enumerate(ax.spines.values()):
        spine.set_color("#CCCCCC")

    plt.title("NFL Goal Line EPA", color="white", alpha=0.8, fontsize=14, fontweight="bold")


    ax.set_xlabel("Offensive Goal Line EPA/Play", fontsize=14, color="#cccccc")
    ax.set_ylabel("Defensive Goal Line EPA/Play (Inverted)", fontsize=14, color="#cccccc") # maybe invert?

    plt.tick_params(axis='x', colors='white')
    plt.tick_params(axis='y', colors='white')

    plt.tick_params(axis='x', colors='white')
    plt.tick_params(axis='y', colors='white')

    x = df["gl_epa"]
    y = df["def_gl_epa"]
    r = np.corrcoef(x, y)[0, 1]
    print("r =", r)


    plt.tight_layout()
    plt.savefig("glepa.png", dpi=350)



import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image

_logo_cache = {}
def get_logo(team):
    if team not in _logo_cache:
        _logo_cache[team] = Image.open(f"../nfl_logos/{'lar' if team.lower() == 'la' else team.lower()}.png")
    return _logo_cache[team]

def beeswarm(df, metric="def_total_to"):
    df_plot = df[["team", metric]].dropna().sort_values(metric).copy()
    df_plot["col"] = ""  # single swarm column

    fig, ax = plt.subplots(figsize=(5, 6))
    fig.set_facecolor("#000000")
    ax.set_facecolor("#000000")

    sns.swarmplot(data=df_plot, x="col", y=metric, size=0, ax=ax)

    points = ax.collections[0].get_offsets()

    total_length = {x:df[df[metric] == x].shape[0] for x in range(0,4)}
    counts = {x:0 for x in range(0, 4)}

    for i, (_, row) in enumerate(df_plot.iterrows()):
        x, y = points[i]
        if int(y) > 0:
            x = 0.085 * (counts[int(y)] + 0.5 - total_length[int(y)] / 2)
        else:
            x = (0.085 * ((counts[int(y)] % 9) + 0.5 - total_length[int(y)] / 4))

        img = get_logo(row["team"])
        ab = AnnotationBbox(
            OffsetImage(img, zoom=0.3),  # tweak zoom
            (x, y+(0.1 if int(y) == 0 and counts[int(y)] >= (9 if metric.startswith("def") else 8) else -0.1 if int(y) == 0 else 0)),
            frameon=False
        )
        counts[int(y)] += 1
        ax.add_artist(ab)

    ax.set_xlim(-0.5, 0.5)
    ax.set_xlabel("")
    ax.set_xticks([])
    ax.set_yticks([0,1,2,3])
    ax.set_ylabel("")

    ax.set_title(f"Goal Line {'Takeaways' if metric.startswith('def') else 'Turnovers'}", color="#cccccc", fontweight="bold")

    plt.tick_params(axis='y', colors='white')
    plt.tick_params(axis='y', colors='white')

    for spine in ax.spines.values():
        spine.set_color("#ffffff")

    sns.despine(left=False, bottom=True)
    # plt.tight_layout()
    plt.savefig(f"{metric}_beeswarm2.png", dpi=350)

