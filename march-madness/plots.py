import matplotlib.pyplot as plt
import numpy as np

def stacked_bar(appearances):
    fig, ax = plt.subplots(figsize=(10, 6), facecolor="black")
    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")

    seeds = np.arange(1, 17)

    final_four = [x['final four'] for x in appearances.values()]
    championship = [x['championship'] for x in appearances.values()]
    wins = [x['wins'] for x in appearances.values()]

    ax.bar(seeds, final_four, label="Final Four", color="#1e40af")
    ax.bar(seeds, championship, bottom=final_four, label="Championship", color="#3b82f6")
    ax.bar(seeds, wins, bottom=np.array(final_four) + np.array(championship), label="Wins", color="#93c5fd")

    ax.set_xlabel("Seed", color="white")
    ax.set_ylabel("Count (across simulations)", color="white")
    ax.set_xticks(seeds)
    ax.legend(facecolor="black", edgecolor="none", labelcolor="white")

    ax.tick_params(colors="white")
    for i, spine in enumerate(ax.spines.values()):
        if i in [0, 2]:
            spine.set_color("white")

    fig.tight_layout()

def pie_chart(appearances):
    norm = np.linspace(0, 1, 16)
    colors = plt.cm.plasma(norm)  # plasma colormap

    fig, ax = plt.subplots(figsize=(8, 8), facecolor="black")  # black background
    ax.pie(
        [x['final four'] for x in appearances.values()],
        colors=colors,
        startangle=90,
        counterclock=False
    )

    plt.show()