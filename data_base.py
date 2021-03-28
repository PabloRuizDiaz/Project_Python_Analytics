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
    [pop_data_2019] -> 
    [continent_exp] -> 
    [Cumulative_number_for_14_days_of_COVID_19_cases_per_100000] ->
'''


##################### Librerias #####################
# Libreria para Base de datos
import requests
import json
import sqlite3


API_REQUEST = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/json'


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
            [date_rep] DATE,
            [year_week] TEXT,
            [cases_weekly] INTEGER,
            [deaths_weekly] INTEGER,
            [countries_and_territories] TEXT,
            [geo_id] TEXT,
            [country_territory_Code] TEXT,
            [pop_data_2019] INTEGER,
            [continent_exp] TEXT,
            [Cumulative_number_for_14_days_of_COVID_19_cases_per_100000] TEXT
            );
            """)
    
    conn.commit()
    conn.close()


def actualise_table_SQL():
    '''
    Se carga los datos extraidos del json a la tabla "table_covid_world"
    '''

    conn = sqlite3.connect('db_covid_world.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()

    response = requests.get(API_REQUEST, timeout=60)
    json_data = response.json()

    data = json_data.get('records')

    for datum in data:
        c.execute("""
                INSERT INTO table_covid_world 
                (date_rep, year_week, cases_weekly, deaths_weekly, countries_and_territories,
                geo_id, country_territory_Code, pop_data_2019, continent_exp, 
                Cumulative_number_for_14_days_of_COVID_19_cases_per_100000)
                VALUES ('{}', strftime('%Y-%W','{}'), {}, {}, '{}', '{}', '{}', '{}', '{}', '{}');
                """ .format(datum["dateRep"],datum["dateRep"],datum["cases"],datum["deaths"],datum["countriesAndTerritories"],
                datum["geoId"],datum["countryterritoryCode"],datum["popData2019"],datum["continentExp"],
                datum["Cumulative_number_for_14_days_of_COVID-19_cases_per_100000"]))
    
    conn.commit()
    conn.close()


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