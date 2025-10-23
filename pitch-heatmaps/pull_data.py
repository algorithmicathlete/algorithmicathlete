from pybaseball import statcast, cache
from datetime import timedelta, datetime
import pandas as pd

cache.enable()

curr_date = datetime.strptime("2025-9-30", "%Y-%m-%d")
end_date = datetime.strptime("2025-10-20", "%Y-%m-%d")

all_data = []

while curr_date < end_date:
    next_date = curr_date + timedelta(days=7)
    print(f"Getting from {curr_date.date()} to {next_date.date()}")
    df = statcast(start_dt=curr_date.strftime("%Y-%m-%d"), end_dt=next_date.strftime("%Y-%m-%d"))
    all_data.append(df)

    curr_date = next_date + timedelta(days=1)

final_df = pd.concat(all_data, ignore_index=True)
final_df.to_csv('statcast_data_2025.csv', index=False)
