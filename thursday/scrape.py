import requests
from bs4 import BeautifulSoup, Comment
from datetime import datetime


# r = requests.get("https://www.pro-football-reference.com/years/2024/fantasy.htm")
r = requests.get("https://www.pro-football-reference.com/players/B/BarkSa00/fantasy/2024/")
soup = BeautifulSoup(r.content, "lxml")

cols = [
    "G#", "Date", "Tm", "Home", "Opp", "Result", "Pos",
    "Att", "Yds", "TD",        # Passing/Rushing attempts
    "Tgt", "Rec", "Yds", "TD", # Receiving targets/receptions
    "Att", "Yds", "TD",        # Rushing again
    "Tgt", "Rec", "Yds", "TD", # More receiving?
    "Num", "Pct", "Num", "Pct", "Num", "Pct",  # Snap counts / % splits
    "FantPt", "DKPt", "FDPt"   # Fantasy scoring systems
]

table = soup.find("tbody")
last_date = None
points = 0
games = 0
for row in table.find_all("tr"):
    player = [x.text for x in row.find_all("td")]
    date = datetime.strptime(player[cols.index("Date")], "%Y-%m-%d")

    row = [
        "Saquon Barkley",
        int(player[cols.index("G#")]),
        date.isoweekday(),
        player[cols.index("Opp")],
        player[cols.index("Home")] != "@",
        (date - last_date).days if last_date else None,
        round(points / games, 1) if games > 0 else 0,
        float(player[cols.index("FantPt")]),
    ]
    games += 1
    points += float(player[cols.index("FantPt")])
    print(row)
    last_date = date

# cols = [
#     "Player", "Tm", "FantPos", "Age", "G", "GS",
#     "Pass_Cmp", "Pass_Att", "Pass_Yds", "Pass_TD", "Pass_Int",
#     "Rush_Att", "Rush_Yds", "Rush_Y/A", "Rush_TD",
#     "Rec_Tgt", "Rec", "Rec_Yds", "Rec_Y/R", "Rec_TD",
#     "Fmb", "FL", "Misc_TD", "2PM", "2PP",
#     "FantPt", "PPR", "DKPt", "FDPt", "VBD", "PosRank", "OvRank"
# ]
#
# table = soup.find("tbody")
# for row in table.find_all("tr"):
#     player = [x for x in row.find_all("td")]
#     if player and player[cols.index("FantPos")].text == "RB":
#         print(player[0].text, player[0].find("a")["href"].replace(".htm", "/fantasy/2024/"))