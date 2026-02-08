from nba_api.stats.endpoints import leaguedashteamstats

from colors import nba_team_map

season = "2025-26"

# Defensive opponent stats
df = leaguedashteamstats.LeagueDashTeamStats(
    season=season,
    season_type_all_star="Regular Season",
    per_mode_detailed="PerGame",
    measure_type_detailed_defense="Opponent"   # ← Works for YOUR version
).get_data_frames()[0]


print(list(df.columns))

# Keep real NBA teams
df = df[df["TEAM_NAME"].isin(list(nba_team_map))]

# Rankings
df["opp_fta_rank"] = df["OPP_FT_PCT"].rank(ascending=True, method="dense").astype(int)

# Final table
df = df.sort_values("OPP_FT_PCT", ascending=True)[["TEAM_NAME", "OPP_FTM", "OPP_FTA", "OPP_FT_PCT"]]

print(df)