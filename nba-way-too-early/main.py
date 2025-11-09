from nba_api.stats.endpoints import leaguedashteamstats
import pandas as pd

nba_team_map = {
    "Atlanta Hawks": "ATL",
    "Boston Celtics": "BOS",
    "Brooklyn Nets": "BKN",
    "Charlotte Hornets": "CHA",
    "Chicago Bulls": "CHI",
    "Cleveland Cavaliers": "CLE",
    "Dallas Mavericks": "DAL",
    "Denver Nuggets": "DEN",
    "Detroit Pistons": "DET",
    "Golden State Warriors": "GSW",
    "Houston Rockets": "HOU",
    "Indiana Pacers": "IND",
    "LA Clippers": "LAC",
    "Los Angeles Lakers": "LAL",
    "Memphis Grizzlies": "MEM",
    "Miami Heat": "MIA",
    "Milwaukee Bucks": "MIL",
    "Minnesota Timberwolves": "MIN",
    "New Orleans Pelicans": "NOP",
    "New York Knicks": "NYK",
    "Oklahoma City Thunder": "OKC",
    "Orlando Magic": "ORL",
    "Philadelphia 76ers": "PHI",
    "Phoenix Suns": "PHX",
    "Portland Trail Blazers": "POR",
    "Sacramento Kings": "SAC",
    "San Antonio Spurs": "SAS",
    "Toronto Raptors": "TOR",
    "Utah Jazz": "UTA",
    "Washington Wizards": "WAS"
}

teams_off = leaguedashteamstats.LeagueDashTeamStats(
    season="2025-26",
    season_type_all_star="Regular Season",
    per_mode_detailed="PerGame"
).get_data_frames()[0]

teams_def = leaguedashteamstats.LeagueDashTeamStats(
    season="2025-26",
    season_type_all_star="Regular Season",
    per_mode_detailed="PerGame",
    measure_type_detailed_defense="Opponent"
).get_data_frames()[0]

df = teams_off.merge(
    teams_def[["TEAM_ID", "OPP_FTA"]],
    on="TEAM_ID"
)

# === 4️⃣ Compute free throw differential ===
df["FT_DIFF"] = df["FTA"] - df["OPP_FTA"]

# === 5️⃣ Sort for clarity ===
df = df.sort_values("FT_DIFF", ascending=False)[["TEAM_NAME", "FTA", "OPP_FTA", "FT_DIFF"]]
df = df[df["TEAM_NAME"].isin(list(nba_team_map))]
print(df)

import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))
plt.barh(df["TEAM_NAME"], df["FT_DIFF"], color=['#1D428A' if x>0 else '#C8102E' for x in df["FT_DIFF"]])
plt.axvline(0, color='black', lw=1)
plt.title("Free Throw Attempt Differential (2024-25 Season)")
plt.xlabel("Team FTA - Opponent FTA per Game")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()