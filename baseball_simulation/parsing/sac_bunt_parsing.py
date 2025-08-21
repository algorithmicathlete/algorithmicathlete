import math

import pandas as pd

df = pd.read_pickle("statcast_data_2.pkl")
df = df[df["on_3b"].isna()]

print((df["events"] == "sac_bunt").sum())

sac_bunt_dict = {}


for outs in range(0, 2):
    df_o = df[df["outs_when_up"] == outs]

    df_first = df_o[df_o["on_1b"].notna() & df_o["on_2b"].isna()]
    sac_bunt_dict[(outs, "first")] = df_first["events"].value_counts(normalize=True)["sac_bunt"]

    df_second = df_o[df_o["on_2b"].notna() & df_o["on_1b"].isna()]
    sac_bunt_dict[(outs, "second")] = df_second["events"].value_counts(normalize=True).get("sac_bunt")

    df_both = df_o[df_o["on_1b"].notna() & df_o["on_2b"].notna()]
    sac_bunt_dict[(outs, "both")] = df_both["events"].value_counts(normalize=True)["sac_bunt"]

print(sac_bunt_dict)

# df = df[df["events"] == "sac_bunt"]

# df["hitter"] = df["at_bat_number"] % 9
#
# print(df["disparity"].value_counts().to_dict())
# print(df["outs_when_up"].value_counts().to_dict())
# print(df["strikes"].value_counts().to_dict())
# print(df["balls"].value_counts().to_dict())
#
# print((df["on_1b"].notna()).sum())
# print((df["on_2b"].notna()).sum())
# print((df["on_1b"].notna() & df["on_2b"].notna()).sum())
#
# print(df["attack_zone"].value_counts().to_dict())
