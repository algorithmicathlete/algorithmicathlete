import nfl_data_py as nfl
import numpy as np
import pandas as pd

fg = pd.read_pickle("field_goal_attempts.pkl")
fg["wp_diff"] = fg["home_wp"] - fg["next_wp"]
# fg = fg[fg["pressure_kick"]]

under_40 = fg[fg["field_goal_length"] < 40]
between_40 = fg[fg["field_goal_length"].between(40, 49)]
between_50 = fg[fg["field_goal_length"].between(50, 59)]
longer_60 = fg[fg["field_goal_length"] >= 60]

def makes_misses(d):
    att = d.shape[0]
    makes = d[d["field_goal_result"] == "made"].shape[0]
    return att, makes, round(makes/att, 3)

stuff = []
for df in [under_40, between_40, between_50, longer_60, fg]:
    att, makes, pct = makes_misses(df)
    ice_att, ice_makes, iced_pct = makes_misses(df[df["ice_attempt"]])
    non_ice_att, non_ice_makes, non_iced_pct = makes_misses(df[~df["ice_attempt"] & df["pressure_kick"]])
    non_press_att, non_press_make, non_press_pct = makes_misses(df[~df["pressure_kick"]])
    press_att, press_make, press_pct = makes_misses(df[df["pressure_kick"]])

    stuff.append([non_press_pct, iced_pct, non_iced_pct])

    print(f"{makes}/{att} ({pct}) | iced: {ice_makes}/{ice_att} ({iced_pct}) | non-iced: {non_ice_makes}/{non_ice_att} ({non_iced_pct}) | pressured: {press_make}/{press_att} ({press_pct}) | non-pressured: {non_press_make}/{non_press_att} ({non_press_pct})")

print(stuff)
cols_to_show = [
    "game_id","posteam","defteam","posteam_score","defteam_score",
    "game_seconds_remaining","field_goal_result", "ice_attempt",
    "field_goal_length", "kick_distance", "kicker_player_name", "wp_diff"
]

fg_sorted = fg.loc[fg["pressure_kick"], cols_to_show].sort_values(
    by="wp_diff", key=np.abs, ascending=False
)

print(fg_sorted.to_string(index=False))

pressure_kicks = fg[fg["pressure_kick"]]
kickers = {}
for name, group in pressure_kicks.groupby("kicker_player_name"):
    att, makes, pct = makes_misses(group)
    kickers[name] = {"makes": makes, "att": att, "pct": pct}

for k, v in sorted(kickers.items(), key=lambda x: x[1]["att"], reverse=True):
    if v["att"] >= 10:
        print(k, v)
print(list(fg.columns))