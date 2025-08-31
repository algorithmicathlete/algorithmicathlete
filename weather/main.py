import nfl_data_py as nfl

pbp = nfl.import_pbp_data([2024])
pbp = pbp[pbp["field_goal_attempt"]]

# temp, wind, weahter
for x in pbp.columns:
    print(x)

print(pbp["weather"].unique())
print(pbp["wind"].unique())

print(pbp["temp"].unique())
print(pbp["run_gap"].unique())

"""
CHAOS FACTOR
punt5 blocks, fumbles, picks, muffs, penalties, free kick out of bounds, missed field goal
"""