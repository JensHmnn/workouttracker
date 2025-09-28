#Script to generate a .db file with 200 randomized entries
#200個のランダムエントリを含む .db ファイルを生成するスクリプト

# Imports
import pandas as pd
import numpy as np
import random
import datetime
import sqlalchemy

# Function to generate random dates
# ランダムな日付を生成する関数です
def generate_random_dates(start_date, end_date, num_dates):
    """
    Generates a list of random dates within a specified range.
    指定された範囲内のランダムな日付のリストを生成するメソッド
    
    Args:
        start_date (datetime.date): The earliest possible date.
        end_date (datetime.date): The latest possible date.
        num_dates (int): The number of random dates to generate.

    Returns:
        list: A list of datetime.date objects, each representing a random date.
    """
    date_list = []
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days

    while len(date_list) < num_dates:
        random_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_days)
        if random_date not in date_list:
            date_list.append(random_date)

    date_list.sort()
    return date_list

# Function to generate a Pandas df of 200 random workout entries
# 0個のランダムなエントリーのデータフレームをする関数
def generate_random_df():
    """Generates a Pandas dataframe of 200 random workout entries with data for the columns: ID, Date, Workout, Calories, Duration.
    200個のランダムなエントリーのデータフレームを作成する。列のラベルはID, Date, Workout, Calories, Durationだ。"""

    db_randm = pd.DataFrame()

    # Create ID col
    # 「ID」の列
    id_list = []
    for n in range(1, 201):
        id_list.append(n)
    db_randm["ID"] = id_list

    # Create Date col
    # 「Date」（日付）の列
    start = datetime.date(2024, 1, 1)
    end = datetime.date(2025, 12, 31)
    num_dates = 200
    db_randm["Date"] = generate_random_dates(start, end, num_dates)

    # Create Workout list
    # 「Workout」（運動種類）の列
    workout_list = []
    for n in range(num_dates):
        x = random.randint(0, 2)
        if x == 0:
            workout_list.append("Upper Body")
        elif x == 1:
            workout_list.append("Lower Body")
        else:
            workout_list.append("Cardio")
    
    db_randm["Workout"] = workout_list

    # Create cols for workout durations and burned calories
    # 「Calories」（消費カロリー）と「Duration」（運動時間）の列
    duration_list = [random.randint(20, 181) for n in range(num_dates)]
    calories_list = [round(170/30*n)+random.randint(-45, 45) for n in duration_list]
    db_randm["Calories"]  = calories_list
    db_randm["Duration"] = duration_list

    # Return df
    return db_randm

# Export to .db file
# データフレームを.dbファイルに書き出す
random_workouts = generate_random_df()
engine = sqlalchemy.create_engine("sqlite:///C:\\Users\\jensh\Desktop\\Workout\\workout.db", echo=False)
random_workouts.to_sql("workout", con=engine, index=False, if_exists="replace")
