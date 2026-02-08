import os

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

from colors import nfl_team_colors


def one_score_differential(df):
    fig, ax = plt.subplots(figsize=(12,6))
    ax.set_facecolor("#000000")
    fig.patch.set_facecolor("#000000")


    ax.bar(df["team"], df["one_score_win_pct"], color=[nfl_team_colors[{'WSH': 'WAS', 'LAR': 'LA'}.get(x, x)] for x in df["team"]])
    ax.axhline(0, color='white', lw=0.5)

    for i, txt in enumerate(df["team"]):
        top = df["one_score_win_pct"].iloc[i] > 0

        # ax.annotate(round(df["diff"].iloc[i], 1), (i, df["diff"].iloc[i]+(0.05 if top else -0.1)), ha="center", va="bottom" if top else "top", fontsize=11, color="white")
        ax.annotate(
            f"{df['one_score_wins'].iloc[i]}-{df['one_score_losses'].iloc[i]}{'-1' if df['ties'].iloc[i] > 0 else ''}",
            (i, df["one_score_win_pct"].iloc[i]+(0.005 if top else -0.005)),
            ha="center", va="bottom" if top else "top",
            fontsize=10 if df['ties'].iloc[i] == 0 else 8, color="white"
        )


        name = {'WSH': 'WAS'}.get(txt)
        path = f"../nfl_logos/{name or txt}.png"
        logo = mpimg.imread(path)
        imagebox = OffsetImage(logo, zoom=0.29)
        ab = AnnotationBbox(imagebox, (i, -0.025 if top else 0.025), frameon=False)
        plt.gca().add_artist(ab)

    for spine in ax.spines.values():
        spine.set_color("#000000")

    plt.xticks([])
    plt.yticks([])

    ax.set_title("NFL Teams' Records in One-Score Games", fontweight='bold', fontsize=16, color="#CCCCCC")
    plt.tight_layout()
    # plt.show()
    plt.savefig("onescoregamebar.png", dpi=350)

