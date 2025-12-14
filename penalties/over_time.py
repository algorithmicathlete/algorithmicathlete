# import time
#
# import requests
# from bs4 import BeautifulSoup
#
#
# total_flags = []
# total_plays = []
# total_yards = []
# total_accepted_flags = []
#
# for year in range(2009, 2025+1):
#     r = requests.get(f"https://www.nflpenalties.com/index.php?year={year}&view=games")
#     soup = BeautifulSoup(r.content, "lxml")
#
#     footer = soup.find("tfoot")
#     stats = [i.text for i in footer.find_all("td")]
#
#     total_plays.append(stats[2])
#     total_accepted_flags.append(stats[3])
#     total_yards.append(stats[4])
#     total_flags.append(stats[-3])
#     time.sleep(2)
#
# print(total_flags)
# print(total_plays)
# print(total_yards)
# print(total_accepted_flags)
import numpy as np

total_flags = ['6.93', '6.95', '7.30', '7.13', '6.81', '7.95', '8.10', '7.80', '7.80', '7.87', '8.01', '6.50', '6.86', '6.56', '6.72', '7.56', '7.95']
total_plays = ['174.24', '174.73', '176.21', '177.07', '176.41', '177.74', '180.22', '178.59', '176.85', '176.51', '177.29', '157.60', '154.12', '153.47', '154.67', '152.77', '150.92']
total_yards = ['48.77', '50.65', '53.35', '52.58', '52.49', '55.34', '58.57', '57.24', '57.31', '56.93', '56.76', '48.01', '50.39', '45.57', '46.73', '51.83', '53.46']
total_accepted_flags = ['5.93', '6.02', '6.32', '6.22', '6.08', '6.60', '6.87', '6.63', '6.60', '6.68', '6.69', '5.56', '5.86', '5.55', '5.67', '6.40', '6.64']
plays_per_flag = [float(flags)/(float(plays)/100) for (plays, flags) in zip(total_plays, total_flags)]

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10,5))
plt.plot([x for x in range(2009, 2025+1)], list(map(float, plays_per_flag)), marker='o')

fig.set_facecolor("#000000")
ax.set_facecolor("#111111")
for i, spine in enumerate(ax.spines.values()):
    spine.set_color("#CCCCCC")

ax.yaxis.label.set_color("#CCCCCC")
ax.xaxis.label.set_color("#CCCCCC")

plt.tick_params(axis='x', colors='white')
plt.tick_params(axis='y', colors='white')
plt.title("NFL Flags Per 100 Plays", fontsize=14, fontweight="bold", color="#cccccc")
plt.tight_layout();
# plt.show()
plt.savefig("flagsperplay.png", dpi=350)