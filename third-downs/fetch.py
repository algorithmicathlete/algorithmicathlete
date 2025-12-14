import os

import nfl_data_py as nfl
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

pbp = nfl.import_pbp_data([2025])
third_downs = pbp[pbp["down"] == 3]
third_downs.dropna(subset=["epa", "defteam"])
print(list(pbp.columns))
def_epa = third_downs.groupby("defteam")["epa"].mean().rename("def_epa")
# converted = third_downs.groupby("defteam")["third_down_converted"].mean().sort_values()
off_epa = third_downs.groupby("posteam")["epa"].mean().rename("off_epa")
# off_converted = third_downs.groupby("posteam")["third_down_converted"].mean().rename("off_epa")

df = (
    pd.concat([off_epa, def_epa], axis=1)
    .dropna()
    .reset_index()
    .rename(columns={"index": "team"})
)

fig, ax = plt.subplots(figsize=(10, 6))
ax.set_facecolor("#111111")
fig.patch.set_facecolor("#000000")
for spine in ax.spines.values():
    spine.set_color("#888888")

ax.yaxis.label.set_color("#CCCCCC")
ax.xaxis.label.set_color("#CCCCCC")

plt.tick_params(axis='x', colors='white')
plt.tick_params(axis='y', colors='white')

ax.axvline(x=0, color='gray', linestyle='--', linewidth=1, alpha=0.7, zorder=1)
ax.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.7, zorder=1)

for _, team in df.iterrows():
    name = team['team'].lower()
    path = f"../nfl_logos/{'lar' if name == 'la' else name}.png"
    logo = mpimg.imread(path)
    imagebox = OffsetImage(logo, zoom=0.35)
    ab = AnnotationBbox(imagebox, (team['off_epa'], -team['def_epa']), frameon=False)
    plt.gca().add_artist(ab)

ax.scatter(df['off_epa'], -df['def_epa'], color='dodgerblue', s=80, alpha=0)

plt.title("NFL Teams' EPA on 3rd Down", fontsize=14, fontweight="bold", color="#CCCCCC")
ax.set_xlabel("Average Offensive EPA", fontsize=12)
ax.set_ylabel("Average Defensive EPA (Inverted)", fontsize=12)

plt.tight_layout()
# plt.show()
plt.savefig("3rddown.png", dpi=300)