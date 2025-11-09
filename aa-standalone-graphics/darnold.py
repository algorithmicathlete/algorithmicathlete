import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from matplotlib import image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

r = requests.get("https://www.pro-football-reference.com/players/D/DarnSa00/gamelog/")

soup = BeautifulSoup(r.content, "lxml")


table = soup.find("tbody")


total_wins = 0
total_games = 0
win_perc_history = []

for row in table.find_all("tr"):
    game = [i.text for i in row.find_all("td")]
    if len(game) < 9 or game[8] != "*":
        continue

    total_games += 1
    total_wins += game[7][0]=="W"
    print(f'#{total_games-1} {game[4]} {game[7][0]} (career record {total_wins}-{total_games-total_wins})')
    win_perc_history.append(total_wins/total_games)

exclude = 1
win_perc_history = win_perc_history[exclude:]

fig, ax = plt.subplots(figsize=(10,5))
ax.set_facecolor("#111111")
fig.patch.set_facecolor("#000000")
for spine in ax.spines.values():
    spine.set_color("#888888")


ax.yaxis.label.set_color("#CCCCCC")
ax.xaxis.label.set_color("#CCCCCC")

plt.tick_params(axis='x', colors='white')
plt.tick_params(axis='y', colors='white')


ax.plot(list(range(exclude, exclude+len(win_perc_history))), win_perc_history, linewidth=1, marker='.')

ax.axvline(x=37.5-exclude, color='gray', linestyle='--', linewidth=1, alpha=0.7, zorder=1)

def draw_team(path, record, x, y, zoom=0.18, minus=0.03, fontsize=10):
    logo = mpimg.imread(path)
    imagebox = OffsetImage(logo, zoom=zoom)
    ab = AnnotationBbox(imagebox, (x, y), frameon=False)
    plt.gca().add_artist(ab)

    plt.text(x, y-minus, record, color='white', fontsize=fontsize, ha='center', va='bottom',  fontweight='bold')

draw_team(f"logos/New_York_Jets_2024.svg.png", "13-25", 25, 0.31)
draw_team(f"logos/Carolina_Panthers_logo.svg.png", "8-9", 46, 0.450, zoom=0.25)
draw_team(f"logos/Minnesota_Vikings_logo.svg.png", "14-3", 64, 0.35, minus=0.04)
draw_team(f"logos/Seattle_Seahawks_logo.svg.png", "6-2", 77, 0.42, zoom=0.25, minus=0.03)

plt.annotate(
    '',                   # no label text
    xy=(53, 0.3),     # arrow tip
    xytext=(50, 0.28), # arrow tail
    arrowprops=dict(
        arrowstyle='->',
        color='gray',
        lw=1
    )
)
draw_team(f"logos/sf.png", "0-1", 50, 0.28, zoom=0.3, minus=0.02, fontsize=8)



ax.axvline(x=54.5, color='gray', linestyle='--', linewidth=1, alpha=0.7, zorder=1)
ax.axvline(x=55.5, color='gray', linestyle='--', linewidth=1, alpha=0.7, zorder=1)
ax.axvline(x=72.5, color='gray', linestyle='--', linewidth=1, alpha=0.7, zorder=1)


ax.set_ylabel('Career Win %', fontsize=14)
ax.set_xlabel('Games Played', fontsize=14)
# plt.title('Sam Darnold Career Win % Over Time', color="white")

# for tht second time ever, Sam Darnold has a career win% above .500
# his first time starting off above .500 was when he won his first game ever and started off with a career w-L of 1-0

plt.xlim(6, 82)
# Show the plot
plt.tight_layout()
# plt.show()
plt.savefig("darnold.png", dpi=350)