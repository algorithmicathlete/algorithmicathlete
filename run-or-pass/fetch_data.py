import nfl_data_py as nfl

if __name__ == '__main__':
    pbp = nfl.import_pbp_data([2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024])

    pbp = pbp[pbp['play_type'].isin(['run', 'pass'])]

    features = [
        'down', 'ydstogo', 'yardline_100', 'score_differential', 'half_seconds_remaining', 'shotgun'
    ]

    X = pbp[features].copy()
    y = (pbp['play_type'] == 'pass').astype(int)

    df = X.copy()
    df['target'] = y
    df.to_csv("play_data.csv", index=False)