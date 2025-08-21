import pandas as pd

def classify_contact(row):
    if row["description"] in ["hit_into_play", "foul", "foul_tip"]:
        return True
    else:
        return False

df = pd.read_pickle("statcast_data_3.pkl")
df = df[df["swing"] == True]
df["contact"] = df.apply(classify_contact, axis=1)

contact_dict = {}


for count in ["2 strike", "ahead", "even", "behind"]:
    df_c = df.loc[df["count"] == count]

    print(count, df_c["contact"].value_counts(normalize=True).to_dict()[True])

    for pitch in ["fastball", "offspeed", "breaking"]:
        df_p = df_c.loc[df_c["pitch"] == pitch]

        df_z = df_p.loc[df_p["attack_zone"].isin(["shadow ball", "shadow strike"])]
        contact_dict[(count, pitch, "shadow")] = df_z["contact"].value_counts(normalize=True).to_dict()[True]

        for zone in ["heart", "chase", "waste"]:
            df_z = df_p.loc[df_p["attack_zone"] == zone]
            contact_dict[(count, pitch, zone)] = df_z["contact"].value_counts(normalize=True).to_dict()[True]

print(contact_dict)
# df.to_pickle("statcast_data_4.pkl")