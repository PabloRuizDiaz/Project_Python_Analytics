'''
BASE DE DATOS DE COVID-19
------------------------------------------------------------------------------------------
Website oficial:
    De: European Centre for Disease Prevention and Control - An agency of the European Union
    https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide

En este script se definen los comandos basicos para crear y cargar la informacion
extraida del json de la URL https://opendata.ecdc.europa.eu/covid19/casedistribution/json
donde sera guardada en una base de datos SQL. La misma estara utilizando las bases de 
SQLite.

Contiene dos funciones principales:
    create_table() -> se crea la base de datos con su correspondiente tabla "table_covid_world";
    actualise_table() -> se carga los datos extraidos del json a la tabla "table_covid_world".

Sus Campos son:
    [id] -> identificador unico creciente
    [date_rep] -> Fecha del reportye (Formato: DD/MM/YYYY)
    [year_week] -> Fecha con formato año-semana (numerico)
    [cases_weekly] -> Cantidad de casos por semana
    [deaths_weekly] -> Cantidad de muertes por semana
    [countries_and_territories] -> Paises y territorios mundiales
    [geo_id] -> identificador geografico
    [country_territory_Code] -> Codigo mundial del territorio
    [pop_data_2019] -> poblacion en 2019
    [continent_exp] -> 
    [Cumulative_number_for_14_days_of_COVID_19_cases_per_100000] ->
'''

__author__ = "Pablo Martin Ruiz Diaz"
__email__ = "rd.pablo@gmail.com"
__version__ = "2.0"


##################### Librerias #####################
# Libreria JSON
import requests
import json
# Libreria Base de datos
import sqlite3
import os
from datetime import datetime, timedelta
# Libreria ORM
from flask_sqlalchemy import SQLAlchemy


API_REQUEST = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/json'


db = SQLAlchemy()

class TableCovidWorld(db.Model):
    __tablename__ = "table_covid_world"
    
    id = db.Column(db.Integer, primary_key=True)
    date_rep = db.Column(db.String)
    year_week = db.Column(db.String)
    cases_weekly = db.Column(db.Integer)
    deaths_weekly = db.Column(db.Integer)
    countries_and_territories = db.Column(db.String)
    geo_id = db.Column(db.Integer)
    country_territory_Code = db.Column(db.String)
    pop_data_2019 = db.Column(db.Integer)
    continent_exp = db.Column(db.String)
    Cumulative_number_for_14_days_of_COVID_19_cases_per_100000 = db.Column(db.Integer)
    
    def __repr__(self):
        return f"""id {self.id}\ndate_rep {self.date_rep}\nyear_week {self.year_week}\ncases_weekly {self.cases_weekly}\n
                deaths_weekly {self.deaths_weekly}\ncountries_and_territories {self.countries_and_territories}\ngeo_id {self.geo_id}\n
                country_territory_Code {self.country_territory_Code}\npop_data_2019 {self.pop_data_2019}\ncontinent_exp {self.continent_exp}\n
                Cumulative_number_for_14_days_of_COVID_19_cases_per_100000 {self.Cumulative_number_for_14_days_of_COVID_19_cases_per_100000}\n\n"""


##################### Main Script #####################
def create_table_SQL():
    '''
    Crea la base de datos con su correspondiente tabla "table_covid_world";
    '''

    conn = sqlite3.connect('db_covid_world.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()

    c.execute("""
            DROP TABLE IF EXISTS table_covid_world;
            """)
    
    c.execute("""
            CREATE TABLE table_covid_world(
            [id] INTEGER PRIMARY KEY AUTOINCREMENT,
            [date_rep] TEXT,
            [year_week] TEXT,
            [cases_weekly] INTEGER,
            [deaths_weekly] INTEGER,
            [countries_and_territories] TEXT,
            [geo_id] INTEGER,
            [country_territory_Code] TEXT,
            [pop_data_2019] INTEGER,
            [continent_exp] TEXT,
            [Cumulative_number_for_14_days_of_COVID_19_cases_per_100000] INTEGER
            );
            """)
    
    conn.commit()
    conn.close()


def reset_table_SQL():
    '''
    Borra toda la informacion de la base de datos "table_covid_world";
    '''

    db.drop_all()

    db.create_all()


def actualise_table_SQL():
    '''
    Se carga los datos extraidos del json a la tabla "table_covid_world"
    '''

    response = requests.get(API_REQUEST, timeout=60)
    json_data = response.json()

    data = json_data.get('records')

    for datum in data:
        insert_datum = TableCovidWorld(date_rep=datum["dateRep"],year_week=datetime.strptime(datum["dateRep"],'%d/%m/%Y').strftime("%y-%W"),
                                        cases_weekly=datum["cases"],deaths_weekly=datum["deaths"],
                                        countries_and_territories=datum["countriesAndTerritories"],
                                        geo_id=datum["geoId"],country_territory_Code=datum["countryterritoryCode"],
                                        pop_data_2019=datum["popData2019"],continent_exp=datum["continentExp"],
                                        Cumulative_number_for_14_days_of_COVID_19_cases_per_100000=datum["Cumulative_number_for_14_days_of_COVID-19_cases_per_100000"])
        db.session.add(insert_datum)
    
    db.session.commit()


def list_all_countries():
    '''
    Listado de todos los Paises y territorios del mundo.
    '''
    
    conn = sqlite3.connect('db_covid_world.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()

    c.execute(""" SELECT geo_id, countries_and_territories FROM table_covid_world 
            GROUP BY countries_and_territories;""")
    
    all_countries = c.fetchall()

    conn.commit()
    conn.close()

    return all_countries
