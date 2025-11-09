from scipy.ndimage import label

teams = {
    'TOR': ['10.3%', '9.9%', '8.9%', '8.8%', '13.8%', '17.8%', '16.6%', '13.4%', '20.1%', '20.0%', '17.4%', '17.5%', '11.2%', '5.4%', '5.1%', '9.4%', '14.9%', '7.1%', '7.0%', '15.0%', '33.7%', '33.7%', '33.9%'],
    'BOS': ['6.3%', '4.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%'],
    'NYY': ['5.0%', '9.3%', '16.5%', '16.0%', '10.5%', '4.4%', '4.2%', '7.8%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%'],
    'DET': ['5.3%', '3.7%', '5.8%', '6.0%', '10.0%', '7.1%', '7.1%', '3.4%', '8.0%', '7.4%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%'],
    'CLE': ['0.7%', '1.6%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%'],
    'SEA': ['19.5%', '19.0%', '17.9%', '17.5%', '10.7%', '16.7%', '15.9%', '21.6%', '16.1%', '15.1%', '28.0%', '27.4%', '34.7%', '39.4%', '37.2%', '32.2%', '23.7%', '33.3%', '32.8%', '22.5%', '0.0%', '0.0%', '0.0%'],
    'PHI': ['15.4%', '13.6%', '14.0%', '13.2%', '8.9%', '8.6%', '3.4%', '3.2%', '7.3%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%'],
    'MIL': ['7.2%', '6.7%', '6.5%', '6.8%', '9.1%', '8.9%', '11.1%', '10.7%', '9.7%', '6.4%', '5.6%', '11.6%', '11.4%', '7.2%', '3.4%', '3.6%', '1.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%'],
    'CHC': ['6.2%', '3.8%', '7.2%', '7.7%', '4.7%', '4.4%', '1.9%', '2.0%', '3.6%', '7.1%', '6.3%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%'],
    'CIN': ['0.5%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%'],
    'LAD': ['20.7%', '23.2%', '23.4%', '23.9%', '32.2%', '32.2%', '39.7%', '38.0%', '35.1%', '44.0%', '42.6%', '43.5%', '42.8%', '48.0%', '54.3%', '54.8%', '60.4%', '59.7%', '60.2%', '62.5%', '66.3%', '66.3%', '66.1%'],
    'SDP': ['2.9%', '5.2%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%']
}

team_colors = {
    "BOS": "#bd3039",
    "CHC": "#0e3386",
    "CIN": "#c6011f",
    "CLE": "#e31937",
    "DET": "#0C2340",
    "LAD": "#005a9c",
    "MIL": "#FFC52F",
    "NYY": "#132448",
    "PHI": "#e81828",
    "SEA": "#005c5c",
    "TOR": "#134a8e",
"SDP": "#FFC425",
}

import matplotlib.pyplot as plt


fig, ax = plt.subplots(figsize=(12, 6))
ax.set_facecolor("#111111")
fig.patch.set_facecolor("#000000")
for spine in ax.spines.values():
    spine.set_color("#888888")

from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg

goo = 0

for team, odds in teams.items():
    values = [float(odd.strip("%")) for odd in odds]
    if 0.0 in values:
        values = values[:values.index(0.0)+1]
    ax.plot(values, label=team, linewidth=2, alpha=0.8, color=team_colors[team])

    x_last = len(values) - 1
    y_last = values[-1]

    path = f"logos/{team.lower()}.png"
    logo = mpimg.imread(path)

    if len(values) > 3 or team == "CIN":
        imagebox = OffsetImage(logo, zoom=0.2 if team == "CIN" else 0.3)
        ab = AnnotationBbox(imagebox, (len(values) - 1, values[-1]), frameon=False)
        plt.gca().add_artist(ab)
    else:
        imagebox = OffsetImage(logo, zoom=0.2)
        ab = AnnotationBbox(imagebox, (len(values) - 1 + goo/5, values[-1]+(goo%2)*3), frameon=False)
        plt.gca().add_artist(ab)
        goo += 1

dates = [2, 11, 20]
names = ["Wild Card", "Division Series", "Championship Series"]

for (date, name) in zip(dates, names):
    plt.axvline(x=date, color='gray', linestyle=':', linewidth=1)
# plt.xticks(dates, names, fontsize=12)

plt.xticks([])
ax.tick_params(colors="#CCCCCC")
ax.yaxis.label.set_color("#CCCCCC")
ax.xaxis.label.set_color("#CCCCCC")
ax.title.set_color("#FFFFFF")

plt.ylabel("World Series Odds (%)",  fontsize=16, labelpad=10)
plt.xlabel("Time", fontsize=16, labelpad=10)

plt.tight_layout()

plt.xlim(left=0)
# plt.show()
plt.savefig("playoffodds.png", dpi=350)