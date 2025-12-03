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

r = requests.get("https://www.footballdb.com/statistics/300-yard-passing.html?yr=2024", headers=headers)
soup = BeautifulSoup(r.content, "lxml")

count = 0
week_num = 0
for week in soup.find_all("tbody"):
    week_num += 1
    print(f"WEEK {week_num}")
    for game in week.find_all("tr"):
        count += 1

        print(count, [i.text for i in game.find_all("td")])

print(count)
# 46