import csv

busts= [{'name': 'Eddie Lacy', 'year': 2015, 'adp': 5, 'adpr': 4, 'pos_rank': 25, 'ppg': 9.373333333333333, 'games': 15}, {'name': 'C.J. Anderson', 'year': 2015, 'adp': 11, 'adpr': 6, 'pos_rank': 30, 'ppg': 9.42, 'games': 15}, {'name': 'DeAndre Hopkins', 'year': 2016, 'adp': 5, 'adpr': 4, 'pos_rank': 36, 'ppg': 12.3375, 'games': 16}, {'name': 'David Johnson', 'year': 2016, 'adp': 7, 'adpr': 2, 'pos_rank': 71, 'ppg': 1.0625, 'games': 16}, {'name': 'Mike Evans', 'year': 2017, 'adp': 7, 'adpr': 4, 'pos_rank': 20, 'ppg': 13.54, 'games': 15}, {'name': 'Jordy Nelson', 'year': 2017, 'adp': 11, 'adpr': 6, 'pos_rank': 50, 'ppg': 9.146666666666667, 'games': 15}, {'name': "Le'Veon Bell", 'year': 2019, 'adp': 7, 'adpr': 6, 'pos_rank': 21, 'ppg': 14.333333333333334, 'games': 15}, {'name': 'Davante Adams', 'year': 2019, 'adp': 8, 'adpr': 2, 'pos_rank': 29, 'ppg': 17.724999999999998, 'games': 12}, {'name': 'Odell Beckham Jr.', 'year': 2019, 'adp': 12, 'adpr': 5, 'pos_rank': 31, 'ppg': 12.58125, 'games': 16}, {'name': 'David Johnson', 'year': 2019, 'adp': 6, 'adpr': 5, 'pos_rank': 37, 'ppg': 10.884615384615385, 'games': 13}, {'name': 'Saquon Barkley', 'year': 2021, 'adp': 9, 'adpr': 7, 'pos_rank': 34, 'ppg': 11.430769230769231, 'games': 13}, {'name': 'Jonathan Taylor', 'year': 2022, 'adp': 1, 'adpr': 1, 'pos_rank': 36, 'ppg': 13.30909090909091, 'games': 11}, {'name': 'Austin Ekeler', 'year': 2023, 'adp': 4, 'adpr': 2, 'pos_rank': 31, 'ppg': 13.242857142857144, 'games': 14}, {'name': 'Breece Hall', 'year': 2024, 'adp': 5, 'adpr': 3, 'pos_rank': 18, 'ppg': 15.05625, 'games': 16}, {'name': 'Tyreek Hill', 'year': 2024, 'adp': 3, 'adpr': 2, 'pos_rank': 23, 'ppg': 12.835294117647058, 'games': 17}]
what_ifs = [{'name': 'Julian Edelman', 'year': 2015, 'adp': None, 'adpr': None, 'pos_rank': 38, 'ppg': 19.166666666666668, 'games': 9}, {'name': 'Keenan Allen', 'year': 2015, 'adp': None, 'adpr': None, 'pos_rank': 47, 'ppg': 20.1875, 'games': 8}, {'name': "Le'Veon Bell", 'year': 2015, 'adp': 1, 'adpr': 1, 'pos_rank': 46, 'ppg': 18.533333333333335, 'games': 6}, {'name': 'Steve Smith Sr.', 'year': 2015, 'adp': None, 'adpr': None, 'pos_rank': 51, 'ppg': 18.714285714285715, 'games': 7}, {'name': 'Jamaal Charles', 'year': 2015, 'adp': 4, 'adpr': 3, 'pos_rank': 51, 'ppg': 20.22, 'games': 5}, {'name': 'Marshawn Lynch', 'year': 2015, 'adp': 6, 'adpr': 5, 'pos_rank': 56, 'ppg': 11.814285714285715, 'games': 7}, {'name': 'Dez Bryant', 'year': 2015, 'adp': 8, 'adpr': 3, 'pos_rank': 79, 'ppg': 9.899999999999999, 'games': 9}, {'name': 'Arian Foster', 'year': 2015, 'adp': None, 'adpr': None, 'pos_rank': 65, 'ppg': 19.25, 'games': 4}, {'name': 'A.J. Green', 'year': 2016, 'adp': 6, 'adpr': 5, 'pos_rank': 34, 'ppg': 18.64, 'games': 10}, {'name': 'Rob Gronkowski', 'year': 2016, 'adp': 11, 'adpr': 1, 'pos_rank': 22, 'ppg': 12.125, 'games': 8}, {'name': 'Adrian Peterson', 'year': 2016, 'adp': 10, 'adpr': 4, 'pos_rank': 125, 'ppg': 3.0, 'games': 3}, {'name': 'Ezekiel Elliott', 'year': 2017, 'adp': None, 'adpr': None, 'pos_rank': 9, 'ppg': 20.32, 'games': 10}, {'name': 'Odell Beckham Jr.', 'year': 2017, 'adp': 5, 'adpr': 3, 'pos_rank': 82, 'ppg': 18.5, 'games': 4}, {'name': 'David Johnson', 'year': 2017, 'adp': 1, 'adpr': 1, 'pos_rank': 123, 'ppg': 13.0, 'games': 1}, {'name': 'Leonard Fournette', 'year': 2018, 'adp': 9, 'adpr': 7, 'pos_rank': 36, 'ppg': 15.05, 'games': 8}, {'name': 'James Conner', 'year': 2019, 'adp': 9, 'adpr': 7, 'pos_rank': 33, 'ppg': 14.55, 'games': 10}, {'name': 'Dak Prescott', 'year': 2020, 'adp': None, 'adpr': None, 'pos_rank': 31, 'ppg': 27.119999999999997, 'games': 5}, {'name': 'Joe Mixon', 'year': 2020, 'adp': 10, 'adpr': 8, 'pos_rank': 49, 'ppg': 16.599999999999998, 'games': 6}, {'name': 'Christian McCaffrey', 'year': 2020, 'adp': 1, 'adpr': 1, 'pos_rank': 51, 'ppg': 30.133333333333336, 'games': 3}, {'name': 'Michael Thomas', 'year': 2020, 'adp': 5, 'adpr': 1, 'pos_rank': 103, 'ppg': 11.985714285714286, 'games': 7}, {'name': 'Marcus Mariota', 'year': 2020, 'adp': None, 'adpr': None, 'pos_rank': 46, 'ppg': 25.8, 'games': 1}, {'name': 'Antonio Williams', 'year': 2020, 'adp': None, 'adpr': None, 'pos_rank': 94, 'ppg': 21.3, 'games': 1}, {'name': 'Saquon Barkley', 'year': 2020, 'adp': 2, 'adpr': 2, 'pos_rank': 119, 'ppg': 7.7, 'games': 2}, {'name': 'Derrick Henry', 'year': 2021, 'adp': 4, 'adpr': 4, 'pos_rank': 14, 'ppg': 24.1625, 'games': 8}, {'name': 'Christian McCaffrey', 'year': 2021, 'adp': 1, 'adpr': 1, 'pos_rank': 44, 'ppg': 18.214285714285715, 'games': 7}, {'name': 'Cooper Kupp', 'year': 2022, 'adp': 4, 'adpr': 1, 'pos_rank': 22, 'ppg': 22.37777777777778, 'games': 9}, {'name': 'Justin Jefferson', 'year': 2023, 'adp': 1, 'adpr': 1, 'pos_rank': 26, 'ppg': 20.22, 'games': 10}, {'name': 'Nick Chubb', 'year': 2023, 'adp': 10, 'adpr': 5, 'pos_rank': 87, 'ppg': 11.55, 'games': 2}, {'name': 'Chris Godwin', 'year': 2024, 'adp': None, 'adpr': None, 'pos_rank': 56, 'ppg': 19.685714285714287, 'games': 7}, {'name': 'Christian McCaffrey', 'year': 2024, 'adp': 1, 'adpr': 1, 'pos_rank': 73, 'ppg': 11.95, 'games': 4}]

for bust in busts:
    bust["ppg"] = round(bust["ppg"], 1)

for what_if in what_ifs:
    what_if["ppg"] = round(what_if["ppg"], 1)


injury_busts = [x for x in what_ifs if x['adp'] is not None]
what_ifs = [x for x in what_ifs if x['adp'] is None]

for player in busts+injury_busts+what_ifs:
    player["position"] = input(f"{player['name']}: ")

for player in busts+injury_busts:
    adp = str(player['adp'])
    if len(adp) == 2:
        player['adp'] = f'1.{adp}'
    else:
        player['adp'] = f'1.0{adp}'


# Leveon didnt play in 2018 (ranked #2)

busts = list(sorted(busts, key=lambda x: x["pos_rank"]-x["adpr"], reverse=True))
what_ifs = list(sorted(what_ifs, key=lambda x: x["ppg"], reverse=True))
injury_busts = list(sorted(injury_busts, key=lambda x: x["ppg"], reverse=True))
