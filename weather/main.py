import nfl_data_py as nfl

pbp = nfl.import_pbp_data([x for x in range(2016, 2025)])
pbp = pbp[(pbp["field_goal_attempt"] == 1) & (pbp["kick_distance"] > 50)]
print(list(pbp.columns))
print(pbp["kick_distance"].unique())

wind = {"heavy": [0, 0], "light": [0, 0]}
for _, attempt in pbp.iterrows():
    if attempt["wind"] >= 20:
        wind["heavy"][attempt["field_goal_result"] != "made"] += 1
    else:
        wind["light"][attempt["field_goal_result"] != "made"] += 1

print(wind)

"""
CHAOS FACTOR
punt5 blocks, fumbles, picks, muffs, penalties, free kick out of bounds, missed field goal
"""