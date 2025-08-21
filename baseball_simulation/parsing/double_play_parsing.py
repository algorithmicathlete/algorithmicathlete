import pandas as pd

df = pd.read_pickle("statcast_data.pkl")
df = df[
    df["on_3b"].notna() & (df["bb_type"] == "ground_ball") & (df["hit_location"].between(1, 6))
    & (~df["events"].isin(["single", "double", "triple", "sac_bunt", "field_error"])) & df["on_1b"].isna()
    & (df["outs_when_up"] <= 1)
]

df["scored"] = df["bat_score"] < df["post_bat_score"]
print(df["scored"].value_counts())

for cq in range(1, 7):
    df_cq = df[df["launch_speed_angle"] == cq]
    print(cq, df_cq["scored"].value_counts().to_dict())

# print(df["description"].value_counts())
# print(df["events"].value_counts().to_dict())
#
# score_from_third_dict = {"free": {}, "loaded": {}}
#
# for outs in range(0, 2):
#     df_o = df[df["outs_when_up"] == outs]
#     for event in ["field_out", "force_out", "grounded_into_double_play", "fielders_choice"]:
#         df_e = df[(df["events"] == event)]
#         df_e_loaded = df_e[df_e["on_2b"].notna()]
#
#         score_from_third_dict["corners"][event] = df_e["scored"].value_counts(normalize=True).to_dict()[True]
#         score_from_third_dict["loaded"][event] = df_e_loaded["scored"].value_counts(normalize=True).to_dict()[True]
#
#     print(score_from_third_dict)

# 'fielders_choice': 367, 'double_play': 334, 'truncated_pa': 314, 'fielders_choice_out': 305,

df = pd.read_pickle("statcast_data_2.pkl")
df = df[
    df["on_1b"].notna() & (df["bb_type"] == "ground_ball") &
    (df["hit_location"].between(1, 6)) &
    (~df["events"].isin(["single", "double", "triple", "sac_bunt", "field_error"]))
]

ground_ball_out_dict = {}

for outs in range(0, 3):
    df_o = df[df["outs_when_up"] == outs]
    for contact_quality in {1, 2, 4}:
        df_cq = df_o[df_o["launch_speed_angle"] == contact_quality]
        events_dict = df_cq["events"].value_counts(normalize=True).to_dict()

        if "fielders_choice_out" in events_dict:
            events_dict["force_out"] += events_dict.pop("fielders_choice_out")

        if "double_play" in events_dict:
            events_dict["grounded_into_double_play"] += events_dict.pop("double_play")

        ground_ball_out_dict[(outs, contact_quality)] = events_dict

print(ground_ball_out_dict)