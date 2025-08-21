import math
import random

import pandas as pd


df = pd.read_pickle("statcast_data_5.pkl")
df = df[df["bip"] == True]
df = df.dropna(subset=["launch_speed_angle"])

batted_ball_type = {}
hit_location_dict = {}
event_dict = {}

def change_misc_to_outs(hit_dict):
    x = 0
    new_dict = {}
    for k, v in hit_dict.items():
        if k not in {"home_run", "triple", "double", "single"}:
            x += v
        else:
            new_dict[k] = v

    new_dict["out"] = x
    return new_dict

for contact_quality in range(1, 7):
    df_cq = df.loc[df["launch_speed_angle"] == contact_quality]

    batted_ball_type[contact_quality] = df_cq["bb_type"].value_counts(normalize=True).to_dict()

    for bb_type in ["ground_ball", "popup", "line_drive", "fly_ball"]:
        df_bb = df_cq.loc[df_cq["bb_type"] == bb_type]

        df_r = df_bb.loc[df_bb["stand"] == "R"]
        hit_location_dict[(contact_quality, bb_type, "R")] = df_r["hit_location"].value_counts(normalize=True, dropna=False).to_dict()

        df_l = df_bb.loc[df_bb["stand"] == "L"]
        hit_location_dict[(contact_quality, bb_type, "L")] = df_l["hit_location"].value_counts(normalize=True, dropna=False).to_dict()

        for hit_location in range(1, 10):
            df_r_hl = df_r.loc[df_r["hit_location"] == hit_location]
            event_dict[(contact_quality, bb_type, "R", hit_location)] = change_misc_to_outs(df_r_hl["events"].value_counts(normalize=True).to_dict())

            df_l_hl = df_l.loc[df_l["hit_location"] == hit_location]
            event_dict[(contact_quality, bb_type, "L", hit_location)] = change_misc_to_outs(df_l_hl["events"].value_counts(normalize=True).to_dict())

print(batted_ball_type)
print(hit_location_dict)
print(event_dict)

