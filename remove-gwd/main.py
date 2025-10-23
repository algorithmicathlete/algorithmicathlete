import numpy as np
from adjustText import adjust_text

records = {'MIA': [8, 9], 'DET': [15, 2], 'ATL': [8, 9], 'KC': [15, 2], 'LV': [4, 13], 'WAS': [12, 5], 'NYJ': [5, 12], 'SEA': [10, 7], 'PIT': [10, 7], 'PHI': [14, 3], 'LA': [10, 7], 'DEN': [10, 7], 'HOU': [10, 7], 'ARI': [8, 9], 'BAL': [12, 5], 'DAL': [7, 10], 'JAX': [4, 13], 'BUF': [13, 4], 'IND': [8, 9], 'GB': [11, 6], 'CLE': [3, 14], 'NE': [4, 13], 'TEN': [3, 14], 'CAR': [5, 12], 'MIN': [14, 3], 'SF': [6, 11], 'LAC': [11, 6], 'NO': [5, 12], 'TB': [10, 7], 'CIN': [9, 8], 'CHI': [5, 12], 'NYG': [3, 14]}
new_records = {'MIA': [8, 9], 'DET': [11, 6], 'ATL': [8, 9], 'KC': [8, 9], 'LV': [3, 14], 'WAS': [9, 8], 'NYJ': [9, 8], 'SEA': [8, 9], 'PIT': [10, 7], 'PHI': [12, 5], 'LA': [7, 10], 'DEN': [10, 7], 'HOU': [12, 5], 'ARI': [7, 10], 'BAL': [12, 5], 'DAL': [8, 9], 'JAX': [9, 8], 'BUF': [12, 5], 'IND': [5, 12], 'GB': [10, 7], 'CLE': [4, 13], 'NE': [7, 10], 'TEN': [4, 13], 'CAR': [4, 13], 'MIN': [10, 7], 'SF': [9, 8], 'LAC': [13, 4], 'NO': [9, 8], 'TB': [11, 6], 'CIN': [11, 6], 'CHI': [7, 10], 'NYG': [5, 12]}

gwd = {'MIA': 3, 'DET': 4, 'ATL': 3, 'KC': 7, 'LV': 2, 'WAS': 5, 'NYJ': 3, 'SEA': 4, 'PIT': 2, 'PHI': 4, 'LAR': 5, 'DEN': 3, 'HOU': 2, 'ARI': 3, 'BAL': 2, 'DAL': 1, 'JAX': 2, 'BUF': 2, 'IND': 5, 'GB': 3, 'CLE': 2, 'NE': 1, 'TEN': 2, 'CAR': 4, 'MIN': 5, 'SF': 1, 'LAC': 2, 'NO': 1, 'TB': 2, 'CIN': 2, 'CHI': 1, 'NYG': 0}
gld = {'MIA': 3, 'DET': 0, 'ATL': 3, 'KC': 0, 'LV': 1, 'WAS': 2, 'NYJ': 7, 'SEA': 2, 'PIT': 2, 'PHI': 2, 'LAR': 2, 'DEN': 3, 'HOU': 4, 'ARI': 2, 'BAL': 2, 'DAL': 2, 'JAX': 7, 'BUF': 1, 'IND': 2, 'GB': 2, 'CLE': 3, 'NE': 4, 'TEN': 3, 'CAR': 3, 'MIN': 1, 'SF': 4, 'LAC': 4, 'NO': 5, 'TB': 3, 'CIN': 4, 'CHI': 3, 'NYG': 2}

import matplotlib.pyplot as plt

