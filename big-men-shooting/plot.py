import numpy as np
from matplotlib import pyplot as plt

fig = plt.figure(figsize=(7, 6.8))
ax = fig.add_axes([0, 0, 1, 1], facecolor="black")

import matplotlib as mpl
from matplotlib.colors import LogNorm


def create_court(ax, color):
    ax.plot([-220, -220], [0, 140], linewidth=2, color=color)
    ax.plot([220, 220], [0, 140], linewidth=2, color=color)
    ax.add_artist(mpl.patches.Arc((0, 140), 440, 315, theta1=0, theta2=180, facecolor='none', edgecolor=color, lw=2))
    ax.plot([-80, -80], [0, 190], linewidth=2, color=color)
    ax.plot([80, 80], [0, 190], linewidth=2, color=color)
    ax.plot([-60, -60], [0, 190], linewidth=2, color=color)
    ax.plot([60, 60], [0, 190], linewidth=2, color=color)
    ax.plot([-80, 80], [190, 190], linewidth=2, color=color)
    ax.add_artist(mpl.patches.Circle((0, 190), 60, facecolor='none', edgecolor=color, lw=2))
    ax.add_artist(mpl.patches.Circle((0, 60), 15, facecolor='none', edgecolor=color, lw=2))
    ax.plot([-30, 30], [40, 40], linewidth=2, color=color)
    ax.set_xlim(-250, 250)
    ax.set_ylim(0, 470)
    ax.set_xticks([])
    ax.set_yticks([])
    mpl.rcParams['font.family'] = 'Avenir'
    mpl.rcParams['font.size'] = 18
    mpl.rcParams['axes.linewidth'] = 2

def draw_shots_hex(ax, df, gridsize=25):
    x = df["LOC_X"].to_numpy()
    y = (df["LOC_Y"] + 60).to_numpy()  # shift to half-court coords

    hb = ax.hexbin(
        x, y,
        gridsize=gridsize,
        extent=[-250, 250, 0, 470],
        mincnt=None,
        linewidths=0,
        edgecolors='none',
        cmap='plasma',
        norm=LogNorm(),
    )

    counts = hb.get_array()

    X = 200
    top_indices = np.argsort(counts)[-X:]

    mask = np.ones_like(counts, dtype=bool)
    mask[top_indices] = False
    counts_masked = np.ma.array(counts, mask=mask)

    # Update the hexbin artist
    hb.set_array(counts_masked)

    return hb

import pandas as pd
df = pd.read_csv("7foot_2010.csv")

draw_shots_hex(ax, df, gridsize=30)

create_court(ax, 'white')
plt.show()
# plt.savefig("big-man-shots-2000.png", dpi=300)