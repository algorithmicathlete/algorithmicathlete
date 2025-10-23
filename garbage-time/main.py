import nfl_data_py as nfl
import pandas as pd

pbp = nfl.import_pbp_data([2024])
pbp = pbp[pbp["qtr"] == 4]

print([ x for x in list(pbp.columns)])

# passes = pbp[(pbp["pass"] == 1) & (pbp["qtr"] == 4)]
#
# for i, row in pass_tds.sort_values(by='wpa', ascending=False).iterrows():
#     print(row["wpa"], row["qtr"], row["quarter_seconds_remaining"], row["total_home_score"], row["total_away_score"], row["posteam"], row["passer_player_name"])


from collections import defaultdict

stats = defaultdict(lambda: {"completions": 0, "attempts": 0, "yards": 0, "tds": 0, "ints": 0})

for game_id, game in pbp.groupby("game_id"):
    game = game.sort_values("order_sequence")

    for drive_id, drive in game.groupby("drive"):
        drive = drive.sort_values("order_sequence")
        starting_wp = drive.iloc[0]["wp"]
        off_score, def_score = drive.iloc[0]["posteam_score"], drive.iloc[0]["defteam_score"]

        if starting_wp < 0.05:
            print(starting_wp, drive["game_id"].unique(), drive["posteam"].unique(), drive.iloc[0]["wp"],
                  drive.iloc[0]["posteam_score"], drive.iloc[0]["defteam_score"],
                  drive.iloc[0]["quarter_seconds_remaining"])

            for i, play in drive.iterrows():
                name = play["passer_player_name"]
                if play["pass"]:
                    if play["incomplete_pass"]:
                        stats[name]["attempts"] += 1
                    elif play["interception"]:
                        stats[name]["attempts"] += 1
                        stats[name]["ints"] += 1
                    elif pd.notna(play["pass_length"]):
                        stats[name]["attempts"] += 1
                        stats[name]["completions"] += 1
                        stats[name]["tds"] += play["pass_touchdown"]
                        stats[name]["yards"] += play["yards_gained"]


def calc_passer_rating(qb):
    a = max(0.0, min(2.375, ((qb["completions"] / qb["attempts"]) - 0.3) * 5))
    b = max(0.0, min(2.375, ((qb["yards"] / qb["attempts"]) - 3) * 0.25))
    c = max(0.0, min(2.375, (qb["tds"] / qb["attempts"]) * 20))
    d = max(0.0, min(2.375, 2.375 - ((qb["ints"] / qb["attempts"]) * 25)))

    return ((a+b+c+d) / 6) * 100


for k, v in stats.items():
    print(k, v, calc_passer_rating(v))

# fumbles = pbp[(pbp["fumble_lost"] == 1) & (pbp["yardline_100"] >= 95)]
#
# for i, row in fumbles.iterrows():
#     print(row["game_id"], row["fumbled_1_player_name"])

# keep on back burner