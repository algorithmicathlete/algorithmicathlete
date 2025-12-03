import pandas as pd
import requests
from bs4 import BeautifulSoup
from matplotlib import image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.google.com/",
}


r = requests.get("https://www.espn.com/nfl/standings/_/group/league", headers=headers)
soup = BeautifulSoup(r.content, "lxml")
rows = []

for team, info in zip(*[x.find_all("tr") for x in soup.find_all("tbody")]):
    stats = [x.text for x in info.find_all("td")]
    rows.append({
        "TEAM": team.find("span", class_="hide-mobile").text,
        "RECORD": float(stats[3]),
        "POINT_DIFF": int(stats[-2].strip("+"))
    })

print(rows)

df = pd.DataFrame(rows)
df = df.sort_values("RECORD", ascending=False)
print(df)

team_to_abbr = {
    "Arizona Cardinals": "ARI",
    "Atlanta Falcons": "ATL",
    "Baltimore Ravens": "BAL",
    "Buffalo Bills": "BUF",
    "Carolina Panthers": "CAR",
    "Chicago Bears": "CHI",
    "Cincinnati Bengals": "CIN",
    "Cleveland Browns": "CLE",
    "Dallas Cowboys": "DAL",
    "Denver Broncos": "DEN",
    "Detroit Lions": "DET",
    "Green Bay Packers": "GB",
    "Houston Texans": "HOU",
    "Indianapolis Colts": "IND",
    "Jacksonville Jaguars": "JAX",
    "Kansas City Chiefs": "KC",
    "Las Vegas Raiders": "LV",
    "Los Angeles Chargers": "LAC",
    "Los Angeles Rams": "LAR",
    "Miami Dolphins": "MIA",
    "Minnesota Vikings": "MIN",
    "New England Patriots": "NE",
    "New Orleans Saints": "NO",
    "New York Giants": "NYG",
    "New York Jets": "NYJ",
    "Philadelphia Eagles": "PHI",
    "Pittsburgh Steelers": "PIT",
    "San Francisco 49ers": "SF",
    "Seattle Seahawks": "SEA",
    "Tampa Bay Buccaneers": "TB",
    "Tennessee Titans": "TEN",
    "Washington Commanders": "WAS"
}

team_colors = {
    "ARI": "#97233F",  # Arizona Cardinals
    "ATL": "#A71930",  # Atlanta Falcons
    "BAL": "#241773",  # Baltimore Ravens
    "BUF": "#00338D",  # Buffalo Bills
    "CAR": "#0085CA",  # Carolina Panthers
    "CHI": "#C83803",  # Chicago Bears
    "CIN": "#FB4F14",  # Cincinnati Bengals
    "CLE": "#FF3C00",  # Cleveland Browns
    "DAL": "#869397",  # Dallas Cowboys
    "DEN": "#FB4F14",  # Denver Broncos
    "DET": "#0076B6",  # Detroit Lions
    "GB": "#203731",  # Green Bay Packers
    "HOU": "#A71930",  # Houston Texans
    "IND": "#002C5F",  # Indianapolis Colts
    "JAX": "#006778",  # Jacksonville Jaguars
    "KC": "#E31837",  # Kansas City Chiefs
    "LV": "#A5ACAF",  # Las Vegas Raiders
    "LAC": "#0080C6",  # Los Angeles Chargers
    "LAR": "#003594",  # Los Angeles Rams
    "MIA": "#008E97",  # Miami Dolphins
    "MIN": "#4F2683",  # Minnesota Vikings
    "NE": "#C60C30",  # New England Patriots
    "NO": "#D3BC8D",  # New Orleans Saints
    "NYG": "#0B2265",  # New York Giants
    "NYJ": "#125740",  # New York Jets
    "PHI": "#004C54",  # Philadelphia Eagles
    "PIT": "#FFB612",  # Pittsburgh Steelers
    "SF": "#AA0000",  # San Francisco 49ers
    "SEA": "#002244",  # Seattle Seahawks
    "TB": "#D50A0A",  # Tampa Bay Buccaneers
    "TEN": "#4B92DB",  # Tennessee Titans
    "WAS": "#773141"   # Washington Commanders
}

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12,6))
fig.set_facecolor("#000000")
ax.set_facecolor("#111111")

