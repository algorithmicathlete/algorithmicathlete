import numpy as np
from bs4 import BeautifulSoup
from matplotlib import image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

with open("history.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

table = soup.find("table")
cowboys = []
lions = []
year = 1966
for row in table.find_all("tr"):
    try:
        t1, t2 = row.text.lower().replace("(ot)", "").strip().split(",")
        t1score, t2score = [int(x.split()[-1]) for x in (t1, t2)]
        t1win = 1 if t1score > t2score else 0 if t1score == t2score else -1
        if "detroit lions" in t1 or "detroit lions" in t2:
            lions_win = t1win * (-1 if "detroit lions" in t2 else 1)
            lions.append(lions_win)
            if len(lions) == 5:
                lions += [np.nan] * 6
        elif "dallas cowboys" in t1 or "dallas cowboys" in t2:
            cowboys_win = t1win * (-1 if "dallas cowboys" in t2 else 1)
            cowboys.append(cowboys_win)
            year += 1
            if year == 1975 or year == 1977:
                cowboys.append(np.nan)
    except ValueError:
        pass

print(cowboys)
print(lions)
cowboys.append(1)
lions.append(1)
# both won 2024
cowboys.append(1)
lions.append(-1)
# cowboys win lions lose

def cumulative(results):
    wins = 0
    ties = 0
    cumulative_win_pct = []
    nans = 0

    for i, r in enumerate(results, start=1):
        if r == 1:
            wins += 1
        elif r == 0:
            ties += 1
        elif np.isnan(r):
            nans += 1

        win_pct = (wins + 0.5 * ties) / (i-nans)
        cumulative_win_pct.append(win_pct)

    return cumulative_win_pct


import matplotlib.pyplot as plt

remove_first = 3
lions_curve = cumulative(lions)[remove_first:]
cowboys_curve = cumulative(cowboys)[remove_first:]
print(len(cowboys))
# Shift Cowboys 32 seasons to the right
shift = 32
cowboys_shifted = np.concatenate([np.full(shift+remove_first, np.nan), cowboys_curve])
lions_shifted = np.concatenate([np.full(remove_first, np.nan), lions_curve])


years = np.arange(1934, 2026)   # 1932 through 2025 inclusive

fig, ax = plt.subplots(figsize=(10, 5))
ax.set_facecolor("#111111")
fig.patch.set_facecolor("#000000")
for spine in ax.spines.values():
    spine.set_color("#888888")


ax.yaxis.label.set_color("#CCCCCC")
ax.xaxis.label.set_color("#CCCCCC")

plt.tick_params(axis='x', colors='white')
plt.tick_params(axis='y', colors='white')

plt.plot(years, lions_shifted, marker='.', label="Lions", linewidth=1, color="#0076B6")
plt.plot(years, cowboys_shifted, marker='.', label="Cowboys", linewidth=1, color="#869397")

def draw_team(path, x, y, record, zoom=0.3, minus=0.4):
    logo = mpimg.imread(path)
    imagebox = OffsetImage(logo, zoom=zoom)
    ab = AnnotationBbox(imagebox, (x, y), frameon=False)
    plt.gca().add_artist(ab)

    plt.text(x, y - minus, record, color='white', fontsize=11, ha='center', va='bottom', fontweight='bold')


draw_team(f"Detroit_Lions_logo.svg.png", 1960, 0.42, f"{lions.count(1)}-{lions.count(-1)}-{lions.count(0)}", minus=0.085, )
draw_team(f"Dallas_Cowboys.svg.png", 2005, 0.8, f"{cowboys.count(1)}-{cowboys.count(-1)}-{cowboys.count(0)}", minus=0.1)

plt.text(1941, 0.61, "WW2", color='white', fontsize=8, ha='center', va='bottom', fontweight='bold')

plt.ylabel("Win %", fontsize=14)

def win_p_calc(wins, ties, losses):
    print(f"{wins}-{losses}-{ties}")
    return (wins + 0.5 * ties) / (wins+ties+losses)

plt.xlim(left=1933)
plt.tight_layout()
# plt.show()
plt.savefig("thanksgivingovertime.png", dpi=350)

labels = ["Lions", "Cowboys"]
categories = ["Thanksgiving", "Total"]
ranges = [
    [win_p_calc(lions.count(1), lions.count(0), lions.count(-1)), win_p_calc(613, 34, 714)],
    [win_p_calc(cowboys.count(1), cowboys.count(0), cowboys.count(-1)), win_p_calc(575, 7, 428)]
]
data = np.array(ranges)

# Plot positions
x = np.array([0, 0.75])
print(x)
width = 0.25

fig, ax = plt.subplots(figsize=(5, 5), facecolor="black")
fig.patch.set_facecolor("black")
ax.set_facecolor("black")

ax.tick_params(colors="white")
for i, spine in enumerate(ax.spines.values()):
    if i in [0, 2]:
        spine.set_color("white")

# Plot bars for each category
for i in range(data.shape[1]):
    ax.bar(x + (i - 0.5) * width, data[:, i], width, label=categories[i], color=["#E3A447", "#3A5FCD"][i], alpha=0.9)

ax.set_ylabel("Win%", color="white")
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend(facecolor="black", edgecolor="none", labelcolor="white")
ax.set_ylim(0, 1)  # keep scale as percentages

plt.tight_layout()

plt.savefig("thanksgivingvsnormal.png", dpi=350)


print(cumulative(lions))
print(cumulative(cowboys))