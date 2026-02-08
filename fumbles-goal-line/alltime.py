import nfl_data_py as nfl


pbp = nfl.import_pbp_data(list(range(2000, 2026)))
gl = pbp[pbp["yardline_100"] <= 5].copy() # goal line
gl["turnover"] = (gl["fumble_lost"] == 1) | (gl["interception"] == 1)

df_year = (
    gl.groupby(["season"])
      .agg(total_to=("turnover", "sum"))
      .reset_index()
)

print(df_year)
