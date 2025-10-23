import nfl_data_py as nfl

pbp = nfl.import_pbp_data([2024])
pbp = pbp[pbp["time"].notna()]

print(list(pbp.columns))
print(pbp["interception"].unique())
print(pbp["fumble_lost"].unique())

for game_id, game in pbp.groupby("game_id"):
    game = game.sort_values("order_sequence")
    teams = {
        x: {"name": game[f"{x}_team"].iloc[0], "score": game[f"total_{x}_score"].iloc[-1]}
        for x in ["home", "away"]
    }

    if teams["home"]["score"] == teams["away"]["score"]:
        print(teams)
        continue # ties are boring

    winner, loser = ("home", "away") if teams["home"]["score"] > teams["away"]["score"] else ("away", "home")

    max_loser = game[f"{loser}_wp"]

    if max_loser.max() < 0.5:
        continue # never choked, never were in winnin position

    q = game.loc[max_loser.idxmax()]
    choke_df = game.loc[max_loser.idxmax() + 1:].reset_index(drop=True)
    choke_team_df = choke_df[choke_df["posteam_type"] == loser]
    ints = choke_team_df["interception"].eq(1).sum()
    fumbles = choke_team_df["fumble_lost"].eq(1).sum()

    print(teams["home"]["name"], teams["home"]["score"], teams["away"]["score"], teams["away"]["name"], max_loser.max(), ints, fumbles)