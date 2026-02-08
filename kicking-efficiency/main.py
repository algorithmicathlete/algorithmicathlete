import adjustText
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from colors import nfl_team_colors

df = pd.read_csv("kicking.csv")
df = df[df["att"] > 15]
df["color"] = df["team"].map(nfl_team_colors).fillna("#AAAAAA")

fig, ax = plt.subplots(figsize=(12, 6))
ax.set_facecolor("#111111")
fig.patch.set_facecolor("#000000")
for spine in ax.spines.values():
    spine.set_color("#888888")


ax.yaxis.label.set_color("#CCCCCC")
ax.xaxis.label.set_color("#CCCCCC")

plt.tick_params(axis='x', colors='white')
plt.tick_params(axis='y', colors='white')

x_median = np.median(df["avg_fg_distance"])
y_median = np.median(df["fg_pct"])

ax.scatter(df["avg_fg_distance"], df["fg_pct_oe"], c=df["color"], s=100)
texts = []
for _, row in df.iterrows():
    if row["kicker_player_name"] == "W.Lutz":
        texts.append(ax.annotate(row["kicker_player_name"], (row["avg_fg_distance"]+0.05, row["fg_pct_oe"]-0.5), color="#cccccc", fontsize=11))
    else:
        texts.append(ax.annotate(row["kicker_player_name"], (row["avg_fg_distance"]+0.05, row["fg_pct_oe"]), color="#cccccc", fontsize=11))


# adjustText.adjust_text(texts)

ax.axvline(x=x_median, color='gray', linestyle='--', linewidth=1, alpha=0.7, zorder=1)
ax.axhline(y=y_median, color='gray', linestyle='--', linewidth=1, alpha=0.7, zorder=1)

ax.set_ylabel("FG% Over Expected", fontsize=12)
ax.set_xlabel("Average Field Goal Distance", fontsize=12)

plt.tight_layout()
# plt.show()
plt.savefig("pctoevsdist2.png", dpi=350)