import random
import time

from bs4 import BeautifulSoup
import requests

seed_matchups = {

}

# (lower seed, higher seed) = [lower seed wins, higher seed wins]

seed_win_rates = {
    x: [0, 0] # wins, losses
    for x in range(1, 17)
}

def extract_team_data(tag):
    if len(tag.find_all("a")) < 2:
        print(tag.find("a").text)
        return {}

    seed = tag.find("span").text
    name, score = tag.find_all("a")
    return {
        "seed": int(seed),
        "name": name.text,
        "score": int(score.text)
    }

def parse_bracket(bracket):
    games = 0

    for game in bracket.find_all("div", class_=lambda x: x is None):
        if len(game.find_all("div")) < 2:
            continue

        team1, team2 = [extract_team_data(x) for x in game.find_all("div")]
        if not team1 or not team2:
            continue

        if team1["seed"] > team2["seed"]: # higher seed? switch
            team1, team2  = team2, team1

        upset = team2["score"] > team1["score"]

        key = (team1["seed"], team2["seed"])
        if key not in seed_matchups:
            seed_matchups[key] = [1 - int(upset), int(upset)]
        else:
            seed_matchups[key][int(upset)] += 1 # False = 0, True = 1

        # print(f"({team1['seed']}) {team1['name']} {team1['score']} - {team2['score']} {team2['name']} ({team2['seed']}) ")
        seed_win_rates[team1["seed"]][upset] += 1
        seed_win_rates[team2["seed"]][1-upset] += 1

        games += 1

    return games

def parse_tournament(year):
    r = requests.get(f"https://www.sports-reference.com/cbb/postseason/men/{year}-ncaa.html")
    soup = BeautifulSoup(r.content, "lxml")

    total_games = 0
    for bracket in soup.find_all("div", {"id": "bracket"}):
        total_games += parse_bracket(bracket)

    return total_games

if __name__ == '__main__':
    for year in range(1985, 2026):
        print(year)
        parse_tournament(year)
        time.sleep(3+random.random())

    print(seed_matchups)
    print(seed_win_rates)