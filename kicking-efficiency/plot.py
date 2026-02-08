import matplotlib.pyplot as plt
import pandas as pd

years = list(range(1999, 2026))


years = list(range(1999, 2026))
fg_pct = [
    0.0909, 0.1429, 0.25, 0.1667, 0.3077, 0.2308, 0.3571,
    0.375, 0.25, 0.5333, 0.24, 0.5, 0.4643, 0.4474,
    0.4615, 0.4688, 0.5385, 0.3947, 0.6047, 0.5745,
    0.4324, 0.4906, 0.5283, 0.6125, 0.5897, 0.5851, 0.6186
]

attempts = [11.0, 7.0, 12.0, 12.0, 13.0, 13.0, 14.0, 8.0, 16.0, 15.0, 25.0, 22.0, 28.0, 38.0, 26.0, 32.0, 26.0, 38.0, 43.0, 47.0, 37.0, 53.0, 53.0, 80.0, 78.0, 94.0, 97.0]


fg_pct = pd.Series(fg_pct, index=years)
attempts = pd.Series(attempts, index=years)

fg_pct_rolling = fg_pct.rolling(window=5, min_periods=3).mean()


fig, ax = plt.subplots(figsize=(10,5))
ax.set_facecolor("#111111")
fig.patch.set_facecolor("#000000")


ax.yaxis.label.set_color("#CCCCCC")
ax.xaxis.label.set_color("#CCCCCC")

plt.tick_params(axis='x', colors='white')
plt.tick_params(axis='y', colors='white')

# FG%
ax.plot(years, fg_pct_rolling, color="blue", marker=".")
ax.set_ylabel("FG% (55+ yards)", fontsize=12)
ax.set_ylim(0, 0.7)


ax2 = ax.twinx()
ax2.plot(years[2:], attempts[2:], color='orange', marker='.')
ax2.set_ylabel("Attempts (55+ yards)", fontsize=12)

for spine in ax2.spines.values():
    spine.set_color("#888888")

ax2.yaxis.label.set_color("#CCCCCC")
ax2.xaxis.label.set_color("#CCCCCC")

plt.tick_params(axis='x', colors='white')
plt.tick_params(axis='y', colors='white')

line1, = ax.plot(
    years,
    fg_pct_rolling,
    marker=".",
    label="FG% (55+ yards)"
)

# Attempts
line2, = ax2.plot(
    years[2:],
    attempts[2:],
    color="orange",
    marker=".",
    label="Attempts (55+ yards)"
)

# Legend (combine both axes)
ax.legend(
    handles=[line1, line2],
    loc="upper left",
    frameon=False,
    labelcolor="white"
)

ax.set_xlabel("Season", fontsize=12)
# plt.title("55+ Yard Field Goals: Volume vs Accuracy")
plt.tight_layout()
plt.savefig("extra-long2.png", dpi=350)