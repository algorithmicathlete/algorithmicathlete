import nfl_data_py as nfl
import numpy as np

pbp = nfl.import_pbp_data([2024])

print([ x for x in list(pbp.columns) if "drive" in x])
print(pbp["fixed_drive_result"].unique())
results = {x: {"times": [], "first_downs": []} for x in range(10)}

for game_id, game in pbp.groupby("game_id"):
    game = game.sort_values("order_sequence")

    for drive_id, drive in game.groupby("drive"):
        drive = drive.sort_values("order_sequence")

        team = drive.iloc[0]["posteam"]
        start = drive["drive_start_yard_line"].unique()[0]
        if not start:
            continue

        if start == "50":
            yard = 50
        else:
            side, yard = start.split()

            yard = int(yard)
            if team != side:
                yard = 100 - yard

        result = drive["fixed_drive_result"].unique()[0]

        if result in ["End of half"]:
            continue

        elif result in ["Field goal", "Missed field goal"]:
            result = "Field goal attempt"

        elif result in ["Turnover", "Opp touchdown"]:
            result = "Turnover"

        x = yard // 10

        minutes, seconds = drive["drive_time_of_possession"].unique()[0].split(":")
        results[x]["times"].append(int(minutes)*60+int(seconds))
        results[x]["first_downs"].append(drive["drive_first_downs"].unique()[0])

        if result in results[x]:
            results[x][result] += 1
        else:
            results[x][result] = 1

outcomes = ['Touchdown', 'Field goal attempt', 'Punt', 'Turnover', 'Turnover on downs', 'Safety']

def stats(arr):
    mean = np.mean(arr)
    median = np.median(arr)

    return mean, median

# fg attempt, safety, TO, to on downs, punt, TD
all = []
for k, v in results.items():
    for outcome in outcomes:
        if outcome not in v:
            v[outcome] = 0

    play_count = sum([x[1] for x in v.items() if x[0] not in ["times", "first_downs"]])

    time_array = np.array(v["times"])
    mean_val, median_val = stats(time_array)

    fd_array = np.array(v["first_downs"])
    mean_val2, median_val2 = stats(fd_array)



    for res, value in v.items():
        if type(value) != list:
            v[res] = value/play_count

    print(k)
    mins, secs = divmod(mean_val, 60)
    print(mean_val, f"{int(mins)}:{int(secs)}", mean_val2)
    all.append(v)

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6), facecolor="black")
fig.patch.set_facecolor("black")
ax.set_facecolor("black")

seeds = [f"{x*10}-{x*10+9}" for x in range(5)] + [f"{x*10+10}-{x*10+1}" for x in range(4, -1, -1)]
print(seeds)
plasma_colors = [
    "#0d0887",  # deep violet
    "#46039f",  # purple
    "#7201a8",  # violet
    "#9c179e",  # magenta
    "#bd3786",  # pinkish
    "#d8576b",  # reddish-pink
    "#ed7953",  # orange
    "#fb9f3a",  # golden orange
    "#fdca26",  # bright yellow
    "#f0f921",  # neon yellow
]
bottom = np.array([0 for x in range(10)])
for i, outcome in enumerate(outcomes):
    curr = np.array([x[outcome] for x in all])

    ax.bar(seeds, curr, bottom=bottom, label=outcome, color=plasma_colors[i])
    bottom = bottom + curr

ax.set_xlabel("Starting Field Position", color="white")
ax.set_ylabel("% Of Drives", color="white")
ax.set_xticks(seeds)
ax.legend(facecolor="black", edgecolor="none", labelcolor="white")

ax.tick_params(colors="white")
for i, spine in enumerate(ax.spines.values()):
    if i in [0, 2]:
        spine.set_color("white")

# fig.tight_layout()
# plt.show()
plt.savefig("fieldposition.png", dpi=300)
