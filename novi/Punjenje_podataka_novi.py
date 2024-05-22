from sqlalchemy.orm import sessionmaker
import pymysql
import pandas as pd
import numpy as np
import json
import requests
import random
from sqlalchemy import create_engine

# Učitavanje CSV datoteke
CSV_FILE_PATH = r'c:\Users\Ivana\OneDrive\Desktop\SIR\SIR_projekt\novi\Crash_Data_novi.csv'
df = pd.read_csv(CSV_FILE_PATH, delimiter=',', low_memory=False)
print("CSV size: ", df.shape)

# Ispis prvih redaka dataframe-a
print(df.head())

# Uklanjanje dupliciranih Crash ID
df = df.drop_duplicates(subset=['Crash ID'])

# Database connection
user = 'root'
passw = 'root'
host = 'localhost'
port = 3306
database = 'prometne_nesrece'

mydb = create_engine('mysql+pymysql://' + user + ':' + passw +
                     '@' + host + ':' + str(port) + '/' + database, echo=False)
print(mydb)
connection = mydb.connect()

# Popunjavanje tablice state
state_names = df['State'].unique().tolist()
state_data = pd.DataFrame({'name': state_names})
state_data.to_sql(con=mydb, name='state', if_exists='append', index=False)

# Popunjavanje tablice holiday
holiday_data = pd.DataFrame(
    {'christmas_period': df['Christmas Period'], 'easter_period': df['Easter Period']})
holiday_data.to_sql(con=mydb, name='holiday', if_exists='append', index=False)


# Popunjavanje tablice hour
hour_data = []

for i, row in df.iterrows():
    month = row['Month']
    year = row['Year']
    dayweek = row['Dayweek']
    time = row['Time']
    time_of_day = row['Time of day']
    day_of_week = row['Day of week']

    hour_entry = {
        'month': month,
        'year': year,
        'dayweek': dayweek,
        'time': time,
        'time_of_day': time_of_day,
        'day_of_week': day_of_week
    }

    hour_data.append(hour_entry)

hour_df = pd.DataFrame(hour_data)
hour_df.to_sql(con=mydb, name='hour', if_exists='append', index=False)


# Popunjavanje tablice other_participants
other_participants_data = []

for i, row in df.iterrows():
    bus_involvement = row['Bus Involvement']
    heavy_rigid_truck_involvement = row['Heavy Rigid Truck Involvement']
    articulated_truck_involvement = row['Articulated Truck Involvement']

    other_participant_data = {
        'bus_involvement': bus_involvement,
        'heavy_rigid_truck_involvement': heavy_rigid_truck_involvement,
        'articulated_truck_involvement': articulated_truck_involvement
    }

    other_participants_data.append(other_participant_data)

# Zadržavamo originalne indekse
other_participants_df = pd.DataFrame(other_participants_data, index=df.index)
other_participants_df.to_sql(
    con=mydb, name='other_participants', if_exists='append', index=False)


# Popunjavanje tablice victim
victim_data = []

for i, row in df.iterrows():
    road_user = row['Road User']
    gender = row['Gender']
    age = row['Age']
    age_group = row['Age Group']

    other_participants_id = i + 1  # Koristimo indeks df za referenciranje

    victim_entry = {
        'road_user': road_user,
        'gender': gender,
        'age': age,
        'age_group': age_group,
        'other_participants_fk': other_participants_id
    }

    victim_data.append(victim_entry)

victim_df = pd.DataFrame(victim_data)
victim_df.to_sql(con=mydb, name='victim', if_exists='append', index=False)

# punjenje tablice speed

speed_data = []

for i, row in df.iterrows():
    speed_limit = row['Speed Limit']

    speed_entry = {
        'speed_limit': speed_limit
    }

    speed_data.append(speed_entry)

# Pretvaranje u DataFrame
speed_df = pd.DataFrame(speed_data)

# Popunjavanje tablice 'speed' u bazi
speed_df.to_sql(con=mydb, name='speed', if_exists='append', index=False)

# Učitavanje CSV datoteke
CRASH_CSV_PATH = r'c:\Users\Ivana\OneDrive\Desktop\SIR\SIR_projekt\novi\Crashtablica.csv'
crash_df = pd.read_csv(CRASH_CSV_PATH)

# Popunjavanje tablice crash
crash_data = []

for i, row in crash_df.iterrows():
    crash_entry = {
        'id': row['Crash ID'],
        'type': row['Crash Type'],
        'penalty_price': row['Penalty Price'],
        'state_fk': row['State_id'],
        'hour_fk': row['Hour_id'],
        'victim_fk': row['Victim_id'],
        'speed_fk': row['Speed_id'],
        'holiday_fk': row['Holiday_id']
    }
    crash_data.append(crash_entry)

# Pretvaranje u DataFrame
crash_df = pd.DataFrame(crash_data)

# Popunjavanje tablice 'crash' u bazi
crash_df.to_sql(con=mydb, name='crash', if_exists='append', index=False)