records = {'PHI': {'wins': 7, 'losses': 10, 'ties': 0, 'num_1score': 12, 'real_wins': 11, 'real_losses': 6, 'one_score_wins': 8, 'one_score_losses': 4}, 'DAL': {'wins': 6, 'losses': 10, 'ties': 1, 'num_1score': 7, 'real_wins': 7, 'real_losses': 9, 'one_score_wins': 4, 'one_score_losses': 3}, 'LAC': {'wins': 7, 'losses': 10, 'ties': 0, 'num_1score': 8, 'real_wins': 11, 'real_losses': 6, 'one_score_wins': 6, 'one_score_losses': 2}, 'KC': {'wins': 14, 'losses': 3, 'ties': 0, 'num_1score': 10, 'real_wins': 6, 'real_losses': 11, 'one_score_wins': 1, 'one_score_losses': 9}, 'TB': {'wins': 8, 'losses': 9, 'ties': 0, 'num_1score': 12, 'real_wins': 8, 'real_losses': 9, 'one_score_wins': 6, 'one_score_losses': 6}, 'ATL': {'wins': 8, 'losses': 9, 'ties': 0, 'num_1score': 10, 'real_wins': 8, 'real_losses': 9, 'one_score_wins': 5, 'one_score_losses': 5}, 'CIN': {'wins': 8, 'losses': 9, 'ties': 0, 'num_1score': 8, 'real_wins': 6, 'real_losses': 11, 'one_score_wins': 3, 'one_score_losses': 5}, 'CLE': {'wins': 8, 'losses': 9, 'ties': 0, 'num_1score': 9, 'real_wins': 5, 'real_losses': 12, 'one_score_wins': 3, 'one_score_losses': 6}, 'IND': {'wins': 12, 'losses': 5, 'ties': 0, 'num_1score': 10, 'real_wins': 8, 'real_losses': 9, 'one_score_wins': 3, 'one_score_losses': 7}, 'MIA': {'wins': 6, 'losses': 11, 'ties': 0, 'num_1score': 7, 'real_wins': 7, 'real_losses': 10, 'one_score_wins': 4, 'one_score_losses': 3}, 'LV': {'wins': 6, 'losses': 11, 'ties': 0, 'num_1score': 7, 'real_wins': 3, 'real_losses': 14, 'one_score_wins': 2, 'one_score_losses': 5}, 'NE': {'wins': 10, 'losses': 7, 'ties': 0, 'num_1score': 10, 'real_wins': 14, 'real_losses': 3, 'one_score_wins': 7, 'one_score_losses': 3}, 'ARI': {'wins': 9, 'losses': 8, 'ties': 0, 'num_1score': 10, 'real_wins': 3, 'real_losses': 14, 'one_score_wins': 2, 'one_score_losses': 8}, 'NO': {'wins': 8, 'losses': 9, 'ties': 0, 'num_1score': 8, 'real_wins': 6, 'real_losses': 11, 'one_score_wins': 3, 'one_score_losses': 5}, 'PIT': {'wins': 6, 'losses': 11, 'ties': 0, 'num_1score': 10, 'real_wins': 10, 'real_losses': 7, 'one_score_wins': 7, 'one_score_losses': 3}, 'NYJ': {'wins': 5, 'losses': 12, 'ties': 0, 'num_1score': 8, 'real_wins': 3, 'real_losses': 14, 'one_score_wins': 3, 'one_score_losses': 5}, 'WSH': {'wins': 8, 'losses': 9, 'ties': 0, 'num_1score': 7, 'real_wins': 5, 'real_losses': 12, 'one_score_wins': 2, 'one_score_losses': 5}, 'NYG': {'wins': 10, 'losses': 7, 'ties': 0, 'num_1score': 8, 'real_wins': 4, 'real_losses': 13, 'one_score_wins': 1, 'one_score_losses': 7}, 'JAX': {'wins': 10, 'losses': 7, 'ties': 0, 'num_1score': 9, 'real_wins': 13, 'real_losses': 4, 'one_score_wins': 6, 'one_score_losses': 3}, 'CAR': {'wins': 4, 'losses': 13, 'ties': 0, 'num_1score': 10, 'real_wins': 8, 'real_losses': 9, 'one_score_wins': 7, 'one_score_losses': 3}, 'DEN': {'wins': 5, 'losses': 12, 'ties': 0, 'num_1score': 13, 'real_wins': 14, 'real_losses': 3, 'one_score_wins': 11, 'one_score_losses': 2}, 'TEN': {'wins': 6, 'losses': 11, 'ties': 0, 'num_1score': 7, 'real_wins': 3, 'real_losses': 14, 'one_score_wins': 2, 'one_score_losses': 5}, 'SF': {'wins': 8, 'losses': 9, 'ties': 0, 'num_1score': 6, 'real_wins': 12, 'real_losses': 5, 'one_score_wins': 5, 'one_score_losses': 1}, 'SEA': {'wins': 11, 'losses': 6, 'ties': 0, 'num_1score': 9, 'real_wins': 14, 'real_losses': 3, 'one_score_wins': 6, 'one_score_losses': 3}, 'GB': {'wins': 10, 'losses': 6, 'ties': 1, 'num_1score': 9, 'real_wins': 9, 'real_losses': 7, 'one_score_wins': 4, 'one_score_losses': 5}, 'DET': {'wins': 11, 'losses': 6, 'ties': 0, 'num_1score': 8, 'real_wins': 9, 'real_losses': 8, 'one_score_wins': 3, 'one_score_losses': 5}, 'LAR': {'wins': 13, 'losses': 4, 'ties': 0, 'num_1score': 9, 'real_wins': 12, 'real_losses': 5, 'one_score_wins': 4, 'one_score_losses': 5}, 'HOU': {'wins': 10, 'losses': 7, 'ties': 0, 'num_1score': 12, 'real_wins': 12, 'real_losses': 5, 'one_score_wins': 7, 'one_score_losses': 5}, 'BUF': {'wins': 10, 'losses': 7, 'ties': 0, 'num_1score': 8, 'real_wins': 12, 'real_losses': 5, 'one_score_wins': 5, 'one_score_losses': 3}, 'BAL': {'wins': 11, 'losses': 6, 'ties': 0, 'num_1score': 7, 'real_wins': 8, 'real_losses': 9, 'one_score_wins': 2, 'one_score_losses': 5}, 'MIN': {'wins': 8, 'losses': 9, 'ties': 0, 'num_1score': 9, 'real_wins': 9, 'real_losses': 8, 'one_score_wins': 5, 'one_score_losses': 4}, 'CHI': {'wins': 8, 'losses': 9, 'ties': 0, 'num_1score': 11, 'real_wins': 11, 'real_losses': 6, 'one_score_wins': 7, 'one_score_losses': 4}}

df = (
    pd.DataFrame.from_dict(records, orient="index")
      .reset_index()
      .rename(columns={"index": "team"})
)
df["real_win_pct"] = (df["real_wins"]+0.5*df["ties"])/(df["wins"]+df["losses"]+df["ties"])
df["win_pct"] = (df["wins"]+0.5*df["ties"])/(df["wins"]+df["losses"]+df["ties"])

df["one_score_win_pct"] = (df["one_score_wins"]+0.5*df["ties"])/(df["one_score_wins"]+df["one_score_losses"]+df["ties"]) - 0.5
df["diff"] = df["real_wins"] - df["wins"]
df = df.sort_values("one_score_win_pct", ascending=False)
print(df.sort_values("win_pct", ascending=False)[["team", "wins", "losses"]])
one_score_differential(df)