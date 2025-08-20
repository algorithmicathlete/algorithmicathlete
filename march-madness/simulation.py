import random
from utils import calc_prob

def simulate_region():
    history = []
    matchups = [1, 16, 8, 9, 5, 12, 4, 13, 6, 11, 3, 14, 7, 10, 2, 15]

    rounds_from_region_winner = 3
    games = 0
    upsets = 0

    history.append(matchups.copy())


    while len(matchups) > 1:
        favorite, underdog = int(matchups.pop(0)), int(matchups.pop(0))
        if favorite > underdog:
            favorite, underdog = underdog, favorite

        if random.random() < calc_prob(favorite, underdog): # probability that favorite wins
            matchups.append(favorite)
        else:
            if underdog-favorite >= 5:
                upsets += 1
                matchups.append(str(underdog))
            else:
                matchups.append(underdog)

        games += 1

        if games == 2**rounds_from_region_winner:
            history.append(matchups.copy())
            games = 0
            rounds_from_region_winner -= 1

    region_winner = matchups[0]
    return history, region_winner, upsets

def final_four_matchup(a, b):
    favorite, underdog = (a, b) if int(a["seed"]) <= int(b["seed"]) else (b, a)
    fav_seed, under_seed = int(favorite['seed']), int(underdog['seed'])

    if random.random() < calc_prob(fav_seed, under_seed): # probability that favorite wins
        return favorite
    else:
        if under_seed-fav_seed >= 5:
            underdog["seed"] = str(under_seed)
        return underdog

def simulate_final_four(winners):
    winner_left = final_four_matchup(winners[0], winners[1])
    winner_right = final_four_matchup(winners[2], winners[3])
    champ = final_four_matchup(winner_left, winner_right)

    return winner_left, winner_right, champ

def simulate_march_madness(appearances):
    total_history = []
    region_winners = []
    total_upsets = 0

    for i in range(4):
        region_history, winner, upset_count = simulate_region()
        total_upsets += upset_count
        appearances[int(winner)]["final four"] += 1

        total_history.append(region_history)
        region_winners.append({
            "seed": winner,
            "region": ["South", "West", "East", "Midwest"][i]
        })

    winner_left, winner_right, champion = simulate_final_four(region_winners)

    appearances[int(winner_left['seed'])]["championship"] += 1
    appearances[int(winner_right['seed'])]["championship"] += 1
    appearances[int(champion['seed'])]["wins"] += 1

    return total_history, total_upsets, [winner_left, winner_right, champion]

def run(SIMULATIONS):
    appearances = {
        x + 1: {
            "final four": 0,
            "championship": 0,
            "wins": 0
        } for x in range(16)
    }

    total_upsets = 0
    perfect_brackets = 0

    upset_bracket = {
        "count": 0,
        "history": None,
        "final_four": None
    }

    for i in range(SIMULATIONS):
        history, upsets, final_four = simulate_march_madness(appearances)
        total_upsets += upsets

        if upsets > upset_bracket["count"]:
            upset_bracket = {
                "count": upsets,
                "history": history,
                "final_four": final_four
            }

        if upsets == 0:
            perfect_brackets += 1

    return appearances, total_upsets, perfect_brackets, upset_bracket