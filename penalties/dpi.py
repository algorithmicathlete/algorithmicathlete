import requests
from bs4 import BeautifulSoup
import pandas as pd
from matplotlib import image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

r = requests.get("https://www.nflpenalties.com/penalty/defensive-pass-interference?year=2025")
soup = BeautifulSoup(r.content, "lxml")

table = soup.find("tbody")
rows = []
for row in table.find_all("tr"):
    team = [i.text for i in row.find_all("td")]
    rows.append({
        "TEAM": team[0],
        "DIFF": int(team[-4])-int(team[3])
    })

df = pd.DataFrame(rows)
df = df.sort_values("DIFF", ascending=False)

team_to_abbr = {
    "Arizona": "ARI",
    "Atlanta": "ATL",
    "Baltimore": "BAL",
    "Buffalo": "BUF",
    "Carolina": "CAR",
    "Chicago": "CHI",
    "Cincinnati": "CIN",
    "Cleveland": "CLE",
    "Dallas": "DAL",
    "Denver": "DEN",
    "Detroit": "DET",
    "Green Bay": "GB",
    "Houston": "HOU",
    "Indianapolis": "IND",
    "Jacksonville": "JAX",
    "Kansas City": "KC",
    "Las Vegas": "LV",
    "LA Chargers": "LAC",
    "LA Rams": "LAR",
    "Miami": "MIA",
    "Minnesota": "MIN",
    "New England": "NE",
    "New Orleans": "NO",
    "N.Y. Giants": "NYG",
    "N.Y. Jets": "NYJ",
    "Philadelphia": "PHI",
    "Pittsburgh": "PIT",
    "San Francisco": "SF",
    "Seattle": "SEA",
    "Tampa Bay": "TB",
    "Tennessee": "TEN",
    "Washington": "WAS"
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
fig.set_facecolor("#111111")
ax.set_facecolor("#111111")

ax.bar(df["TEAM"], df["DIFF"], color=[team_colors[team_to_abbr[x.strip('*+')]] for x in df["TEAM"]])
ax.axhline(0, color='white', lw=0.5)

for i, txt in enumerate(df["TEAM"]):
    top = df["DIFF"].iloc[i] > 0

    ax.annotate(("+" if top else "")+str(df["DIFF"].iloc[i]), (i, df["DIFF"].iloc[i]+(0.5 if top else -2)), ha="center", va="bottom" if top else "top", fontsize=9, color="white")

    path = f"../nfl_logos/{team_to_abbr[txt.strip('*+')].lower()}.png"
    logo = mpimg.imread(path)
    imagebox = OffsetImage(logo, zoom=0.28)
    ab = AnnotationBbox(imagebox, (i, top*-20 + 10), frameon=False)
    plt.gca().add_artist(ab)

for i, spine in enumerate(ax.spines.values()):
    spine.set_color("#111111")

# plt.ylim(bottom=-5)
plt.title("Net Defensive Pass Interference Yardage", color="white", alpha=0.8, fontsize=16, fontweight="bold")
plt.xticks([])
plt.yticks([])
plt.tight_layout()

ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)

# plt.show()
plt.savefig("dpinet.png", dpi=350)
