import numpy as np
import requests
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt, image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.google.com/",
}


team_colors = {
    "BOS": "#bd3039",
    "CHC": "#0e3386",
    "CIN": "#c6011f",
    "CLE": "#e31937",
    "DET": "#0C2340",
    "LAD": "#005a9c",
    "MIL": "#FFC52F",
    "NYY": "#132448",
    "PHI": "#e81828",
    "SEA": "#005c5c",
    "TOR": "#134a8e",
"SDP": "#FFC425",
}

r = requests.get("https://www.spotrac.com/mlb/payroll/_/year/2025", headers=headers)
soup = BeautifulSoup(r.content, "lxml")

table = soup.find("tbody")

fig, ax = plt.subplots(figsize=(10, 5))

x = []
y = []
z = []


for row in table.find_all("tr"):
    team = [i.text.strip() for i in row.find_all("td")]
    name, record, payroll = team[1].split()[0], team[2], team[4]

    payroll = int(payroll.strip("$").replace(",","")) / 1_000_000
    win = int(record.split("-")[0])

    x.append(payroll)
    y.append(win)

    if name.lower() == "sd":
        name="sdp"
    path = f"logos/{name.lower() if name in team_colors else name}.png"
    logo = mpimg.imread(path)
    imagebox = OffsetImage(logo, zoom=0.3)
    ab = AnnotationBbox(imagebox, (payroll, win), frameon=False)
    plt.gca().add_artist(ab)



fig.set_facecolor("#000000")
ax.set_facecolor("#CCCCCC")  # soft off-white background

ax.yaxis.label.set_color("#CCCCCC")
ax.xaxis.label.set_color("#CCCCCC")

plt.tick_params(axis='x', colors='white')
plt.tick_params(axis='y', colors='white')

x = np.array(x); y = np.array(y)
# fit linear regression y = m*x + b
m, b = np.polyfit(x, y, 1)


plt.plot(x, m*x + b, color='#0a0aaa', linewidth=1, linestyle='--', alpha=0.6)

ax.set_xlim(50, 360)
ax.set_ylim(38, 102)

ax.set_xlabel("Payroll (in $m)", fontsize=12)
ax.set_ylabel("Wins", fontsize=12)

plt.tight_layout()
# plt.show()
plt.savefig("payrollvswins.png", dpi=350)
