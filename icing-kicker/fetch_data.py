import nfl_data_py as nfl

pbp = nfl.import_pbp_data([x for x in range(2015, 2026)])
pbp = pbp.sort_values(["game_id", "order_sequence"])
pbp["prev_desc"] = pbp.groupby("game_id")["desc"].shift(1)

pbp["next_wp"] = pbp.groupby("game_id")["home_wp"].shift(-1)


fg = pbp[pbp["field_goal_attempt"] == 1].copy()

fg["close_score"] = (fg["defteam_score"] - fg["posteam_score"]).between(0, 3)
fg["late_in_game"] = fg["game_seconds_remaining"] < 120
fg["pressure_kick"] = fg["close_score"] & fg["late_in_game"]

# fg = fg[fg["pressure_kick"]]

fg["field_goal_length"] = fg["yardline_100"] + 18.0
fg["ice_attempt"] = (
    fg["pressure_kick"]
    & fg["prev_desc"].str.contains("Timeout", na=False)
    & fg.apply(lambda row: row["defteam"] in row["prev_desc"], axis=1)
)

fg.to_pickle("field_goal_attempts.pkl")