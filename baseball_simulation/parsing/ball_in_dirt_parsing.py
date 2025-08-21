import pandas as pd

df = pd.read_pickle("statcast_data_2.pkl")
wp = 1440
df = df[(df["on_1b"].notna() | df["on_2b"].notna()) & (df["attack_zone"] == "waste")]

print(wp/df.shape[0])


df = pd.read_pickle("statcast_data_2.pkl")
pb = 239
df = df[(df["on_1b"].notna() | df["on_2b"].notna()) & (df["attack_zone"] == "chase")]

print(pb/df.shape[0])