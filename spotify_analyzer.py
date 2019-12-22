#!/usr/bin/env python
__author__ = "Maximilian Werner"

import json
from collections import defaultdict
from nltk import FreqDist
import datetime


def read_data(filename):
    """
    load streaming history from a JSON file
    """
    try:
        with open(filename, "r", encoding="utf8") as f:
            raw_data = json.load(f)
            return raw_data
            print("test")
    except FileNotFoundError:
        print("Error: file not found")


def assemble_history(files):
    """
    assembles all given streaming history files into a dictionary
    """
    data = []
    for file in files:
        data += read_data(file)
    return data


def general_info(history, year):
    print(f"Minutes listened in {year}:", end=" ")
    minutes = (int(sum([entry["msPlayed"] for entry in history if entry["endTime"].startswith(year)]) / 1000 / 60))
    print(f"{minutes} ({int(minutes/60)} hours)")

    print(f"Number of different songs listened to in {year}:", end=" ")
    print(len(set([entry["trackName"] for entry in history if entry["endTime"].startswith(year)])))

    print(f"Number of different artists listened to in {year}:", end=" ")
    print(len(set([entry["artistName"] for entry in history if entry["endTime"].startswith(year)])))

    print(f"10 favorite songs in {year}:")
    for song, times_played in FreqDist([entry["trackName"] for entry in history
                                        if entry["endTime"].startswith(year)]).most_common(10):
        print(f"  {song}: {times_played} times played")

    print(f"10 favorite artists in {year} and their playtime:")
    artist_playtime_tuples = [(entry["artistName"], entry["msPlayed"]) for entry in history
                              if entry["endTime"].startswith(year)]

    dic = defaultdict(int)
    for key, ms in artist_playtime_tuples:
        dic[key] += ms / 1000 / 60 / 60

    for artist, ms in sorted(dic.items(), key=lambda i: i[1], reverse=True)[:10]:
        print(f"  {artist}: {int(ms)}h {int((ms * 60) % 60)}min playtime")

# print("Day with longest playtime:")


def day_summary(day, month, year, history_dic):
    """
    prints listening history for given day plus total played time on that day
    """
    date = f"{year}-{month}-{day}"
    songs = [(entry["trackName"], entry["artistName"], get_start_time(entry["endTime"], entry["msPlayed"]),
              entry["msPlayed"]) for entry in history_dic if entry["endTime"].startswith(date)
             and entry["msPlayed"] > 5000]
    playtime = 0
    print(f"Listening history for {day}.{month}.{year}:")
    for title, artist, time, ms in songs:
        print(f"{time}: {artist} - {title}")
        playtime += ms / 1000 / 60 / 60
    print(f"Total playtime on this day: {int(playtime)}h {int((playtime * 60) % 60)}min")


def get_start_time(end_time, ms):
    """
    helper function for "day_summary"
    determines startTime by subtracting time played from endTime
    """
    start_time = datetime.datetime.strptime(end_time + ":00.000000", '%Y-%m-%d %H:%M:%S.%f')
    string = start_time - datetime.timedelta(milliseconds=ms)
    return str(string.time())[:5]


def run():
    file_names = ["streaming_history0.json", "streaming_history1.json", "streaming_history2.json"]
    input_year = "2019"
    history = assemble_history(file_names)

    general_info(history, input_year)
    day_summary("06", "12", 2019, history)


if __name__ == '__main__':
    run()









