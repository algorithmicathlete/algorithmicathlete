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

def draw_shots(ax, df):
    made_shots = df[df['SHOT_MADE_FLAG'] == 1]
    missed_shots = df[df['SHOT_MADE_FLAG'] == 0]

    ax.scatter(made_shots['LOC_X'], made_shots['LOC_Y'] + 60, c='green', s=10, alpha=0.6)
    ax.scatter(missed_shots['LOC_X'], missed_shots['LOC_Y'] + 60, c='red', s=10, alpha=0.6)

def draw_shots_hex(ax, df, gridsize=25, mincount=200):
    x = df["LOC_X"].to_numpy()
    y = (df["LOC_Y"] + 60).to_numpy()  # shift to half-court coords

    hb = ax.hexbin(
        x, y,
        gridsize=gridsize,
        extent=[-250, 250, 0, 470],
        mincnt=mincount,
        linewidths=0,
        edgecolors='none',
        cmap='plasma',
        norm=LogNorm(),
    )

    return hb