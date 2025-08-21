import time

from bs4 import BeautifulSoup
import requests

def scrape_top_players(year):
    r = requests.get(f"https://www.fantasypros.com/nfl/adp/ppr-overall.php?year={year}")
    soup = BeautifulSoup(r.content, "lxml")

    table = soup.find("tbody")

    players = {}

    for i, row in enumerate(table.find_all("tr")[:12]):
        player = row.find_all("td")[1].find("a").text
        players[player] = {
            "ADP": i+1,
            "PosRank": int(row.find_all("td")[2].text[2:])
        }

    return players

if __name__ == '__main__':
    top_players = {}
    for i in range(2015, 2025):
        top_players[i] = scrape_top_players(i)
        time.sleep(1)

    print(top_players)
