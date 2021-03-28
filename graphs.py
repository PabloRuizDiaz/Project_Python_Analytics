'''
Diseño de graficos
----------------------------------------------------------
En este script se realizan los diversos graficos de barra o lineales
que son implementados para el website.
Funciones:
 1. bar_graph_continent()
 2. bar_graph_continent_death()
 3. ranking_table_graph()
 4. ranking_table_graph_death()
 5. line_graph()
 6. line_graph_death()
 7. line_graph_per_country(country)
'''

##################### Librerias #####################
import requests
import json
import sqlite3


##################### Main Script #####################
def bar_graph_continent():
    '''
    Grafico de barra que muestra el avance de casos de contagio total en el mundo por contiente.
    '''
    
    conn = sqlite3.connect('db_covid_world.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    
    c.execute("""
            SELECT 
            SUM(cases_weekly), continent_exp
            FROM table_covid_world
            GROUP BY continent_exp;
            """)
    
    row = c.fetchall()

    conn.commit()
    conn.close()
    
    return row


def bar_graph_continent_death():
    '''
    Grafico de barra que muestra el avance de casos de muertes total en el mundo por contiente.
    '''
   
    conn = sqlite3.connect('db_covid_world.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    
    c.execute("""
            SELECT 
            SUM(deaths_weekly), continent_exp
            FROM table_covid_world
            GROUP BY continent_exp;
            """)
    
    row = c.fetchall()

    conn.commit()
    conn.close()

    return row


def ranking_table_graph():
    '''
    Tabla donde muestra el top 10 de los paises en el mundo que la peor situacion de contagios por pais.
    '''
    
    conn = sqlite3.connect('db_covid_world.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    
    c.execute("""
            SELECT 
            countries_and_territories, SUM(cases_weekly),
            (SUM(cases_weekly)* 100 / (Select SUM(cases_weekly) From table_covid_world))
            FROM table_covid_world
            GROUP BY countries_and_territories
            ORDER BY SUM(cases_weekly) DESC
            LIMIT 10;
            """)
    
    row = c.fetchall()

    conn.commit()
    conn.close()

    return row


def ranking_table_graph_death():
    '''
    Tabla donde muestra el top 10 de los paises en el mundo con la peor situacion de muertes por pais.
    '''
    
    conn = sqlite3.connect('db_covid_world.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    
    c.execute("""
            SELECT 
            countries_and_territories, SUM(deaths_weekly), 
            (SUM(deaths_weekly)* 100 / (Select SUM(deaths_weekly) From table_covid_world))
            FROM table_covid_world
            GROUP BY countries_and_territories
            ORDER BY SUM(deaths_weekly) DESC
            LIMIT 10;
            """)
    
    row = c.fetchall()

    conn.commit()
    conn.close()

    return row


def line_graph():
    '''
    Grafico de linea temporal (semanal) que muestra el avance de casos de contagio total en el mundo por contienente.
    '''
    
    conn = sqlite3.connect('db_covid_world.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    
    c.execute("""
            SELECT 
            year_week,
            SUM(cases_weekly),
            continent_exp
            FROM table_covid_world
            GROUP BY year_week, continent_exp
            ORDER BY year_week;
            """)

    row = c.fetchall()

    conn.commit()
    conn.close()

    return row


def line_graph_death():
    '''
    Grafico de linea temporal (semanal) que muestra el avance de casos de muertes total en el mundo.
    '''
    
    conn = sqlite3.connect('db_covid_world.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    
    c.execute("""
            SELECT 
            year_week,
            SUM(deaths_weekly),
            continent_exp
            FROM table_covid_world
            GROUP BY year_week, continent_exp
            ORDER BY year_week;
            """)

    row = c.fetchall()

    conn.commit()
    conn.close()

    return row


def line_graph_per_country(country):
    '''
    Grafico de linea temporal que muestra el avance de casos de contagio\muertes total por pais.
    '''

    conn = sqlite3.connect('db_covid_world.db')
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()
    
    c.execute("""
            SELECT 
            year_week,
            SUM(cases_weekly), SUM(deaths_weekly),
            FROM table_covid_world
            WHERE countries_and_territories LIKE ?
            GROUP BY year_week, countries_and_territories
            ORDER BY year_week;
            """, (country,))
    
    row = c.fetchall()

    conn.commit()
    conn.close()

    return row
