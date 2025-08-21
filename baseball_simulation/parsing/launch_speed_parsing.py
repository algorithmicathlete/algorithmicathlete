import pandas as pd


df = pd.read_pickle("statcast_data_5.pkl")

df = df[df["bip"] == True]

launch_speed_dict = {}


for pitch in ["fastball", "offspeed", "breaking"]:
    df_p = df.loc[df["pitch"] == pitch]

    df_z = df_p.loc[df_p["attack_zone"].isin(["shadow ball", "shadow strike"])]
    launch_speed_dict[(pitch, "shadow")] = df_z["launch_speed_angle"].value_counts(normalize=True).to_dict()

    for zone in ["heart", "chase", "waste"]:
        df_z = df_p.loc[df_p["attack_zone"] == zone]
        launch_speed_dict[(pitch, zone)] = df_z["launch_speed_angle"].value_counts(normalize=True).to_dict()

print(launch_speed_dict)
