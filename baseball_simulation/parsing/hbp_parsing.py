import pandas as pd

df = pd.read_pickle("statcast_data_2.pkl")
# df = df[df["events"] == "hit_by_pitch"]
# print(df["attack_zone"].value_counts().to_dict())

hbp_dict = {}
for zone in ["waste", "chase"]:
    df_z = df[df["attack_zone"] == zone]
    hbp_dict[zone] = df_z["events"].value_counts(normalize=True, dropna=False).to_dict()["hit_by_pitch"]

print(hbp_dict)