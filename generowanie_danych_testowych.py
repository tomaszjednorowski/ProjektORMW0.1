
from pages.Model import *
import faker
import random
import streamlit as st
import pandas as pd
import configparser
from sqlalchemy import create_engine, Select
import sqlalchemy as sqa
from pages.Model import *
from sqlalchemy.orm import sessionmaker
import random

# odczyt konfiguracji
config = configparser.ConfigParser()
config.read('.streamlit\secrets.toml')

server = config['MSSQL']['server']
port = config['MSSQL']['port']
database = config ['MSSQL']['database']
username = config ['MSSQL']['username']
password = config ['MSSQL']['password']

connection_string = f"mssql+pyodbc://{username}:{password}@{server}:{port}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
engine = sqa.create_engine(connection_string)
Session = sessionmaker(bind=engine)
session= Session()

fake = faker.Faker(['cz_CZ'])
fakepl = faker.Faker(['pl_PL'])
for i in range(100):
    
    
    # Generowanie danych dla nowego zwierzaka
    wimie = fake.first_name()
    wmasa = random.randint(1, 50)  # Losowa masa od 1 do 50
    wplec = fake.random_element(elements=["Samiec", "Samica"])
    wtypRasy = 'mieszana'
    wopis = 'opis'  # Generowanie opisu
    wstatusZwierzecia = 'Do adopcji'
    wdataPrzyjecia = fake.date_time()  # Generowanie daty przyjęcia
    wnumerChip = fake.random_number(digits=6)  # Losowy numer chipu
    wwiek = random.randint(1, 15)  # Losowy wiek od 1 do 15 lat
    wboks = fake.random_element(elements=["G1", "G11", "Poziomki"])  # Losowy boks

    # Tworzenie nowego obiektu Zwierze
    nowy_zwierzak = Zwierze(
        imie = wimie,
        masa = wmasa,
        plec = wplec,
        typRasy = wtypRasy,
        opis = wopis,
        statusZwierzecia = wstatusZwierzecia,
        dataPrzyjecia = wdataPrzyjecia,
        numerChip = wnumerChip,
        wiek = wwiek,
        boks = wboks
    )
    
    nowy_kandydat = Kandydat(
        imiona = fakepl.first_name(),
        nazwisko = fakepl.last_name(),
        numerPESEL = fake.random_number(digits=11),
        telefon1 = fake.random_number(digits=9),
        telefon2 = fake.random_number(digits=9),
        mail = fakepl.email()
    )
                     

    # Dodanie nowego zwierzaka do sesji i zatwierdzenie zmian w bazie danych
    session.add(nowy_zwierzak)
    session.add(nowy_kandydat)
    session.commit()