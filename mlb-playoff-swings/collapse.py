import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg

fig, ax = plt.subplots(figsize=(10, 5))

def get_history(url, window, label, game_number, color):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")

    results = soup.find("div", {"id": "timeline_results"})

    wins = 0
    losses = 0
    history = []

    print(url)
    for result in results.find_all("li", {"class": "result"}):
        win = "beat" in result.text.strip()
        wins += win
        losses += 1 - win
        history.append(wins / (wins + losses))

    history = history[game_number:]
    dates = list(range(game_number, len(history)+game_number))

    df = pd.DataFrame({"Game": dates, "WinPct": history})
    df["RollingAvg"] = df["WinPct"].rolling(window=window, min_periods=1).mean()

    # ax.plot(df["Game"], df["WinPct"], alpha=0.4, label=f"{label or 'Raw'} Win%")

    path = f"logos/{label.lower()}.png"
    logo = mpimg.imread(path)
    imagebox = OffsetImage(logo, zoom=0.3)
    ab = AnnotationBbox(imagebox, (151, history[-11] + (0.005 if label == "DET" else -0.005)), frameon=False)
    plt.gca().add_artist(ab)

    ax.plot(df["Game"], df["RollingAvg"], linewidth=2, label=label, color=color)

# Example: Mets
teams = [
    # ('NYM', 67, "#FF5910"),
    # ('MIL', 67, "#FFC52F"),
    ("DET", 90, "#0C2340"),
    ("CLE", 90, "#E50022")
]


for team in teams:
    get_history(f"https://www.baseball-reference.com/teams/{team[0]}/2025.shtml", window=6, label=team[0], game_number=team[1], color=team[2])


# Example: add another team
# get_history("https://www.baseball-reference.com/teams/CHW/2024.shtml", window=10, label="White Sox")

ax.set_facecolor("#111111")
fig.patch.set_facecolor("#000000")
for spine in ax.spines.values():
    spine.set_color("#888888")


ax.yaxis.label.set_color("#CCCCCC")
ax.xaxis.label.set_color("#CCCCCC")

plt.tick_params(axis='x', colors='white')
plt.tick_params(axis='y', colors='white')

ax.set_xlim(left=90)
ax.set_title("Team Win% with Rolling Average")
ax.set_xlabel("Game Number")
ax.set_ylabel("Win Percentage")

# plt.show()
plt.savefig("alcentral.png", dpi=300)