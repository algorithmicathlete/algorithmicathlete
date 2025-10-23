import time

import requests
from bs4 import BeautifulSoup

def fetch_standings(year, week):
    r = requests.get(f"https://www.pro-football-reference.com/boxscores/standings.cgi?week={week}&year={year}")
    soup = BeautifulSoup(r.content, "lxml")

    afc, nfc = soup.find("div", {"id": "all_AFC"}), soup.find("div", {"id": "all_NFC"})
    rows = []
    for row in afc.find_all("tr") + nfc.find_all("tr"):
        team = [i.text for i in row.find_all("td")]
        if len(team) <= 1:
            continue
        rows.append([row.find("th").text] + team)

    return rows


def started_with_two_losses(year):
    started = set()
    for team in fetch_standings(year, 3):
        name, wins, losses, *extra = team
        name = name.strip("+*")

        if int(losses) == 3:
            started.add(name)

    return started

year_counts = {}
team_counts = {'Patriots': 0, 'Jets': 0, 'Bills': 0, 'Dolphins': 0, 'Bengals': 0, 'Steelers': 0, 'Browns': 0, 'Ravens': 0, 'Jaguars': 0, 'Titans': 0, 'Texans': 0, 'Colts': 0, 'Broncos': 0, 'Chiefs': 0, 'Raiders': 0, 'Chargers': 0, 'Cowboys': 0, 'Redskins': 0, 'Eagles': 0, 'Giants': 0, 'Packers': 0, 'Vikings': 0, 'Lions': 0, 'Bears': 0, 'Panthers': 0, 'Falcons': 0, 'Buccaneers': 0, 'Saints': 0, 'Cardinals': 0, 'Rams': 0, '49ers': 0, 'Seahawks': 0}
playoffs = []
all_teams = {}
total_wins = total_losses = total_ties = 0

for year in range(2000, 2025):
    started = started_with_two_losses(year)
    year_counts[year] = len(started)
    for team in started:
        team_counts[team.split()[-1]] += 1

    for team in fetch_standings(year, 18):
        name, wins, losses, ties, *extra = team
        if name.strip("+*") in started:
            total_wins += int(wins)
            total_losses += int(losses)
            all_teams[f"{year} {name.strip('+*')}"] = [wins, losses, ties]
            if not ties.startswith("."):
                total_ties += int(ties)
            print(name, f"{wins}-{losses}")
            if "*" in name or "+" in name:
                playoffs.append(f"{year} {name} {wins}-{losses}")

    print("\n"*2)
    time.sleep(5)


print(total_wins, total_losses, total_ties)
print((total_wins + 0.5*total_ties)/(total_wins+total_losses+total_ties))
print(playoffs)
print(year_counts)
print(team_counts)
print(all_teams)