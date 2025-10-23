import matplotlib.pyplot as plt
import numpy as np

plasma_colors = [
    # "#0d0887",  # deep violet
    "#46039f",  # purple
    # "#7201a8",  # violet
    # "#9c179e",  # magenta
    "#bd3786",  # pinkish
    # "#d8576b",  # reddish-pink
    # "#ed7953",  # orange
    # "#fb9f3a",  # golden orange
    # "#fdca26",  # bright yellow
    # "#f0f921",  # neon yellow
]

# Data
ranges = [
    [0.939, 0.928],
    [0.588, 0.744],
    [0.619, 0.679],
    [0.286, 0.375]
]

print(ranges)

labels = ["0–39 yds", "40–49 yds", "50–59 yds", "60+ yds"]
categories = ["Iced", "Non-iced"]
data = np.array(ranges)

# Plot positions
x = np.arange(len(labels))
width = 0.25

fig, ax = plt.subplots(figsize=(8, 5), facecolor="black")
fig.patch.set_facecolor("black")
ax.set_facecolor("black")

ax.tick_params(colors="white")
for i, spine in enumerate(ax.spines.values()):
    if i in [0, 2]:
        spine.set_color("white")

# Plot bars for each category
for i in range(data.shape[1]):
    ax.bar(x + (i - 0.5) * width, data[:, i], width, label=categories[i], color=["#1565C0", "#FF6F00"][i], alpha=0.9)

ax.set_ylabel("FG%", color="white")
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend(facecolor="black", edgecolor="none", labelcolor="white")
ax.set_ylim(0, 1)  # keep scale as percentages

plt.tight_layout()
plt.savefig("icedvsnoniced.png", dpi=300)

plt.show()