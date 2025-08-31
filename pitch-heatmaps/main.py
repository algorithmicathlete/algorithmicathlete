import pandas as pd
from outside_zone import outside_zone_df
from plot import draw_strike_zone, draw_chase_contact_plot, draw_ops_beeswarm


SWUNG_DESC = ["foul", "hit_into_play", "swinging_strike", "swinging_strike_blocked", "foul_tip"]
CONTACT_DESC = ["foul", "hit_into_play"]

if __name__ == '__main__':
    df = pd.read_csv("statcast_data.csv")
    df_out = df[~df["zone"].between(1, 9, inclusive="both")].copy()
    metrics = outside_zone_df(df_out, SWUNG_DESC, CONTACT_DESC)

    player = "Luis Arraez"
    draw_strike_zone(df_out, player, SWUNG_DESC, CONTACT_DESC)

    # draw_chase_contact_plot(metrics)
    # draw_ops_beeswarm(metrics)
