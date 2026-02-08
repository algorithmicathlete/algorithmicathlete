import random
import time

import requests
from bs4 import BeautifulSoup

r = requests.get("https://www.pro-football-reference.com/teams/chi/2025.htm")
soup = BeautifulSoup(r.content, "lxml")

table = soup.select_one("table#games").find("tbody")

total_fpd = [0]
total_spd = [0]

fpd_independent = []
spd_independent = []

for row in table.find_all("tr"):
    game = row.find_all(["td", "th"])
    if game[4].text:
        print(game[0].text, game[4].find('a')['href'])
        r = requests.get(f"https://www.pro-football-reference.com{game[4].find('a')['href']}")
        soup = BeautifulSoup(r.content, "lxml")
        boxscore = soup.find("table", {"class": "linescore"}).find("tbody")
        fpd = spd = 0
        for team in boxscore.find_all("tr"):
            name, q1, q2, q3, q4, *extra = [i.text for i in team.find_all(["td", "th"])[1:]]
            if name == "Chicago Bears":
                fpd += int(q1) + int(q2)
                spd += int(q3) + int(q4)
            else:
                fpd -= int(q1) + int(q2)
                spd -= int(q3) + int(q4)
            print(name, q1, q2, q3, q4)
        print(f"First half PD: {fpd} | Second half PD: {spd}")
        total_fpd.append(total_fpd[-1]+fpd)
        total_spd.append(total_spd[-1] + spd)

        fpd_independent.append(fpd)
        spd_independent.append(spd)
        print()

    time.sleep(3+random.random()-0.5)

print(total_fpd)
print(total_spd)
print()
print(fpd_independent)
print(spd_independent)