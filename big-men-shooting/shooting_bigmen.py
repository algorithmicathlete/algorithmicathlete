import adjustText
import pandas as pd
from nba_api.stats.endpoints import commonallplayers

df = pd.read_csv("big-men.csv")
df = df[df["3PA"] > 10]

players = commonallplayers.CommonAllPlayers(
    is_only_current_season=1,
).get_data_frames()[0]

seven_footers = players[players["DISPLAY_FIRST_LAST"].isin(df["Player"].values.flatten())][["PERSON_ID", "DISPLAY_FIRST_LAST"]]

import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg

df = df.sort_values("3P%", ascending=False)
names = df["Player"].values.flatten()
x = df["3PA"].values.flatten()
y = df["3P%"].values.flatten()

fig, ax = plt.subplots(figsize=(10,6))
fig.set_facecolor("#000000")

ax.set_facecolor("#111111")

ax.scatter(x, y)
texts = []

print(df[["Player", "3PA", "3P%"]])

for i, name in enumerate(names):
    # texts.append(plt.text(x[i], y[i], name, color="#CCCCCC"))

    player = seven_footers.loc[seven_footers["DISPLAY_FIRST_LAST"] == name].iloc[0]

    img = mpimg.imread(f"headshots/{player['PERSON_ID']}.png")
    imagebox = OffsetImage(img, zoom=0.25)

    increase = False
    ab = AnnotationBbox(imagebox, (x[i]+(1.5 if increase else 0), y[i]+0.01+(0.0025 if increase else 0)), frameon=False)
    ax.add_artist(ab)

# adjustText.adjust_text(texts)
ax.yaxis.label.set_color("#CCCCCC")
ax.xaxis.label.set_color("#CCCCCC")

plt.tick_params(axis='x', colors='white')
plt.tick_params(axis='y', colors='white')

for spine in ax.spines.values():
    spine.set_color("#888888")

ax.set_ylabel("3-Point %", fontsize=14)
ax.set_xlabel("3-Point Attempts", fontsize=14)
plt.tight_layout()
ax.set_ylim(bottom=0.095, top=0.45)
ax.set_xlim(left=14)

# plt.show()
plt.savefig("big-men-3s.png", dpi=300)