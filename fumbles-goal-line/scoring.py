import pandas as pd
import nfl_data_py as nfl
from plot import epa_scatter, beeswarm, gl_score_rate_bar


pbp = nfl.import_pbp_data([2025])

gl = pbp.loc[
    (pbp["posteam"].notna()) &
    (pbp["drive"].notna()) &
    (pbp["yardline_100"].notna()) &
    (pbp["yardline_100"] <= 5),
    ["game_id", "drive", "posteam"]
].drop_duplicates()

gl["gl_drive"] = 1

# --- 2) Identify drives that scored an OFFENSIVE TD by the same posteam ---
# Use touchdown == 1 if present; else fallback to td == 1

td_drives = pbp.loc[
    (pbp["posteam"].notna()) &
    (pbp["drive"].notna()) &
    (pbp["touchdown"] == 1),
    ["game_id", "drive", "posteam"]
].drop_duplicates()

td_drives["td_scored"] = 1

gl_results = gl.merge(td_drives, on=["game_id", "drive", "posteam"], how="left")
gl_results["td_scored"] = gl_results["td_scored"].fillna(0).astype(int)

team_gl_td = (
    gl_results.groupby("posteam", as_index=False)
    .agg(
        gl_drives=("gl_drive", "sum"),
        td_drives=("td_scored", "sum")
    )
)

team_gl_td["gl_td_pct"] = team_gl_td["td_drives"] / team_gl_td["gl_drives"]

# Optional: nicer formatting + sort
team_gl_td = team_gl_td.sort_values(["gl_td_pct", "gl_drives"], ascending=[False, False])
team_gl_td["gl_td_pct"] = (team_gl_td["gl_td_pct"] * 100).astype(int)

print(team_gl_td)

# League-wide goal-line TD%
print("League GL TD%:", round(gl_results["td_scored"].mean() * 100, 1))

# How many goal-line drives total?
print("Total goal-line drives:", int(gl_results["gl_drive"].sum()))

gl_score_rate_bar(df=team_gl_td)
