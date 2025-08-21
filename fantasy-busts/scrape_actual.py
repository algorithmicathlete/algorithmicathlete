import time
from bs4 import BeautifulSoup
import requests

top_players = {2015: {"Le'Veon Bell": {'ADP': 1, 'PosRank': 1}, 'Adrian Peterson': {'ADP': 2, 'PosRank': 2}, 'Antonio Brown': {'ADP': 3, 'PosRank': 1}, 'Jamaal Charles': {'ADP': 4, 'PosRank': 3}, 'Eddie Lacy': {'ADP': 5, 'PosRank': 4}, 'Marshawn Lynch': {'ADP': 6, 'PosRank': 5}, 'Julio Jones': {'ADP': 7, 'PosRank': 2}, 'Dez Bryant': {'ADP': 8, 'PosRank': 3}, 'Rob Gronkowski': {'ADP': 9, 'PosRank': 1}, 'Odell Beckham Jr.': {'ADP': 10, 'PosRank': 4}, 'C.J. Anderson': {'ADP': 11, 'PosRank': 6}, 'Demaryius Thomas': {'ADP': 12, 'PosRank': 5}}, 2016: {'Antonio Brown': {'ADP': 1, 'PosRank': 1}, 'Julio Jones': {'ADP': 2, 'PosRank': 2}, 'Odell Beckham Jr.': {'ADP': 3, 'PosRank': 3}, 'Todd Gurley II': {'ADP': 4, 'PosRank': 1}, 'DeAndre Hopkins': {'ADP': 5, 'PosRank': 4}, 'A.J. Green': {'ADP': 6, 'PosRank': 5}, 'David Johnson': {'ADP': 7, 'PosRank': 2}, 'Ezekiel Elliott': {'ADP': 8, 'PosRank': 3}, 'Allen Robinson II': {'ADP': 9, 'PosRank': 6}, 'Adrian Peterson': {'ADP': 10, 'PosRank': 4}, 'Rob Gronkowski': {'ADP': 11, 'PosRank': 1}, 'Lamar Miller': {'ADP': 12, 'PosRank': 5}}, 2017: {'David Johnson': {'ADP': 1, 'PosRank': 1}, "Le'Veon Bell": {'ADP': 2, 'PosRank': 2}, 'Antonio Brown': {'ADP': 3, 'PosRank': 1}, 'Julio Jones': {'ADP': 4, 'PosRank': 2}, 'Odell Beckham Jr.': {'ADP': 5, 'PosRank': 3}, 'LeSean McCoy': {'ADP': 6, 'PosRank': 3}, 'Mike Evans': {'ADP': 7, 'PosRank': 4}, 'A.J. Green': {'ADP': 8, 'PosRank': 5}, 'Devonta Freeman': {'ADP': 9, 'PosRank': 4}, 'Melvin Gordon III': {'ADP': 10, 'PosRank': 5}, 'Jordy Nelson': {'ADP': 11, 'PosRank': 6}, 'Michael Thomas': {'ADP': 12, 'PosRank': 7}}, 2018: {'Todd Gurley II': {'ADP': 1, 'PosRank': 1}, "Le'Veon Bell": {'ADP': 2, 'PosRank': 2}, 'David Johnson': {'ADP': 3, 'PosRank': 3}, 'Ezekiel Elliott': {'ADP': 4, 'PosRank': 4}, 'Antonio Brown': {'ADP': 5, 'PosRank': 1}, 'Alvin Kamara': {'ADP': 6, 'PosRank': 5}, 'Saquon Barkley': {'ADP': 7, 'PosRank': 6}, 'DeAndre Hopkins': {'ADP': 8, 'PosRank': 2}, 'Leonard Fournette': {'ADP': 9, 'PosRank': 7}, 'Kareem Hunt': {'ADP': 10, 'PosRank': 8}, 'Odell Beckham Jr.': {'ADP': 11, 'PosRank': 3}, 'Melvin Gordon III': {'ADP': 12, 'PosRank': 9}}, 2019: {'Saquon Barkley': {'ADP': 1, 'PosRank': 1}, 'Christian McCaffrey': {'ADP': 2, 'PosRank': 2}, 'Alvin Kamara': {'ADP': 3, 'PosRank': 3}, 'Ezekiel Elliott': {'ADP': 4, 'PosRank': 4}, 'DeAndre Hopkins': {'ADP': 5, 'PosRank': 1}, 'David Johnson': {'ADP': 6, 'PosRank': 5}, "Le'Veon Bell": {'ADP': 7, 'PosRank': 6}, 'Davante Adams': {'ADP': 8, 'PosRank': 2}, 'James Conner': {'ADP': 9, 'PosRank': 7}, 'Julio Jones': {'ADP': 10, 'PosRank': 3}, 'Michael Thomas': {'ADP': 11, 'PosRank': 4}, 'Odell Beckham Jr.': {'ADP': 12, 'PosRank': 5}}, 2020: {'Christian McCaffrey': {'ADP': 1, 'PosRank': 1}, 'Saquon Barkley': {'ADP': 2, 'PosRank': 2}, 'Ezekiel Elliott': {'ADP': 3, 'PosRank': 3}, 'Dalvin Cook': {'ADP': 4, 'PosRank': 4}, 'Michael Thomas': {'ADP': 5, 'PosRank': 1}, 'Alvin Kamara': {'ADP': 6, 'PosRank': 5}, 'Derrick Henry': {'ADP': 7, 'PosRank': 6}, 'Davante Adams': {'ADP': 8, 'PosRank': 2}, 'Josh Jacobs': {'ADP': 9, 'PosRank': 7}, 'Joe Mixon': {'ADP': 10, 'PosRank': 8}, 'Clyde Edwards-Helaire': {'ADP': 11, 'PosRank': 9}, 'Miles Sanders': {'ADP': 12, 'PosRank': 10}}, 2021: {'Christian McCaffrey': {'ADP': 1, 'PosRank': 1}, 'Dalvin Cook': {'ADP': 2, 'PosRank': 2}, 'Alvin Kamara': {'ADP': 3, 'PosRank': 3}, 'Derrick Henry': {'ADP': 4, 'PosRank': 4}, 'Ezekiel Elliott': {'ADP': 5, 'PosRank': 5}, 'Davante Adams': {'ADP': 6, 'PosRank': 1}, 'Travis Kelce': {'ADP': 7, 'PosRank': 1}, 'Aaron Jones Sr.': {'ADP': 8, 'PosRank': 6}, 'Saquon Barkley': {'ADP': 9, 'PosRank': 7}, 'Austin Ekeler': {'ADP': 10, 'PosRank': 8}, 'Jonathan Taylor': {'ADP': 11, 'PosRank': 9}, 'Nick Chubb': {'ADP': 12, 'PosRank': 10}}, 2022: {'Jonathan Taylor': {'ADP': 1, 'PosRank': 1}, 'Christian McCaffrey': {'ADP': 2, 'PosRank': 2}, 'Austin Ekeler': {'ADP': 3, 'PosRank': 3}, 'Cooper Kupp': {'ADP': 4, 'PosRank': 1}, 'Derrick Henry': {'ADP': 5, 'PosRank': 4}, 'Justin Jefferson': {'ADP': 6, 'PosRank': 2}, 'Dalvin Cook': {'ADP': 7, 'PosRank': 5}, 'Najee Harris': {'ADP': 8, 'PosRank': 6}, "Ja'Marr Chase": {'ADP': 9, 'PosRank': 3}, 'Joe Mixon': {'ADP': 10, 'PosRank': 7}, 'Davante Adams': {'ADP': 11, 'PosRank': 4}, 'Stefon Diggs': {'ADP': 12, 'PosRank': 5}}, 2023: {'Justin Jefferson': {'ADP': 1, 'PosRank': 1}, 'Christian McCaffrey': {'ADP': 2, 'PosRank': 1}, "Ja'Marr Chase": {'ADP': 3, 'PosRank': 2}, 'Austin Ekeler': {'ADP': 4, 'PosRank': 2}, 'Travis Kelce': {'ADP': 5, 'PosRank': 1}, 'Tyreek Hill': {'ADP': 6, 'PosRank': 3}, 'Saquon Barkley': {'ADP': 7, 'PosRank': 3}, 'Bijan Robinson': {'ADP': 8, 'PosRank': 4}, 'Stefon Diggs': {'ADP': 9, 'PosRank': 4}, 'Nick Chubb': {'ADP': 10, 'PosRank': 5}, 'Davante Adams': {'ADP': 11, 'PosRank': 5}, 'CeeDee Lamb': {'ADP': 12, 'PosRank': 6}}, 2024: {'Christian McCaffrey': {'ADP': 1, 'PosRank': 1}, 'CeeDee Lamb': {'ADP': 2, 'PosRank': 1}, 'Tyreek Hill': {'ADP': 3, 'PosRank': 2}, 'Bijan Robinson': {'ADP': 4, 'PosRank': 2}, 'Breece Hall': {'ADP': 5, 'PosRank': 3}, 'Amon-Ra St. Brown': {'ADP': 6, 'PosRank': 3}, "Ja'Marr Chase": {'ADP': 7, 'PosRank': 4}, 'Justin Jefferson': {'ADP': 8, 'PosRank': 5}, 'Saquon Barkley': {'ADP': 9, 'PosRank': 4}, 'A.J. Brown': {'ADP': 10, 'PosRank': 6}, 'Jonathan Taylor': {'ADP': 11, 'PosRank': 5}, 'Garrett Wilson': {'ADP': 12, 'PosRank': 7}}}


