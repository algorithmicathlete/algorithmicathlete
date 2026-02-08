from collections import defaultdict

import requests
from bs4 import BeautifulSoup

r = requests.get("https://www.nba.com/news/nba-on-christmas-day-all-time-results")

soup = BeautifulSoup(r.content, "lxml").find("div", {"class": "ArticleContent_article__NBhQ8"})

historical_to_modern = {
    # Lakers
    "Minneapolis Lakers": "Los Angeles Lakers",

    # Warriors
    "Philadelphia Warriors": "Golden State Warriors",
    "San Francisco Warriors": "Golden State Warriors",

    # Pistons
    "Fort Wayne Zollner Pistons": "Detroit Pistons",
    "Fort Wayne Pistons": "Detroit Pistons",

    # Hawks
    "Tri-Cities Blackhawks": "Atlanta Hawks",
    "Milwaukee Hawks": "Atlanta Hawks",
    "St. Louis Hawks": "Atlanta Hawks",

    # Kings
    "Rochester Royals": "Sacramento Kings",
    "Cincinnati Royals": "Sacramento Kings",
    "Kansas City-Omaha Kings": "Sacramento Kings",
    "Kansas City Kings": "Sacramento Kings",

    # 76ers
    "Syracuse Nationals": "Philadelphia 76ers",

    # Clippers
    "San Diego Clippers": "LA Clippers",

    # Rockets
    "San Diego Rockets": "Houston Rockets",

    # Jazz
    "New Orleans Jazz": "Utah Jazz",

    # Nets
    "New Jersey Nets": "Brooklyn Nets",

    # Pelicans
    "New Orleans Hornets": "New Orleans Pelicans",

    # Grizzlies
    "Vancouver Grizzlies": "Memphis Grizzlies",

    # Thunder
    "Seattle SuperSonics": "Oklahoma City Thunder",

    # Wizards
    "Chicago Packers": "Washington Wizards",
    "Baltimore Bullets": "Washington Wizards",
    "Capital Bullets": "Washington Wizards",
    "Washington Bullets": "Washington Wizards",
}

defunct_teams = {
    "Chicago Stags",
    "Providence Steamrollers",
    "Washington Capitols",
    "St. Louis Bombers",
    "Anderson Duffey Packers",
    "Sheboygan Redskins",
    # "Denver Nuggets (1949)",  # NOT the modern Nuggets
    "Waterloo Hawks",
    "Indianapolis Olympians",
    "Buffalo Braves",  # lineage technically Clippers, but usually treated as defunct
}

records = defaultdict(lambda: {"wins": 0, "losses": 0})

x = 0
for li in soup.find_all("li"):
    game = li.text.split("(")[0].strip()
    winner, loser = [" ".join(x.strip().split()[:-1]) for x in game.split("vs." if "vs." in game else " at ")]
    if winner in historical_to_modern:
        winner = historical_to_modern[winner]
    if loser in historical_to_modern:
        loser = historical_to_modern[loser]

    if winner not in defunct_teams:
        records[winner]["wins"] += 1
    if loser not in defunct_teams and game != "Sheboygan Redskins 76 at Denver Nuggets 72":
        records[loser]["losses"] += 1
    x+= 1

print(x)

print(records)