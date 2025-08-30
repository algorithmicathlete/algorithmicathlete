import os
import time

import matplotlib.pyplot as plt
import pandas as pd
from draw_shot_chart import create_court, draw_shots, draw_shots_hex
from shotchart import get_shot_data_player, get_shot_data_team, all_teams

def draw_league_shot_chart(YEAR):
    data = pd.read_csv(f"years/{YEAR}.csv")
    return draw_shots_hex(ax, data, gridsize=35, mincount=0)

def draw_player_shot_chart(player_full_name):
    draw_shots(ax, get_shot_data_player(player_full_name))

def fetch_year(YEAR):
    if not (2000 <= YEAR <= 2024):
        raise ValueError("Has to be between 2000-2024")

    dfs = []
    for team in all_teams:
        print(f"Fetching {team['nickname']}...")
        new_df = get_shot_data_team(team["nickname"], YEAR)
        dfs.append(new_df)
        time.sleep(3)

    master_df = pd.concat(dfs, ignore_index=True)
    master_df.to_csv(f"./years/{YEAR}.csv")

if __name__ == '__main__':
    fig = plt.figure(figsize=(7, 6.8))
    ax = fig.add_axes([0, 0, 1, 1], facecolor="black")

    YEAR = 2000

    if f"{YEAR}.csv" not in os.listdir("./years"):
        fetch_year(YEAR)
        # this takes 2-ish minutes

    data = pd.read_csv(f"years/2024.csv")
    hb = draw_league_shot_chart(YEAR)
    # draw_player_shot_chart("Jordan Poole")

    create_court(ax, 'white')


    plt.show()

