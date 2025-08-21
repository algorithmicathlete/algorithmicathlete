import pandas as pd

df = pd.read_pickle("statcast_data.pkl")

df = df.sort_values("pitch_number").drop_duplicates(subset=["game_pk", "at_bat_number"], keep="last")
print((df["on_1b"].notna() & df["on_2b"].isna()).sum())
# print(df["description"].unique())
# print(df["events"].unique())