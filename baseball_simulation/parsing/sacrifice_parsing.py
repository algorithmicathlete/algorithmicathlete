import pandas as pd

df = pd.read_pickle("statcast_data.pkl")
print(df["events"].unique())

df = df[df["on_3b"].notna() & df["hit_location"].between(7, 9) & (df["outs_when_up"] <= 1) & (df["events"].isin(["field_out", "sac_fly_double_play", "sac_fly"]))]
# the events is to narrow it down where the ball was CAUGHT

print((df["events"]=="sac_fly").sum(), "i got hard")
print((df["events"]=="sac_fly").sum() / df.shape[0])
print(df.shape[0])


# df2 = df[df["events"] == "sac_fly"]
print(df["bb_type"].value_counts(dropna=False).to_dict())
sac_fly_dict = {}

for bb_type in ["fly_ball", "line_drive"]:
    df_bb = df[df["bb_type"] == bb_type]

    for contact_quality in range(3, 7):
        df_cq = df_bb[df_bb["launch_speed_angle"] == contact_quality]
        events_dict = df_cq["events"].value_counts(normalize=True).to_dict()

        if "sac_fly" in events_dict:
            sac_fly_dict[(bb_type, contact_quality)] = df_cq["events"].value_counts(normalize=True).to_dict()["sac_fly"]

print(sac_fly_dict)
