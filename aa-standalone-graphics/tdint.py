import adjustText
import matplotlib.pyplot as plt
import pandas as pd
import requests
from bs4 import BeautifulSoup

r = requests.get("https://www.pro-football-reference.com/years/2025/passing.htm")
soup = BeautifulSoup(r.content, "lxml")

headers = [i.text for i in soup.find("thead").find_all("th")]
count = 0
rows = []

for row in soup.find("tbody").find_all("tr"):
    stats = [i.text for i in row.find_all(["th", "td"])]
    if stats[1] == "League Average" or (stats[1] == "Joe Flacco" and stats[3] != "2TM"):
        continue
    if 12*14 <= int(stats[headers.index("Att")]):
        count += 1
        rows.append({
            "name": stats[1],
            "td": float(stats[headers.index("TD")]),
            "int": float(stats[headers.index("Int")])
        })

fig, ax = plt.subplots(figsize=(12, 6))
df = pd.DataFrame(rows)
ax.scatter(df["int"], df["td"])

texts = []
for _, row in df.iterrows():
    texts.append(
        ax.text(row["int"], row["td"], row["name"])
    )
adjustText.adjust_text(texts)
plt.tight_layout(); plt.show()