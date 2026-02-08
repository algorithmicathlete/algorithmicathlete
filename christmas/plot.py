import numpy as np
from matplotlib import pyplot as plt, image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

from colors import nba_team_colors, nba_team_map

records = {
    'Washington Wizards': {'wins': 19, 'losses': 10},
    'New York Knicks': {'wins': 26, 'losses': 32},
    'Golden State Warriors': {'wins': 16, 'losses': 19},
    'Boston Celtics': {'wins': 17, 'losses': 21},
    'Detroit Pistons': {'wins': 10, 'losses': 22},
    'Sacramento Kings': {'wins': 18, 'losses': 11},
    'Philadelphia 76ers': {'wins': 20, 'losses': 15},
    'Los Angeles Lakers': {'wins': 25, 'losses': 26},
    'Atlanta Hawks': {'wins': 9, 'losses': 12},
    'Chicago Bulls': {'wins': 13, 'losses': 8},
    'Oklahoma City Thunder': {'wins': 6, 'losses': 15},
    'Houston Rockets': {'wins': 6, 'losses': 6},
    'Milwaukee Bucks': {'wins': 5, 'losses': 5},
    'Phoenix Suns': {'wins': 13, 'losses': 9},
    'Cleveland Cavaliers': {'wins': 7, 'losses': 8},
    'Portland Trail Blazers': {'wins': 14, 'losses': 4},
    'Utah Jazz': {'wins': 6, 'losses': 2},
    'San Antonio Spurs': {'wins': 6, 'losses': 7},
    'LA Clippers': {'wins': 7, 'losses': 6},
    'Denver Nuggets': {'wins': 3, 'losses': 7},
    'Brooklyn Nets': {'wins': 6, 'losses': 5},
    'Indiana Pacers': {'wins': 2, 'losses': 2},
    'Orlando Magic': {'wins': 5, 'losses': 4},
    'Miami Heat': {'wins': 12, 'losses': 2},
    'Toronto Raptors': {'wins': 0, 'losses': 2},
    'Dallas Mavericks': {'wins': 4, 'losses': 5},
    'New Orleans Pelicans': {'wins': 1, 'losses': 3},
    'Minnesota Timberwolves': {'wins': 2, 'losses': 1},
    'Memphis Grizzlies': {'wins': 0, 'losses': 1}
}

import pandas as pd

df = (
    pd.DataFrame.from_dict(records, orient="index")
      .reset_index()
      .rename(columns={
          "index": "NAME",
          "wins": "WINS",
          "losses": "LOSSES"
      })
)
df["GP"] = df["WINS"] + df["LOSSES"]
df["W_PCT"] = df["WINS"] / (df["WINS"] + df["LOSSES"])

print(df
      )
def christmas_win_pct(df):
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.set_facecolor("#000000")
    ax.set_facecolor("#191919")

    ax.scatter(df["GP"], df["W_PCT"], alpha=0.1)

    ax.axhline(np.median(df["W_PCT"]), color='gray', linestyle='--', linewidth=1, alpha=0.7, zorder=1)
    ax.axvline(np.median(df["GP"]), color='gray', linestyle='--', linewidth=1, alpha=0.7, zorder=1)


    for i, txt in enumerate(df["NAME"]):
        path = f"../nba_logos/{nba_team_map[txt]}.png"
        logo = mpimg.imread(path)
        imagebox = OffsetImage(logo, zoom=0.35)
        ab = AnnotationBbox(imagebox, (df["GP"].iloc[i], df["W_PCT"].iloc[i]), frameon=False)
        plt.gca().add_artist(ab)

    for spine in ax.spines.values():
        spine.set_color("#888888")

    ax.set_ylabel("Win %", color="#CCCCCC", fontsize=12)
    ax.set_xlabel("Christmas Games", color="#CCCCCC", fontsize=12)

    plt.tick_params(axis='x', colors='white')
    plt.tick_params(axis='y', colors='white')

    plt.tight_layout()
    # plt.show()
    plt.savefig("christmaswinpct.png", dpi=350)

def christmas_wins(df):
    fig, ax = plt.subplots(figsize=(12,6))
    fig.set_facecolor("#191919")
    ax.set_facecolor("#191919")

    ax.bar(df["NAME"], df["WINS"], color=[nba_team_colors[nba_team_map[x]] for x in df["NAME"]])

    for i, txt in enumerate(df["NAME"]):
        ax.annotate(round(df["WINS"].iloc[i], 1), (i, df["WINS"].iloc[i]+0.05), ha="center", va="bottom", fontsize=11, color="white")

        path = f"../nba_logos/{nba_team_map[txt]}.png"
        logo = mpimg.imread(path)
        imagebox = OffsetImage(logo, zoom=0.29)
        ab = AnnotationBbox(imagebox, (i, -0.85), frameon=False)
        plt.gca().add_artist(ab)

    for spine in ax.spines.values():
        spine.set_color("#191919")

    plt.xticks([])
    plt.yticks([])

    ax.set_ylim(bottom=-1)

    ax.set_title("Wins on Christmas Day", fontweight='bold', fontsize=16, color="white")
    plt.tight_layout()
    plt.savefig("christmaswins.png", dpi=350)
    # plt.show()

df = df.sort_values("WINS", ascending=False)

christmas_wins(df)
christmas_win_pct(df)