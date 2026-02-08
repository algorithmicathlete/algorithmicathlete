import nfl_data_py as nfl
from plot import epa_scatter, beeswarm


pbp = nfl.import_pbp_data([2025])
gl = pbp[pbp["yardline_100"] <= 5].copy()
gl["turnover"] = (gl["fumble_lost"] == 1) | (gl["interception"] == 1)
fumbles = gl[(gl["fumble_lost"] == 1)]
picks = gl[(gl["interception"] == 1)]

print(gl[gl["turnover"] == 1]["epa"].mean())

agg_base = dict(
    turnover_pct=("turnover", "mean"),
    total_int=("interception", "sum"),
    total_fmb=("fumble_lost", "sum"),
    total_to=("turnover", "sum"),
    td_rate=("touchdown", "mean"),
    gl_epa=("epa", "mean")
)

df_off = gl.groupby("posteam").agg(**agg_base).reset_index()

df_def = (
    gl.groupby("defteam")
      .agg(**{f"def_{k}": v for k, v in agg_base.items()})
      .reset_index()
      .rename(columns={"defteam": "team"})
)

df_off = df_off.rename(columns={"posteam": "team"})

df = df_off.merge(df_def, on="team", how="outer")
df = df.sort_values("total_to")


df_def = (
    gl.groupby("defteam")
      .agg(**{f"def_{k}": v for k, v in agg_base.items()})
      .reset_index()
      .rename(columns={"defteam": "team"})
)

print(df[["team", "turnover_pct", "def_turnover_pct", "total_to", "def_total_to"]])
print("\n"*5)

print([ x for x in list(pbp.columns)])

beeswarm(df, "def_total_to")
beeswarm(df, 'total_to')
epa_scatter(df)