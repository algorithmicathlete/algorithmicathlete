import math
from collections import defaultdict

import adjustText
import matplotlib.pyplot as plt
import nfl_data_py as nfl
import numpy as np
import pandas as pd


team_colors = {
    "ARI": "#97233F",  # Arizona Cardinals
    "ATL": "#A71930",  # Atlanta Falcons
    "BAL": "#241773",  # Baltimore Ravens
    "BUF": "#00338D",  # Buffalo Bills
    "CAR": "#0085CA",  # Carolina Panthers
    "CHI": "#C83803",  # Chicago Bears
    "CIN": "#FB4F14",  # Cincinnati Bengals
    "CLE": "#FF3C00",  # Cleveland Browns
    "DAL": "#041E42",  # Dallas Cowboys
    "DEN": "#FB4F14",  # Denver Broncos
    "DET": "#0076B6",  # Detroit Lions
    "GB": "#203731",  # Green Bay Packers
    "HOU": "#03202F",  # Houston Texans
    "IND": "#002C5F",  # Indianapolis Colts
    "JAX": "#006778",  # Jacksonville Jaguars
    "KC": "#E31837",  # Kansas City Chiefs
    "LV": "#A5ACAF",  # Las Vegas Raiders
    "LAC": "#0080C6",  # Los Angeles Chargers
    "LA": "#003594",  # Los Angeles Rams
    "MIA": "#008E97",  # Miami Dolphins
    "MIN": "#4F2683",  # Minnesota Vikings
    "NE": "#002244",  # New England Patriots
    "NO": "#D3BC8D",  # New Orleans Saints
    "NYG": "#0B2265",  # New York Giants
    "NYJ": "#125740",  # New York Jets
    "PHI": "#004C54",  # Philadelphia Eagles
    "PIT": "#FFB612",  # Pittsburgh Steelers
    "SF": "#AA0000",  # San Francisco 49ers
    "SEA": "#002244",  # Seattle Seahawks
    "TB": "#D50A0A",  # Tampa Bay Buccaneers
    "TEN": "#4B92DB",  # Tennessee Titans
    "WAS": "#773141"   # Washington Commanders
}

pbp = nfl.import_pbp_data([2025])
print(list(pbp.columns))
pbp = pbp[pbp["pass_attempt"] == 1]

qbs = defaultdict(list)
qb_teams = defaultdict(str)


for _, play in pbp.iterrows():
    name = play["passer_player_name"]
    qb_teams[name] = play["posteam"]
    if play["air_yards"] >= 20:
        qbs[name].append(play["epa"])
    else:
        qbs[name].append(None)

x = [] # deep ball rate
y = [] # success rate
names = []


i = 0
for k, v in qbs.items():
    if len(v) < 80:
        continue
    i += 1
    deep_throws = [x for x in v if x is not None]
    successful_deep = [x for x in deep_throws if x > 0]

    x.append(len(deep_throws)/len(v)*100+(0.1 if k == 'P.Mahomes' else 0))
    y.append(len(successful_deep)/len(deep_throws)*100-(1 if k == 'P.Mahomes' else 0))
    names.append(k)
    print(i, k, len(deep_throws)/len(v)*100, len(successful_deep)/len(deep_throws)*100, f"{np.mean(successful_deep)}")


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


ax.scatter(x, y, c=[team_colors[qb_teams[name]] for name in names], s=90, zorder=3)

texts = []
for team, xi, yi in zip(names, x, y):
    texts.append(ax.text(xi, yi, team, fontsize=10, ha='center', va='center', color='white', zorder=4))
adjustText.adjust_text(texts)

ax.axvline(x=x_median, color='gray', linestyle='--', linewidth=1, alpha=0.7, zorder=1)
ax.axhline(y=y_median, color='gray', linestyle='--', linewidth=1, alpha=0.7, zorder=1)

ax.set_ylabel("Big Throw Success%", fontsize=14)
ax.set_xlabel("Big Throw% (20+ air yard passes)", fontsize=14)
plt.tight_layout()
# plt.show()
plt.savefig("bigthrows.png", dpi=300)
