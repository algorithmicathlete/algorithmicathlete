import nfl_data_py as nfl
import numpy as np
from matplotlib import pyplot as plt

pbp = nfl.import_pbp_data([2025])
print(list(pbp.columns))


fg_attempts = pbp[pbp["field_goal_attempt"] == 1].copy()
fg_attempts["fg_made"] = (fg_attempts["field_goal_result"] == "made").astype(int)

from sklearn.linear_model import LogisticRegression

X = fg_attempts[["kick_distance"]]
y = fg_attempts["fg_made"]

model = LogisticRegression()
model.fit(X, y)

import pandas as pd
distances = pd.DataFrame({
    "kick_distance": [30, 40, 50, 55, 60]
})

print(model.predict_proba(distances))

fg_attempts["fg_expected"] = model.predict_proba(X)[:, 1]
fg_attempts["fg_oe"] = fg_attempts["fg_made"] - fg_attempts["fg_expected"]

kicking = (
    fg_attempts
    .groupby("kicker_player_name")
    .agg(
        team=("posteam", "last"),
        avg_fg_distance=("kick_distance", "mean"),
        fg_pct=("fg_made", "mean"),
        fg_oe_total=("fg_oe", "sum"),
        made=("fg_made", "sum"),
        att=("field_goal_attempt", "count"),
    )
    .assign(fg_pct_oe=lambda x: (x.fg_oe_total / x.att)*100)
    .query("att >= 10")
    .reset_index()
)
kicking = kicking.sort_values("fg_pct_oe", ascending=False)

print(kicking)
kicking.to_csv("kicking.csv")
