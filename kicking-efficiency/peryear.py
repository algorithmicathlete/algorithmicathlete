import nfl_data_py as nfl
import pandas as pd

pbp = pd.read_csv("all_years.csv")
fg = pbp[(pbp["field_goal_attempt"] == 1) & (pbp["kick_distance"] >= 55)].copy()
fg["fg_made"] = (fg["field_goal_result"] == "made").astype(int)

season_fg = (
    fg
    .groupby("season")
    .agg(
        made=("fg_made", "sum"),
        att=("field_goal_attempt", "count"),
        fg_pct=("fg_made", "mean")
    )
    .reset_index()
)

pct_history = []
att_history = []
for _, row in season_fg.iterrows():
    print(row["season"], row["made"], row["att"], row["fg_pct"])
    pct_history.append(row["fg_pct"])
    att_history.append(row["att"])

print(pct_history)
print(att_history)