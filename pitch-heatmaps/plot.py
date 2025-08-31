import matplotlib
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from adjustText import adjust_text

df = pd.read_csv("name.csv")
name_to_id = dict(zip(df["MLBNAME"], df["MLBID"]))
matplotlib.rc('axes', edgecolor='white')

def draw_chase_contact_plot(metrics):
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")

    ax.scatter(metrics["chase%"], metrics["o_contact%"], s=18, alpha=0.8)

    ax.set_xlabel("Chase Rate (O-Swing%)", color="white", alpha=0.7)
    ax.set_ylabel("Outside Contact % (O-Contact%)", color="white", alpha=0.7)
    ax.grid(True, linestyle="--", alpha=0.25)

    x_med = metrics["chase%"].median()
    y_med = metrics["o_contact%"].median()
    ax.axvline(x_med, linestyle="--", linewidth=1, color="#1414aa")
    ax.axhline(y_med, linestyle="--", linewidth=1, color="#1414aa")

    a = metrics.nlargest(5, "chase%")
    b = metrics.nlargest(5, "o_contact%")
    c = metrics.nsmallest(5, "chase%")
    d = metrics.nsmallest(5, "o_contact%")

    chase_thresh = metrics["chase%"].quantile(0.9)
    contact_thresh = metrics["o_contact%"].quantile(0.9)

    both_high = metrics[
        (metrics["chase%"] >= chase_thresh) &
        (metrics["o_contact%"] >= contact_thresh)
    ]

    e = metrics[metrics["name"] == "Javier Baez"]

    texts = []

    for _, r in pd.concat([a, b, c, d, both_high, e]).drop_duplicates().reset_index(drop=True).iterrows():
        texts.append(ax.annotate(r["name"], (r["chase%"], r["o_contact%"]), color="white", fontsize=8, alpha=0.7))

    adjust_text(texts)

    ax.tick_params(colors="white")

    plt.tight_layout()
    plt.show()

def draw_strike_zone(df, name, SWUNG_DESC, CONTACT_DESC):
    df = df[df["batter"] == name_to_id[name]]

    df_neither = df[~df["description"].isin(SWUNG_DESC)]
    df_swing = df[df["description"].isin(SWUNG_DESC) & ~df["description"].isin(CONTACT_DESC)]
    df_contact = df[df["description"].isin(CONTACT_DESC)]

    top = df["sz_top"].median()
    bot = df["sz_bot"].median()

    fig, ax = plt.subplots(figsize=(6,7))
    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")

    half = 17/12/2

    ax.scatter(df_neither["plate_x"], df_neither["plate_z"], color="gray", s=6, alpha=0.2)
    ax.scatter(df_swing["plate_x"], df_swing["plate_z"], color="red", s=12, alpha=0.5)
    ax.scatter(df_contact["plate_x"], df_contact["plate_z"], color="green", s=12, alpha=0.5)

    ax.plot([-half, -half], [top, bot], color="white")
    ax.plot([-half, half], [top, top], color="white")
    ax.plot([-half, half], [bot, bot], color="white")
    ax.plot([half, half], [top, bot], color="white")

    # ax.tick_params(colors="white")

    ax.set_xlim(-2, 2)
    ax.set_ylim(0, 5)
    ax.set_aspect('equal', adjustable='box')
    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
    plt.tight_layout()
    plt.show()

def draw_ops_beeswarm(metrics):
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor("black")
    sns.swarmplot(data=metrics, x="ops_outside", size=4, alpha=0.8)
    ax.set_facecolor("black")

    print(metrics["ops_outside"].median())
    for _, x in metrics.nlargest(6, "ops_outside").iterrows():
        print(x["name"]
              )
    outliers = metrics.nlargest(1, "ops_outside")

    texts = []
    for _, r in pd.concat([outliers]).iterrows():
        texts.append(ax.annotate(r["name"], (r["ops_outside"], -0.04), color="white", alpha=0.7, fontsize=8))

    adjust_text(texts)
    ax.spines["bottom"].set_color("white")

    ax.tick_params(colors="white")
    ax.set_xlabel("OPS On Outside Pitches", color="white", alpha=0.7)

    plt.show()