team_color_codes = {
    "bal": [(26, 25, 95), (0, 0, 0), (158, 124, 12), (198, 12, 14)],
    "cin": [(251, 79, 20), (0, 0, 0)],
    "cle": [(49, 29, 0), (255, 60, 0)],
    "pit": [(255, 182, 18), (16, 24, 32), (0, 48, 135), (198, 12, 48), (165, 172, 175)],
    "buf": [(0, 51, 141), (198, 12, 48)],
    "mia": [(0, 142, 151), (252, 76, 2), (0, 87, 120)],
    "ne": [(0, 34, 68), (198, 12, 48), (176, 183, 188)],
    "nyj": [(18, 87, 64), (0, 0, 0), (255, 255, 255)],
    "hou": [(3, 32, 47), (167, 25, 48)],
    "ind": [(0, 44, 95), (162, 170, 173)],
    "jax": [(215, 162, 42), (159, 121, 44), (0, 103, 120)],
    "ten": [(12, 35, 64), (75, 146, 219), (200, 16, 46), (138, 141, 143)],
    "den": [(251, 79, 20), (0, 34, 68)],
    "kc": [(227, 24, 55), (255, 184, 28)],
    "lv": [(165, 172, 175)],
    "lac": [(0, 128, 198), (255, 194, 14), (255, 255, 255)],
    "chi": [(200, 56, 3)],
    "det": [(0, 118, 182), (176, 183, 188), (0, 0, 0), (255, 255, 255)],
    "gb": [(24, 48, 40), (255, 184, 28)],
    "min": [(79, 38, 131), (255, 198, 47)],
    "dal": [(0, 53, 148), (0, 34, 68), (134, 147, 151), (127, 150, 149), (255, 255, 255)],
    "nyg": [(1, 35, 82), (163, 13, 45), (155, 161, 162)],
    "phi": [(0, 76, 84), (165, 172, 175), (186, 202, 211), (0, 0, 0), (95, 96, 98)],
    "was": [(90, 20, 20), (255, 182, 18)],
    "atl": [(167, 25, 48), (0, 0, 0), (165, 172, 175)],
    "car": [(0, 133, 202), (16, 24, 32), (191, 192, 191)],
    "no": [(211, 188, 141), (16, 24, 31)],
    "tb": [(213, 10, 10), (255, 121, 0), (10, 10, 8), (177, 186, 191), (52, 48, 43)],
    "ari": [(151, 35, 63), (0, 0, 0), (255, 182, 18)],
    "lar": [(0, 53, 148), (255, 163, 0), (255, 130, 0), (255, 209, 0), (255, 255, 255)],
    "sf": [(170, 0, 0), (173, 153, 93)],
    "sea": [(0, 34, 68), (105, 190, 40), (165, 172, 175)]
}

teams = [(x, gwd[x], gld[x], team_color_codes[x.lower()][0]) for x in gwd.keys()]

import matplotlib

fig, ax = plt.subplots(figsize=(7,7))
fig.set_facecolor("black")
ax.set_facecolor("black")

ax.spines['left'].set_color('#aaaaaa')
ax.spines['bottom'].set_color('#aaaaaa')   # hex color
ax.spines['right'].set_color('none')       # remove spine
ax.spines['top'].set_color('none')

xs = np.array([x[1] for x in teams])
ys = np.array([x[2] for x in teams])

jitter = 0.1  # adjust to taste
xs = xs + np.random.uniform(-jitter, jitter, size=len(xs))
ys = ys + np.random.uniform(-jitter, jitter, size=len(ys))


ax.scatter(xs, ys, alpha=0.7, c=[[y/255 for y in x[3]] for x in teams], linewidths=0.5, s=50)

texts = []
for i, (team, gwd, gld, _) in enumerate(teams):
    texts.append(ax.annotate(
        team,                # text
        (xs[i], ys[i]),          # point position
        fontsize=9,
        color="white"
    ))

adjust_text(texts, arrowprops=dict(arrowstyle='-', color='#a0a0a0'))

plt.xlabel("Game-Winning Drives", color="white")
plt.ylabel("Game-Losing Drives", color="white")
ax.tick_params(colors="white")

plt.tight_layout()
fig.savefig("gwdgld.png", facecolor=fig.get_facecolor(), bbox_inches="tight", dpi=300)

plt.show()

# import csv
#
# with open("gwd.csv", "w", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerow(["team", "record", "new_record", "diff", "gwd", "gld"])
#     for (team, (win, loss)), (new_win, new_loss) in zip(records.items(), new_records.values()):
#         stats = [team, f"{win} - {loss}", f"{new_win} - {new_loss}", new_win-win, gwd[team], gld[team]]
#         print(stats)
#         writer.writerow(stats)