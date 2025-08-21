import pandas as pd

def classify_attack_zone(row):
    sz_top = row['sz_top']
    sz_bot = row['sz_bot']
    plate_x = row['plate_x']
    plate_z = row['plate_z']

    zone_height = sz_top - sz_bot
    third = zone_height * 1/3

    STRIKE_ZONE_WIDTH = 0.83

    if (abs(plate_x) <= (STRIKE_ZONE_WIDTH * 2/3)) and ((sz_bot + third/2) <= plate_z <= (sz_top - third/2)):
        zone = "heart"
    elif (abs(plate_x) <= STRIKE_ZONE_WIDTH) and (sz_bot <= plate_z <= sz_top):
        zone = "shadow strike"
    elif (abs(plate_x) <= (STRIKE_ZONE_WIDTH * 4/3)) and ((sz_bot - third/2) <= plate_z <= (sz_top + third/2)):
        zone = "shadow ball"
    elif (abs(plate_x) <= (STRIKE_ZONE_WIDTH * 2)) and ((sz_bot - zone_height/2) <= plate_z <= (sz_top + zone_height/2)):
        zone = "chase"
    else:
        zone = "waste"

    return zone

def classify_pitch(row):
    fastball = {"FF", "SI", "FC"}
    offspeed = {"CH", "FS", "FO", "SC"}
    breaking = {"CU", "KC", "CS", "SL", "ST", "SV"}

    if row["pitch_type"] in fastball:
        return "fastball"
    elif row["pitch_type"] in offspeed:
        return "offspeed"
    elif row["pitch_type"] in breaking:
        return "breaking"
    else:
        return "N/A"


df = pd.read_pickle("statcast_data_2.pkl")
print("its ovea")

# df = df[(~df["pitch_type"].isin(["FA", "EP", "KN", "PO"]) ) & df["pitch_type"].notna()]
# df["pitch"] = df.apply(classify_pitch, axis=1)
# df['attack_zone'] = df.apply(classify_attack_zone, axis=1)

pitch_type_dict = {}
pitch_zone_dict = {}

for balls in range(0, 4):
    df_b = df.loc[df["balls"] == balls]
    for strikes in range(0, 3):
        df_s = df_b.loc[df_b["strikes"] == strikes]
        for outs in range(0, 3):
            df_o = df_s.loc[df_s["outs_when_up"] == outs]

            df_runners = df_o.loc[(df_o["on_1b"].notna()) | (df_o["on_2b"].notna()) | (df_o["on_3b"].notna())]
            df_no_runners = df_o.loc[(df_o["on_1b"].isna()) & (df_o["on_2b"].isna()) & (df_o["on_3b"].isna())]

            pitch_type_dict[(balls, strikes, outs, True)] = df_runners["pitch"].value_counts(normalize=True).to_dict()
            pitch_type_dict[(balls, strikes, outs, False)] = df_no_runners["pitch"].value_counts(normalize=True).to_dict()

            for pitch_type in ["fastball", "offspeed", "breaking"]:
                df_p_runners = df_runners.loc[df_runners["pitch"] == pitch_type]
                df_p_no_runners = df_no_runners.loc[df_no_runners["pitch"] == pitch_type]

                pitch_zone_dict[(balls, strikes, outs, True, pitch_type)] = df_p_runners["attack_zone"].value_counts(normalize=True).to_dict()
                pitch_zone_dict[(balls, strikes, outs, False, pitch_type)] = df_p_no_runners["attack_zone"].value_counts(normalize=True).to_dict()

# df.to_pickle("statcast_data_2.pkl")
print(pitch_type_dict)
print()
print()
print(pitch_zone_dict)