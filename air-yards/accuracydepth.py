import math
import matplotlib.pyplot as plt
import nfl_data_py as nfl
import numpy as np
import pandas as pd
from matplotlib import image as mpimg, patches
from matplotlib.offsetbox import AnnotationBbox, OffsetImage

pbp = nfl.import_pbp_data([2025])
pbp = pbp[pbp["pass_attempt"] == 1]

x = []
y = []
teams = []

for team_id, team in pbp.groupby("posteam"):
    completed = team["complete_pass"].sum()
    attempts = completed + team["incomplete_pass"].sum()
    adot = team["air_yards"].mean() # IAY/A / ADOT
    x.append(adot)
    y.append(completed/attempts*100)
    teams.append(team_id)
    print(team_id, completed, attempts, adot)


# make the scatter plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_facecolor("#111111")
fig.patch.set_facecolor("#000000")
for spine in ax.spines.values():
    spine.set_color("#888888")

ax.yaxis.label.set_color("#CCCCCC")
ax.xaxis.label.set_color("#CCCCCC")

plt.tick_params(axis='x', colors='white')
plt.tick_params(axis='y', colors='white')

x_median = np.median(x)
y_median = np.median(y)
ax.axhline(y_median,color='gray', linestyle='--', linewidth=1, alpha=0.7, zorder=1)
ax.axvline(x_median,color='gray', linestyle='--', linewidth=1, alpha=0.7, zorder=1)

for team, xi, yi in zip(teams, x, y):
    path = f"logos/{team.lower()}.png"
    logo = mpimg.imread(path)
    imagebox = OffsetImage(logo, zoom=0.3)
    ab = AnnotationBbox(imagebox, (xi, yi), frameon=False)
    plt.gca().add_artist(ab)

ax.scatter(x, y, color='dodgerblue', s=80, alpha=0)

ax.text(8.5, 75, "Efficient Passers",
        color="white", fontsize=16, ha="center", va="center", fontweight="semibold", alpha=0.8)

ax.text(6.5, 73.3, "Dink & Dunk",
        color="white", fontsize=16, ha="center", va="center", fontweight="bold", alpha=0.8)

ax.text(8.8, 59, "Boom or Bust",
        color="white", fontsize=16, ha="center", va="center", fontweight="bold", alpha=0.8)

ax.text(7.1, 61.7, "Slow Movers",
        color="white", fontsize=16, ha="center", va="center", fontweight="bold", alpha=0.8)

ax.set_xlabel("Average Depth of Target", fontsize=14)   # rename axis
ax.set_ylabel("Completion %", fontsize=14)   # rename axis

# Calculate correlation coefficient (r)
r = np.corrcoef(x, y)[0, 1]


plt.tight_layout()
# plt.show()
plt.savefig("adotvsaccuracy.png", dpi=350)