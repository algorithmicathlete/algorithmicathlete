import pandas as pd


df = pd.read_pickle("statcast_data_4.pkl")

df = df[df["contact"] == True]
df["bip"] = df["description"] == "hit_into_play"

bip_dict = {}


for pitch in ["fastball", "offspeed", "breaking"]:
    df_p = df.loc[df["pitch"] == pitch]

    df_z = df_p.loc[df_p["attack_zone"].isin(["shadow ball", "shadow strike"])]
    bip_dict[(pitch, "shadow")] = df_z["bip"].value_counts(normalize=True).to_dict()[True]

    for zone in ["heart", "chase", "waste"]:
        df_z = df_p.loc[df_p["attack_zone"] == zone]
        bip_dict[(pitch, zone)] = df_z["bip"].value_counts(normalize=True).to_dict()[True]

print(bip_dict)

df.to_pickle("statcast_data_5.pkl")