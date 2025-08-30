import nfl_data_py as nfl

pbp = nfl.import_pbp_data([2024])
pbp = pbp[pbp["season_type"] == "REG"]

teams = ['MIA', 'DET', 'ATL', 'KC', 'LV', 'WAS', 'NYJ', 'SEA', 'PIT', 'PHI', 'LA', 'DEN', 'HOU', 'ARI', 'BAL', 'DAL', 'JAX', 'BUF', 'IND', 'GB', 'CLE', 'NE', 'TEN', 'CAR', 'MIN', 'SF', 'LAC', 'NO', 'TB', 'CIN', 'CHI', 'NYG']

gwd = {x: 0 for x in teams}
gld = {x: 0 for x in teams}
records = {x: [0,0] for x in teams}

for game_id, game in pbp.groupby("game_id"):
    game = game.sort_values("order_sequence")
    final_home, final_away = [game[f"total_{x}_score"].iloc[-1] for x in ["home", "away"]]
    winner, loser = ("home", "away") if final_home > final_away else ("away", "home")
    win_team, lose_team = [game[f"{x}_team"].unique()[0] for x in (winner, loser)]

    records[win_team][0] += 1
    records[lose_team][1] += 1

    print(win_team, "beat", lose_team)

    for drive_id, drive in game.groupby("drive"):
        drive = drive.sort_values("order_sequence")

        offense_scored = drive[(drive["pass_touchdown"] == 1) | (drive["rush_touchdown"] == 1) | (drive["field_goal_result"] == "made")]
        if offense_scored.empty:
            continue

        pre_home, pre_away = [drive[f"total_{x}_score"].iloc[0] for x in ["home", "away"]]
        post_home, post_away = [drive[f"total_{x}_score"].iloc[-1] for x in ["home", "away"]]

        if (winner == "home" and post_home > post_away and pre_home <= pre_away) or (winner == "away" and post_away > post_home and pre_home >= pre_away):
            if drive["qtr"].iloc[-1] >= 4:
                print(game_id, f"{win_team} won {lose_team} blew it")
                gwd[win_team] += 1
                gld[lose_team] += 1
                break

actual = {'MIA': 3, 'DET': 4, 'ATL': 3, 'KC': 7, 'LV': 2, 'WAS': 5, 'NYJ': 3, 'SEA': 4, 'PIT': 2, 'PHI': 4, 'LA': 5, 'DEN': 3, 'HOU': 2, 'ARI': 3, 'BAL': 2, 'DAL': 1, 'JAX': 2, 'BUF': 2, 'IND': 5, 'GB': 3, 'CLE': 2, 'NE': 1, 'TEN': 2, 'CAR': 4, 'MIN': 5, 'SF': 1, 'LAC': 2, 'NO': 1, 'TB': 2, 'CIN': 2, 'CHI': 1}
print(actual)
print()

print(gwd)
print(gld)
print(records)

for k, v in gwd.items():
    records[k][0] -= v
    records[k][1] += v

for k, v in gld.items():
    records[k][0] += v
    records[k][1] -= v

print(records)


print(list(pbp.columns))
print(pbp["touchdown"].unique())
print(pbp["field_goal_result"].unique())
print(pbp["pass_touchdown"].unique())


