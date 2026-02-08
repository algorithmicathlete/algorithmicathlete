import matplotlib.pyplot as plt

fpd_history = [0, 4, -10, 0, -5, 1, 14, 10, 7, 4, 11, 7, 14, 3, 17, 11, 4, -9, -27]
spd_history = [0, -7, -24, -17, -11, -16, -17, -27, -19, -12, -17, -10, -8, -4, 10, 16, 19, 29, 51]

fpd_total = [4, -14, 10, -5, 6, 13, -4, -3, -3, 7, -4, 7, -11, 14, -6, -7, -13, -18]
spd_total = [-7, -17, 7, 6, -5, -1, -10, 8, 7, -5, 7, 2, 4, 14, 6, 3, 10, 22]

fpd_second_half = [0]
for x in fpd_total[7:]:
    fpd_second_half.append(fpd_second_half[-1]+x)
spd_second_half = [0]
for x in spd_total[7:]:
    spd_second_half.append(spd_second_half[-1]+x)

print(fpd_second_half)


import matplotlib.pyplot as plt
import numpy as np

values = [-37, 78]
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
ax.set_xticks(x)
ax.set_xticklabels(['1st Half', '2nd Half'], color='white')

fig.text(
    0.49, 0.03,  # x, y position (centered horizontally, just below plot)
    "Since Week 9, including Wild Card",
    ha='center', va='center',
    fontsize=8, color='gray', alpha=0.8, style='italic'
)

ax.set_xlabel("")
ax.tick_params(left=False, bottom=False)
ax.yaxis.set_visible(False)

for i, spine in enumerate(ax.spines.values()):
    spine.set_visible(False)

ax.axhline(0, color='white', linewidth=1)
ax.set_title(label="Chicago Bears Point Differential", fontweight="bold", color="white")
ax.set_facecolor('#000000')
fig.patch.set_facecolor('#000000')
plt.subplots_adjust(left=0.25, right=0.75)
plt.savefig("pdhalf.png", dpi=350)