# ax.axhline(0, color='white', lw=0.5)
# ax.axvline(16.5, color='white', linestyle="--", lw=0.7)
# ax.axvline(19.5, color='white', linestyle="--", lw=0.7)
# plt.axvspan(16.5, 19.5, color='gray', alpha=0.3)
#
#
# plt.text(18, 110, ".500 Zone", color='white', fontsize=10, ha='center')
#
# ax.bar(df["TEAM"], df["POINT_DIFF"], color=[team_colors[team_to_abbr[x.strip('*+')]] for x in df["TEAM"]])
ax.scatter(df["POINT_DIFF"], df["RECORD"], alpha=0)

for i, txt in enumerate(df["TEAM"]):
    top = df["POINT_DIFF"].iloc[i] > 0

    ax.annotate(("+" if top else "")+str(df["POINT_DIFF"].iloc[i]), (i, df["POINT_DIFF"].iloc[i]+(0.5 if top else -2)), ha="center", va="bottom" if top else "top", fontsize=10, color="white")

    path = f"../nfl_logos/{team_to_abbr[txt.strip('*+')].lower()}.png"
    logo = mpimg.imread(path)
    imagebox = OffsetImage(logo, zoom=0.28)
    # ab = AnnotationBbox(imagebox, (i, top*-19 + 9), frameon=False)
    ab = AnnotationBbox(imagebox, (df["POINT_DIFF"].iloc[i], df["RECORD"].iloc[i]), frameon=False)
    plt.gca().add_artist(ab)

for i, spine in enumerate(ax.spines.values()):
    spine.set_color("#cccccc")

# plt.xticks([])
# plt.yticks([])
plt.tick_params(axis='x', colors='white')
plt.tick_params(axis='y', colors='white')

# plt.xlabel(f"← Better Record{' '*140}Worse Record →", fontsize=12, fontweight="bold", color="#CCCCCC", labelpad=10)
plt.xlabel(f"Point Differential", fontsize=12, fontweight="bold", color="#CCCCCC")
plt.ylabel(f"Win %", fontsize=12, fontweight="bold", color="#CCCCCC")

# ax.set_title("NFL Point Differential (Sorted by Team Record)", fontweight='bold', fontsize=14, color="#CCCCCC")
ax.set_title("Win % vs. Point Differential", fontweight='bold', fontsize=14, color="#CCCCCC")

ax.axvline(0, color='white', linestyle="--", lw=1, alpha=0.5)
ax.axhline(0.5, color='white', linestyle="--", lw=1, alpha=0.5)

import numpy as np
from scipy.stats import linregress

x = df["POINT_DIFF"]
y = df["RECORD"]

slope, intercept, r_value, p_value, std_err = linregress(x, y)

# Create a sorted version for the line
x_sorted = np.sort(x)
trendline_sorted = slope * x_sorted + intercept


print(r_value, slope, intercept)
# Plot trendline (sorted order prevents the zig-zag)
plt.plot(
    x_sorted,
    trendline_sorted,
    color="white",
    alpha=0.5,
    linestyle="--",
    label=f"Trendline (r={r_value:.3f})"
)

plt.tight_layout()
# plt.show()


plt.savefig("nflpointdifferentialtrendline.png", dpi=350)
# NFL Point Differential, Sorted by Team Record
#  the bucs and the bears are the only teams above .500 with negaitve point differentials. no team below .500 has a positive PD
# sorted left to right by win%
"""
The Bucs and the Bears are the only teams above .500 with negative point differentials.

No team below .500 has a positive PD.

Sorted left-to-right, by win%.
"""