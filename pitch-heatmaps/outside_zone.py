import pandas as pd


df = pd.read_csv("name.csv")
id_to_name = dict(zip(df["MLBID"], df["MLBNAME"]))

def outside_zone_df(df_out, SWUNG_DESC, CONTACT_DESC):
    rows = []
    print(df_out["events"].unique())
    for batter_id, batter_df in df_out.groupby("batter"):
        outside_pitches = batter_df.shape[0]

        df_swing = batter_df[batter_df["description"].isin(SWUNG_DESC)]
        outside_swings = df_swing.shape[0]

        if outside_pitches < 200:
            continue

        df_contact = df_swing[df_swing["description"].isin(CONTACT_DESC)]

        chase = df_swing.shape[0] / batter_df.shape[0]
        o_contact = df_contact.shape[0] / df_swing.shape[0]

        try:
            name = id_to_name[batter_id]
        except Exception as e:
            print(batter_id)
            name = None

        end = batter_df[batter_df["events"].notna()]
        H = end["events"].isin(["single", "double", "triple", "home_run"]).sum()
        BB = end["events"].eq("walk").sum()
        HBP = end["events"].eq("hit_by_pitch").sum()
        SF = end["events"].eq("sac_fly").sum()
        AB = (~end["events"].isin(["walk", "hit_by_pitch", "sac_fly", "sac_bunt", "catcher_interf"])).sum()

        TB = (
            end["events"].eq("single").sum()
            + 2 * end["events"].eq("double").sum()
            + 3 * end["events"].eq("triple").sum()
            + 4 * end["events"].eq("home_run").sum()
        )

        OBP = (H + BB + HBP) / (AB + BB + HBP + SF)
        SLG = TB / AB if AB > 0 else 0

        rows.append({
            "batter": batter_id,
            "name": name,
            "outside_pitches": outside_pitches,
            "outside_swings": outside_swings,
            "chase%": chase,
            "o_contact%": o_contact,
            "ops_outside": OBP + SLG if AB > 50 else None
        })

    return pd.DataFrame(rows).sort_values("outside_pitches", ascending=False).reset_index(drop=True)