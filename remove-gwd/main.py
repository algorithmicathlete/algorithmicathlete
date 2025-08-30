records = {'MIA': [8, 9], 'DET': [15, 2], 'ATL': [8, 9], 'KC': [15, 2], 'LV': [4, 13], 'WAS': [12, 5], 'NYJ': [5, 12], 'SEA': [10, 7], 'PIT': [10, 7], 'PHI': [14, 3], 'LA': [10, 7], 'DEN': [10, 7], 'HOU': [10, 7], 'ARI': [8, 9], 'BAL': [12, 5], 'DAL': [7, 10], 'JAX': [4, 13], 'BUF': [13, 4], 'IND': [8, 9], 'GB': [11, 6], 'CLE': [3, 14], 'NE': [4, 13], 'TEN': [3, 14], 'CAR': [5, 12], 'MIN': [14, 3], 'SF': [6, 11], 'LAC': [11, 6], 'NO': [5, 12], 'TB': [10, 7], 'CIN': [9, 8], 'CHI': [5, 12], 'NYG': [3, 14]}
new_records = {'MIA': [8, 9], 'DET': [11, 6], 'ATL': [8, 9], 'KC': [8, 9], 'LV': [3, 14], 'WAS': [9, 8], 'NYJ': [9, 8], 'SEA': [8, 9], 'PIT': [10, 7], 'PHI': [12, 5], 'LA': [7, 10], 'DEN': [10, 7], 'HOU': [12, 5], 'ARI': [7, 10], 'BAL': [12, 5], 'DAL': [8, 9], 'JAX': [9, 8], 'BUF': [12, 5], 'IND': [5, 12], 'GB': [10, 7], 'CLE': [4, 13], 'NE': [7, 10], 'TEN': [4, 13], 'CAR': [4, 13], 'MIN': [10, 7], 'SF': [9, 8], 'LAC': [13, 4], 'NO': [9, 8], 'TB': [11, 6], 'CIN': [11, 6], 'CHI': [7, 10], 'NYG': [5, 12]}

gwd = {'MIA': 3, 'DET': 4, 'ATL': 3, 'KC': 7, 'LV': 2, 'WAS': 5, 'NYJ': 3, 'SEA': 4, 'PIT': 2, 'PHI': 4, 'LA': 5, 'DEN': 3, 'HOU': 2, 'ARI': 3, 'BAL': 2, 'DAL': 1, 'JAX': 2, 'BUF': 2, 'IND': 5, 'GB': 3, 'CLE': 2, 'NE': 1, 'TEN': 2, 'CAR': 4, 'MIN': 5, 'SF': 1, 'LAC': 2, 'NO': 1, 'TB': 2, 'CIN': 2, 'CHI': 1, 'NYG': 0}
gld = {'MIA': 3, 'DET': 0, 'ATL': 3, 'KC': 0, 'LV': 1, 'WAS': 2, 'NYJ': 7, 'SEA': 2, 'PIT': 2, 'PHI': 2, 'LA': 2, 'DEN': 3, 'HOU': 4, 'ARI': 2, 'BAL': 2, 'DAL': 2, 'JAX': 7, 'BUF': 1, 'IND': 2, 'GB': 2, 'CLE': 3, 'NE': 4, 'TEN': 3, 'CAR': 3, 'MIN': 1, 'SF': 4, 'LAC': 4, 'NO': 5, 'TB': 3, 'CIN': 4, 'CHI': 3, 'NYG': 2}


import csv

with open("gwd.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["team", "record", "new_record", "diff", "gwd", "gld"])
    for (team, (win, loss)), (new_win, new_loss) in zip(records.items(), new_records.values()):
        stats = [team, f"{win} - {loss}", f"{new_win} - {new_loss}", new_win-win, gwd[team], gld[team]]
        print(stats)
        writer.writerow(stats)