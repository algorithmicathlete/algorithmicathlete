import numpy as np
from matplotlib import image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

teams = {'NO': {'committed': 606.0, 'received': 630.0, 'win%': 0.167}, 'ARI': {'committed': 656.0, 'received': 674.0, 'win%': 0.25}, 'BAL': {'committed': 546.0, 'received': 637.0, 'win%': 0.5}, 'BUF': {'committed': 662.0, 'received': 529.0, 'win%': 0.667}, 'JAX': {'committed': 844.0, 'received': 739.0, 'win%': 0.667}, 'CAR': {'committed': 563.0, 'received': 610.0, 'win%': 0.538}, 'CLE': {'committed': 640.0, 'received': 644.0, 'win%': 0.25}, 'CIN': {'committed': 485.0, 'received': 689.0, 'win%': 0.333}, 'PHI': {'committed': 765.0, 'received': 600.0, 'win%': 0.667}, 'DAL': {'committed': 855.0, 'received': 957.0, 'win%': 0.5}, 'GB': {'committed': 566.0, 'received': 620.0, 'win%': 0.708}, 'DET': {'committed': 593.0, 'received': 559.0, 'win%': 0.615}, 'HOU': {'committed': 714.0, 'received': 662.0, 'win%': 0.583}, 'LA': {'committed': 426.0, 'received': 711.0, 'win%': 0.75}, 'KC': {'committed': 753.0, 'received': 711.0, 'win%': 0.5}, 'LAC': {'committed': 598.0, 'received': 596.0, 'win%': 0.667}, 'LV': {'committed': 701.0, 'received': 672.0, 'win%': 0.167}, 'NE': {'committed': 667.0, 'received': 670.0, 'win%': 0.846}, 'IND': {'committed': 628.0, 'received': 651.0, 'win%': 0.667}, 'MIA': {'committed': 577.0, 'received': 659.0, 'win%': 0.417}, 'CHI': {'committed': 759.0, 'received': 472.0, 'win%': 0.75}, 'MIN': {'committed': 715.0, 'received': 637.0, 'win%': 0.333}, 'WAS': {'committed': 678.0, 'received': 671.0, 'win%': 0.25}, 'NYG': {'committed': 818.0, 'received': 813.0, 'win%': 0.154}, 'PIT': {'committed': 577.0, 'received': 649.0, 'win%': 0.5}, 'NYJ': {'committed': 681.0, 'received': 602.0, 'win%': 0.25}, 'SEA': {'committed': 594.0, 'received': 727.0, 'win%': 0.75}, 'SF': {'committed': 499.0, 'received': 568.0, 'win%': 0.692}, 'TB': {'committed': 517.0, 'received': 634.0, 'win%': 0.583}, 'ATL': {'committed': 534.0, 'received': 573.0, 'win%': 0.333}, 'TEN': {'committed': 685.0, 'received': 529.0, 'win%': 0.083}, 'DEN': {'committed': 878.0, 'received': 685.0, 'win%': 0.833}}

import pandas as pd
import matplotlib.pyplot as plt
from colors import nfl_team_colors

df = pd.DataFrame.from_dict(teams, orient="index")
df.index.name = "TEAM"
df = df.reset_index()
df['DIFF'] = (df['received'] - df['committed']).astype(int)
df=df.sort_values("DIFF", ascending=False)

fig, ax = plt.subplots(figsize=(12,6))
fig.set_facecolor("#000000")
ax.set_facecolor("#111111")

ax.scatter(df["DIFF"], df["win%"], alpha=0)

for i, txt in enumerate(df["TEAM"]):
    path = f"../nfl_logos/{'lar' if txt.lower() == 'la' else txt.lower()}.png"
    logo = mpimg.imread(path)
    imagebox = OffsetImage(logo, zoom=0.28)
    ab = AnnotationBbox(imagebox, (df["DIFF"].iloc[i], df["win%"].iloc[i]), frameon=False)
    plt.gca().add_artist(ab)

for i, spine in enumerate(ax.spines.values()):
    spine.set_color("#CCCCCC")

# plt.title("Penalty Yards Differential (2025)", color="white", alpha=0.8, fontsize=14, fontweight="bold")

ax.set_xlabel("Penalty Differential", fontsize=14, color="#cccccc")
ax.set_ylabel("Win %", fontsize=14, color="#cccccc")

plt.tick_params(axis='x', colors='white')
plt.tick_params(axis='y', colors='white')

x = df["DIFF"]
y = df["win%"]

m, b = np.polyfit(x, y, 1)
plt.plot(x, m * x + b, linewidth=1, alpha=0.4, color="white", linestyle="--")
plt.tick_params(axis='x', colors='white')
plt.tick_params(axis='y', colors='white')
r = np.corrcoef(x, y)[0, 1]
print("r =", r)


plt.tight_layout()

# plt.show()
plt.savefig("winpercpenalty.png", dpi=350)