import adjustText
import nfl_data_py as nfl
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

pbp = nfl.import_pbp_data([2025])
third_downs = pbp[(pbp["down"] == 4) & (pbp["pass"] == 1)]

df = (
    third_downs
    .sort_values("game_id")
    .groupby("passer_player_name")
    .agg(
        qb_epa=("qb_epa", "mean"),
        qb_att=("pass_attempt", "sum"),
        posteam=("posteam", "last")
    )
)
df = df[df["qb_att"] >= 8]


fig, ax = plt.subplots(figsize=(10, 6))
ax.set_facecolor("#111111")
fig.patch.set_facecolor("#000000")
for spine in ax.spines.values():
    spine.set_color("#888888")


ax.yaxis.label.set_color("#CCCCCC")
ax.xaxis.label.set_color("#CCCCCC")

plt.tick_params(axis='x', colors='white')
plt.tick_params(axis='y', colors='white')

x_median = np.median(df["qb_att"])
y_median = np.median(df["qb_epa"])

from colors import nfl_team_colors

colors = df["posteam"].map(nfl_team_colors)
ax.scatter(df["qb_att"], df["qb_epa"], c=colors, s=90, zorder=3)

texts = []
print(df)
for name, qb in df.iterrows():
    texts.append(ax.text(qb['qb_att'], qb['qb_epa'], name, fontsize=11, ha='center', va='center', color='white', zorder=4))
adjustText.adjust_text(texts)

ax.axvline(x=x_median, color='gray', linestyle='--', linewidth=1, alpha=0.7, zorder=1)
ax.axhline(y=y_median, color='gray', linestyle='--', linewidth=1, alpha=0.7, zorder=1)

plt.title("NFL QB EPAs on 4th Down", fontsize=14, fontweight="bold", color="#CCCCCC")

ax.set_ylabel("EPA per Dropback", fontsize=12)
ax.set_xlabel("4th Down Pass Attempts", fontsize=12)
plt.tight_layout()
# plt.show()
plt.savefig("qbs.png", dpi=300)