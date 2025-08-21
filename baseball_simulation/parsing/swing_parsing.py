import pandas as pd


def classify_count(row):
    if row["strikes"] == 2:
        return "2 strike"
    elif row["balls"] > row["strikes"]:
        return "ahead"
    elif row["balls"] == row["strikes"]:
        return "even"
    else:
        return "behind" # just 0-1 count lol

def classify_swing(row):
    swing_descs = ['hit_into_play', 'swinging_strike', 'foul', 'swinging_strike_blocked', 'foul_tip']
    if row["description"] in swing_descs:
        return True
    else:
        return False

df = pd.read_pickle("statcast_data_2.pkl")
df = df[~df["description"].isin(["foul_bunt", "missed_bunt", "bunt_foul_tip"])]

df['count'] = df.apply(classify_count, axis=1)
df['swing'] = df.apply(classify_swing, axis=1)

swing_dict = {}

for count in ["2 strike", "ahead", "even", "behind"]:
    df_c = df.loc[df["count"] == count]
    for pitch in ["fastball", "offspeed", "breaking"]:
        df_p = df_c.loc[df_c["pitch"] == pitch]

        df_z = df_p.loc[df_p["attack_zone"].isin(["shadow ball", "shadow strike"])]
        swing_dict[(count, pitch, "shadow")] = df_z["swing"].value_counts(normalize=True).to_dict()[True]

        for zone in ["heart", "chase", "waste"]:
            df_z = df_p.loc[df_p["attack_zone"] == zone]
            swing_dict[(count, pitch, zone)] = df_z["swing"].value_counts(normalize=True).to_dict()[True]

print(swing_dict)
# df.to_pickle("statcast_data_3.pkl")

