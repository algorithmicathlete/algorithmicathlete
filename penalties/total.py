from collections import defaultdict
from colors import nfl_team_colors
import nfl_data_py as nfl
import os
print(os.getcwd())
import matplotlib.pyplot as plt


pbp = nfl.import_pbp_data([2025])
penalty = pbp[(pbp["penalty"] == 1) & (pbp["penalty_yards"] > 0)]

print(list(penalty.columns))

teams = defaultdict(lambda: {"committed": 0, "received": 0})

print(penalty["penalty_type"].unique())
for _, row in penalty.iterrows():
    offense, defense = row["posteam"], row["defteam"]
    yards = row["penalty_yards"]
    penalty_team = row["penalty_team"]
    if row["penalty_player_name"] == "R.Moss":
        continue

    if offense == penalty_team:
        teams[offense]["committed"] += yards
        teams[defense]["received"] += yards
    elif defense == penalty_team:
        teams[defense]["committed"] += yards
        teams[offense]["received"] += yards


    # print(row["penalty_team"], row["posteam"], row["defteam"], row["penalty_yards"], row["desc"])

import pandas as pd
from matplotlib import image as mpimg
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
df = pd.DataFrame.from_dict(teams, orient="index")
df.index.name = "TEAM"
df = df.reset_index()
df['DIFF'] = (df['received'] - df['committed']).astype(int)
df=df.sort_values("DIFF", ascending=False)

fig, ax = plt.subplots(figsize=(12,6))
fig.set_facecolor("#111111")
ax.set_facecolor("#111111")

ax.bar(df["TEAM"], df["DIFF"], color=[nfl_team_colors[x] for x in df["TEAM"]])
ax.axhline(0, color='white', lw=0.5)

for i, txt in enumerate(df["TEAM"]):
    top = df["DIFF"].iloc[i] > 0

    ax.annotate(("+" if top else "")+str(df["DIFF"].iloc[i]), (i, df["DIFF"].iloc[i]+(0.5 if top else -2)), ha="center", va="bottom" if top else "top", fontsize=9, color="white")

    path = f"../nfl_logos/{'lar' if txt.lower() == 'la' else txt.lower()}.png"
    logo = mpimg.imread(path)
    imagebox = OffsetImage(logo, zoom=0.28)
    ab = AnnotationBbox(imagebox, (i, top*-38 + 19), frameon=False)
    plt.gca().add_artist(ab)

for i, spine in enumerate(ax.spines.values()):
    spine.set_color("#111111")

plt.title("Penalty Yards Differential (Without DPI)", color="white", alpha=0.8, fontsize=14, fontweight="bold")
plt.xticks([])
plt.yticks([])
plt.tight_layout()

ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)

plt.show()
# plt.savefig("totalyardsnodpi.png", dpi=350)
