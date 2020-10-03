from pathlib import Path
from datetime import datetime

import pandas as pd


def convert_to_dt(string_dt):
    return datetime.strptime(string_dt, "%Y/%m/%d %H:%M:%S")


def load_transform_raw_data(filename, ):
    if isinstance(filename, str):
        # Running from the terminal
        fp = Path(filename)
        timestamps = pd.read_csv(fp, skiprows=2)
   
    else:
        # Running from the webapp
        # filename is the _io.StringIO uploaded file
        filename.seek(0)
        timestamps = pd.read_csv(filename, skiprows=2)        

    timestamps = timestamps[timestamps["氏名"].notna()] # '氏名' = 'name'
    timestamps["timestamp"] = timestamps["日時"].apply(convert_to_dt)
    timestamps["date"] = timestamps["timestamp"].apply(lambda dt: dt.date())
    timestamps["time"] = timestamps["timestamp"].apply(lambda dt: dt.time())
    return timestamps


def clock_in_clock_out(timestamps):
    timestamps = timestamps[["timestamp", "date", "time", "氏名"]]
    timestamps.set_index("timestamp", inplace=True)
    clock_in = timestamps.groupby(["氏名", "date"]).min() \
        .rename(columns={"time": "Clock In"})
    clock_out = timestamps.groupby(["氏名", "date"]).max() \
        .rename(columns={"time": "Clock Out"})
    timecards = clock_in.join(clock_out).reset_index()
    return timecards


def make_timecards(filename):
    timestamps = load_transform_raw_data(filename)
    timecards = clock_in_clock_out(timestamps)
    
    if isinstance(filename, str):
        # Running from the terminal
        timecards.to_csv("February Timecards script.csv")

    else:
        # Running from the web app
        return timecards


if __name__ == "__main__":
    make_timecards("Feb 2020_converted.csv")
