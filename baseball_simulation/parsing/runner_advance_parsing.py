import math

import pandas as pd

df = pd.read_pickle("statcast_data.pkl")

def runner_on_first_double(df):
    df_double = df.loc[(df["events"] == "double") & (df["on_1b"].notna())].copy()

    def classify_runner_on_first_scored(row):
        runners = pd.notna(row["on_2b"]) + pd.notna(row["on_3b"])
        return (row["bat_score"] + runners + 1) == row["post_bat_score"]

    df_double['runner_scored'] = df_double.apply(classify_runner_on_first_scored, axis=1)

    print(df_double.shape[0])
    print((df_double["runner_scored"] == True).sum())

    for outs in range(0, 3):
        df_o = df_double[df_double["outs_when_up"] == outs]
        print(f"{outs} outs: {(df_o['runner_scored'] == True).sum() / df_o.shape[0]} ({(df_o['runner_scored'] == True).sum()}/{df_o.shape[0]} {df_o['runner_scored'].value_counts(normalize=True).to_dict()}")

#stupid to optimizd for weak, but if you want ig
# # weak is about 0.12 regardless of outs, otherwise no discernable pattern & just ude outs

def runner_on_first_single():
    total = 8241
    reaches = 2615
    print(reaches/total)

def runner_on_second_single(df):
    df_single = df[(df["events"] == "single") & (df["on_2b"].notna())]

    def scored(df):
        sole_runner_scored = (df["post_bat_score"] == df["bat_score"]+1) & df["on_3b"].isna()
        runner_on_third_both_scored = (df["post_bat_score"] == df["bat_score"]+2) & df["on_3b"].notna()
        return sole_runner_scored.sum()+runner_on_third_both_scored.sum()

    print(df_single.shape[0])
    print(scored(df_single))

    for outs in range(0, 3):
        df_o = df_single[df_single["outs_when_up"] == outs]
        print(f"{outs} outs: {scored(df_o)/df_o.shape[0]} ({scored(df_o)}/{df_o.shape[0]})")


runner_on_first_double(df)
print()
runner_on_second_single(df)
print()
runner_on_first_single()