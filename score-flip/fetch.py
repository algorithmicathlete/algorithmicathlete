import random
import time
from collections import defaultdict

import requests
from bs4 import BeautifulSoup

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

records = defaultdict(lambda: {"wins": 0, "losses": 0, "ties": 0, "num_1score": 0, "real_wins": 0, "real_losses": 0, "one_score_wins": 0, "one_score_losses": 0})

for week in range(1, 19):
    r = requests.get(f"https://www.espn.com/nfl/schedule/_/week/{week}/year/2025/seasontype/2", headers=headers)
    soup = BeautifulSoup(r.content, "lxml")

    for result in soup.find_all("td", {"class": "teams__col Table__TD"}):
        (w_name, w_score), (l_name, l_score) = [x.split() for x in result.text.replace(" (OT)", "").split(", ")]
        if w_score == l_score:
            print(result.text)
            records[w_name]["ties"] += 1
            records[l_name]["ties"] += 1
            continue

        records[w_name]["real_wins"] += 1
        records[l_name]["real_losses"] += 1

        if (int(w_score) - int(l_score)) <= 8: # one score
            records[w_name]["num_1score"] += 1
            records[l_name]["num_1score"] += 1
            records[w_name]["one_score_wins"] += 1
            records[l_name]["one_score_losses"] += 1
            w_name, l_name = l_name, w_name

        records[w_name]["wins"] += 1
        records[l_name]["losses"] += 1

    print(week, "done")
    time.sleep(3+random.random()-0.5)

print(records)
for k, v in records.items():
    print(k,f'{v["wins"]}-{v["losses"]}{"-"+str(v["ties"]) if v["ties"] else ""}')