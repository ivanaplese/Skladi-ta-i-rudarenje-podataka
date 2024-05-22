import pandas as pd
import numpy as np
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Time, Boolean
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import pymysql  # osigurajte da je pymysql instaliran

# Putanja do predprocesiranog skupa podataka
CSV_FILE_PATH = r'c:\Users\Ivana\OneDrive\Desktop\SIR\SIR_projekt\novi\Crash_Data_novi.csv'
# Učitavanje predprocesiranog skupa podataka
df = pd.read_csv(CSV_FILE_PATH, delimiter=',', low_memory=False)
print("CSV size: ", df.shape)  # Ispis broja redaka i stupaca
print(df.head())  # Ispis prvih redaka dataframe-a
df.replace('', np.nan, inplace=True)

Base = declarative_base()  # Stvaranje baze
user = 'root'
passw = 'root'
host = 'localhost'
port = 3306
database = 'prometne_nesrece'

mydb = create_engine('mysql+pymysql://' + user + ':' + passw +
                     '@' + host + ':' + str(port) + '/' + database, echo=False)
print(mydb)
connection = mydb.connect()

# Tablica za mjesto nesreće


class State(Base):
    __tablename__ = 'state'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)

# Tablica za vrijeme nesreće


class Hour(Base):
    __tablename__ = 'hour'
    id = Column(Integer, primary_key=True)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    dayweek = Column(String(10), nullable=False)
    time = Column(Time, nullable=True)
    time_of_day = Column(String(5), nullable=False)
    day_of_week = Column(String(20), nullable=False)

# Tablica za onesrecenog


class Victim(Base):
    __tablename__ = 'victim'
    id = Column(Integer, primary_key=True)
    road_user = Column(String(30), nullable=False)
    gender = Column(String(15), nullable=True)
    age = Column(Integer, nullable=False)
    age_group = Column(String(20), nullable=True)
    other_participants_fk = Column(
        Integer, ForeignKey('other_participants.id'))

# Tablica za ostale sudionike nesreće


class Other_participants(Base):
    __tablename__ = 'other_participants'
    id = Column(Integer, primary_key=True)
    bus_involvement = Column(String(10), nullable=True)
    heavy_rigid_truck_involvement = Column(String(10), nullable=True)
    articulated_truck_involvement = Column(String(10), nullable=True)

# Tablica za ograničenje na cesti


class Speed(Base):
    __tablename__ = 'speed'
    id = Column(Integer, primary_key=True, autoincrement=True)
    speed_limit = Column(Integer, nullable=True)

# Tablica za godišnje blagdane


class Holiday(Base):
    __tablename__ = 'holiday'
    id = Column(Integer, primary_key=True)
    christmas_period = Column(String(10), nullable=False)
    easter_period = Column(String(10), nullable=False)


# Tablica crash
class Crash(Base):
    __tablename__ = 'crash'
    id = Column(Integer, primary_key=True,)
    type = Column(String(20), nullable=False)
    penalty_price = Column(Integer, nullable=False)
    state_fk = Column(Integer, nullable=False)
    hour_fk = Column(Integer, nullable=False)
    victim_fk = Column(Integer, nullable=False)
    speed_fk = Column(Integer, nullable=False)
    holiday_fk = Column(Integer, nullable=False)


# Kreiranje tablica u bazi
Base.metadata.create_all(mydb)
