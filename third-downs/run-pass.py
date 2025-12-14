import nfl_data_py as nfl
import numpy as np

pbp = nfl.import_pbp_data([2025])
third_downs = pbp[(pbp["down"] == 3)]

short = third_downs[third_downs["ydstogo"] <= 3]
medium = third_downs[
    (third_downs["ydstogo"] > 3) & (third_downs["ydstogo"] <= 6)
]

long = third_downs[
    (third_downs["ydstogo"] >= 7) & (third_downs["ydstogo"] < 15)
]
extra_long = third_downs[third_downs["ydstogo"] >= 15]

print(third_downs.shape[0], third_downs["pass"].sum(), third_downs["rush"].sum())

print(short["third_down_converted"].mean())
print(medium["third_down_converted"].mean())
print(long["third_down_converted"].mean())
print(extra_long["third_down_converted"].mean())


buckets = {
    "Short (≤3)": short,
    "Medium (4–6)": medium,
    "Long (7–15)": long,
    "Extra Long (15+)": extra_long
}

pass_counts = []
rush_counts = []

for df in buckets.values():
    pass_counts.append(df["pass"].sum())
    rush_counts.append(df["rush"].sum())

labels = list(buckets.keys())
x = np.arange(len(labels))

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 6), facecolor="black")
fig.patch.set_facecolor("black")
ax.set_facecolor("black")

ax.bar(x, rush_counts, label="Rush")
ax.bar(x, pass_counts, bottom=rush_counts, label="Pass")

ax.set_xlabel("3rd Down Lengths", color="white")
ax.set_ylabel("# Of Drives", color="white")
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend(facecolor="black", edgecolor="none", labelcolor="white")

ax.tick_params(colors="white")
for i, spine in enumerate(ax.spines.values()):
    if i in [0, 2]:
        spine.set_color("white")

plt.tight_layout()
# plt.show()
plt.savefig("buckets.png", dpi=300)