what_ifs = []
busts = []

def scrape_actual_year(year):
    r = requests.get(f"https://www.pro-football-reference.com/years/{year}/fantasy.htm")
    soup = BeautifulSoup(r.content, "lxml")

    table = soup.find("tbody")

    for row in table.find_all("tr"):
        player = [x.text for x in row.find_all("td")]
        if not player:
            continue

        try:
            name, position, games, points, pos_rank = player[0].strip("+*"), player[2], int(player[4]), float(player[-6]), int(player[-2])
        except ValueError:
            continue

        ppg = points / games
        pre = top_players[year].get(name)

        player = {
            "name": name,
            "year": year,
            "adp": pre["ADP"] if pre else None,
            "adpr": pre["PosRank"] if pre else None,
            "pos_rank": pos_rank,
            "ppg": ppg,
            "games": games
        }

        if ((ppg > 18 and position != "QB") or (ppg > 25 and position == "QB") or pre) and games <= 10:
            what_ifs.append(player)

        if pre:
            if player["pos_rank"]-player["adpr"] >= 15 and games > 10:
                busts.append(player)


if __name__ == '__main__':
    for year in range(2015, 2025):
        print(year)
        scrape_actual_year(year)
        print()
        time.sleep(1)


    print(busts)
    print(what_ifs)



