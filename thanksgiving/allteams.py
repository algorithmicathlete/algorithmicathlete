import pandas as pd
from matplotlib import image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

team_records = """Arizona Cardinals: 6-15-2
Atlanta Falcons: 1-3
Baltimore Ravens: 2-1
Buffalo Bills: 6-4-1
Carolina Panthers: 1-0
Chicago Bears: 20-16-2
Cincinnati Bengals: 1-1
Cleveland Browns: 3-3
Dallas Cowboys: 35-22-1
Denver Broncos: 4-7
Detroit Lions: 38-46-2
Green Bay Packers: 17-20-2
Houston Texans: 2-0
Indianapolis Colts: 2-1-1
Jacksonville Jaguars: 0-0
Kansas City Chiefs: 5-6
Las Vegas Raiders: 4-4
Los Angeles Chargers: 3-1-1
Los Angeles Rams: 4-1
Miami Dolphins: 5-3
Minnesota Vikings: 7-2
New England Patriots: 3-3
New Orleans Saints: 3-1
New York Giants: 7-7-3
New York Jets: 4-4
Philadelphia Eagles: 6-1
Pittsburgh Steelers: 2-6
San Francisco 49ers: 3-2-1
Seattle Seahawks: 2-3
Tampa Bay Buccaneers: 0-1
Tennessee Titans: 5-2
Washington Commanders: 4-9"""

rows = []
for team in team_records.split("\n"):
    name, record = team.split(": ")
    wins, losses, *ties = record.split("-")
    ties = 0 if not ties else int(ties[0])
    wins, losses = int(wins), int(losses)
    gp = (wins+ties+losses)
    rows.append({
        "TEAM": name,
        "WINS": max(wins, 0.1),
        "WIN_PERC": (wins + 0.5*ties) / gp if gp > 0 else 0,
        "GP": gp
    })

df = pd.DataFrame(rows)
df = df.sort_values("WINS", ascending=False)

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

ax.bar(df["TEAM"], df["WINS"], color=[team_colors[team_to_abbr[x.strip('*+')]] for x in df["TEAM"]])


for i, txt in enumerate(df["TEAM"]):
    ax.annotate(str(int(df["WINS"].iloc[i])), (i, df["WINS"].iloc[i]), ha="center", va="bottom", fontsize=11, color="white")

    path = f"../nfl_logos/{team_to_abbr[txt.strip('*+')].lower()}.png"
    logo = mpimg.imread(path)
    imagebox = OffsetImage(logo, zoom=0.28)
    ab = AnnotationBbox(imagebox, (i, -1.25), frameon=False)
    plt.gca().add_artist(ab)

for i, spine in enumerate(ax.spines.values()):
    spine.set_color("#CCCCCC")

plt.title("Thanksgiving Day Wins", fontweight="bold", fontsize=16, color="white")
plt.ylim(bottom=-5)
plt.xticks([])
plt.yticks([])
plt.tight_layout()

ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)

plt.savefig("allteamsthanksgiving2.png", dpi=350)