import pandas as pd
from nba_api.stats.endpoints import commonallplayers, shotchartdetail
import pandas as pd, time

df = pd.read_csv("big-men-2015.csv")
df = df[df["FGA"] > 10]

players = commonallplayers.CommonAllPlayers(
    is_only_current_season=0,
    season="2014-15"
).get_data_frames()[0]

seven_footers = players[players["DISPLAY_FIRST_LAST"].isin(df["Player"].values.flatten())][["PERSON_ID", "DISPLAY_FIRST_LAST"]]

all_shots = []
for _, row in seven_footers.iterrows():
    try:
        print("Fetching:", row.DISPLAY_FIRST_LAST)
        shots = shotchartdetail.ShotChartDetail(
            team_id=0,
            player_id=row.PERSON_ID,
            season_nullable="2014-15",
            season_type_all_star="Regular Season"
        ).get_data_frames()[0]
        shots["PLAYER_NAME"] = row.DISPLAY_FIRST_LAST
        all_shots.append(shots)
        time.sleep(0.6)
    except Exception as e:
        print("Error:", e)
        continue

shots_df = pd.concat(all_shots, ignore_index=True)
print(shots_df.head())
shots_df.to_csv("7foot_2015.csv")