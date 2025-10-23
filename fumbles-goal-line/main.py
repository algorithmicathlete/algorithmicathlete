from collections import defaultdict
import nfl_data_py as nfl

pbp = nfl.import_pbp_data([x for x in range(2016, 2026)])

print([ x for x in list(pbp.columns)])

# graph of postseason win probs

fumbles = pbp[(pbp["fumble_lost"] == 1) & (pbp["yardline_100"] <= 5)]
picks = pbp[(pbp["interception"] == 1) & (pbp["yardline_100"] <= 5)]
pick_sixes = 0

fumblers =  defaultdict(int)
ball_hawks = defaultdict(int)
qbs =  defaultdict(int)

for i, row in fumbles.iterrows():
    fumblers[row["fumbled_1_player_name"]] += 1
    print(row["game_id"], row["fumbled_1_player_name"], row["yardline_100"], row["wpa"], row["epa"])

for i, row in picks.iterrows():
    pick_sixes += row["return_touchdown"]
    ball_hawks[row["interception_player_name"]] += 1
    qbs[row["passer_player_name"]] += 1
    print(row["game_id"], row["interception_player_name"], row["passer_player_name"], row["yardline_100"], row["wpa"])

print(list(sorted(fumblers.items(), key=lambda x: x[1], reverse=True)))
print(list(sorted(ball_hawks.items(), key=lambda x: x[1], reverse=True)))
print(list(sorted(qbs.items(), key=lambda x: x[1], reverse=True)))

print(fumbles.shape[0], picks.shape[0])
print(pick_sixes)