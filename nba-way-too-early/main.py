from nba_api.stats.endpoints import leaguedashteamstats
from utils import *
from plot import ft_differential, ft_win_pct

season = "2025-26"
# 24-25
# 25-26
# 23-24
# 22-23

teams_off = leaguedashteamstats.LeagueDashTeamStats(
    season=season,
    season_type_all_star="Regular Season",
    per_mode_detailed="PerGame"
).get_data_frames()[0]

teams_def = leaguedashteamstats.LeagueDashTeamStats(
    season=season,
    season_type_all_star="Regular Season",
    per_mode_detailed="PerGame",
    measure_type_detailed_defense="Opponent"
).get_data_frames()[0]

df = teams_off.merge(
    teams_def[["TEAM_ID", "OPP_FTA"]],
    on="TEAM_ID"
)

df["FT_DIFF"] = df["FTA"] - df["OPP_FTA"]
df = df[df["TEAM_NAME"].isin(list(nba_team_map))]


df["opp_fta_rank"] = df["OPP_FTA"].rank(ascending=True, method="dense").astype(int)
df["ft_rank"] = df["FTA"].rank(ascending=False, method="dense").astype(int)

df = df.sort_values("FT_DIFF", ascending=False)[["TEAM_NAME", "FTA", "OPP_FTA", "FT_DIFF"]]

print(df)

if __name__ == '__main__':
    ft_differential(df)
#     ft_win_pct(df)