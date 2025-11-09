differential_500_below = -3 -30 -24
differential_winning_record = 16 + 7 + 10 + -10

import matplotlib.pyplot as plt
import numpy as np

values = [differential_500_below, differential_winning_record]
colors = ['#e74c3c', '#2ecc71']

x = np.array([0, 0.3])

fig, ax = plt.subplots(figsize=(5, 5))
bars = ax.bar(x, values, color=colors, width=0.25)  # wider bars = less space


for i, v in enumerate(values):
    ax.text(
        x[i],
        v/2 if v < 0 else v/2,  # halfway up the bar
        f"{v:+}",               # e.g., +25 or -58
        color="white",
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold"
    )


ax.margins(x=0.05)
# labels
ax.set_xticks(x)
ax.set_xticklabels(['.500 or below', 'Above .500'], color='white')


ax.set_xlabel("")
ax.tick_params(left=False, bottom=False)
ax.yaxis.set_visible(False)

for i, spine in enumerate(ax.spines.values()):
    spine.set_visible(False)

fig.text(
    0.49, 0.03,  # x, y position (centered horizontally, just below plot)
    "Based on team record at time of game",
    ha='center', va='center',
    fontsize=8, color='gray', alpha=0.8, style='italic'
)

ax.axhline(0, color='white', linewidth=1)
ax.set_title(label="ATL PD by Opponent Record", color="white")
ax.set_facecolor('#000000')
fig.patch.set_facecolor('#000000')
plt.subplots_adjust(left=0.25, right=0.75)

plt.savefig("atlpd.png", dpi=300)
