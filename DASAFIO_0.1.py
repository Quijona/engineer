import configparser
import json
from sqlalchemy import create_engine
import pandas as pd
import requests
import os
os.environ['SQLALCHEMY_WARN_20'] = '0'

if __name__ == "__main__":
    def create_table(engine):
        # Define la estructura de la tabla en Redshift
        with engine.connect() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS clima_data1 (
                    coord VARCHAR(MAX),
                    weather VARCHAR(MAX),
                    base VARCHAR(MAX),
                    main VARCHAR(MAX),
                    visibility INT,
                    wind VARCHAR(MAX),
                    clouds VARCHAR(MAX),
                    dt INT,
                    sys VARCHAR(MAX),
                    timezone INT,
                    id INT,
                    name VARCHAR(MAX),
                    cod INT
                )
            """)


    def insert_data(engine, data):
        # Inserta los datos en la tabla
        with engine.connect() as connection:
            # Asegúrate de que los datos JSON estén en un formato válido
            data['coord'] = json.dumps(data['coord'])
            data['weather'] = json.dumps(data['weather'])
            data['main'] = json.dumps(data['main'])
            data['wind'] = json.dumps(data['wind'])
            data['clouds'] = json.dumps(data['clouds'])
            data['sys'] = json.dumps(data['sys'])

            connection.execute("""
                INSERT INTO clima_data1 (coord, weather, base, main, visibility, wind, clouds, dt, sys, timezone, id, name, cod)
                VALUES (%(coord)s, %(weather)s, %(base)s, %(main)s, %(visibility)s, %(wind)s, %(clouds)s, %(dt)s, %(sys)s, %(timezone)s, %(id)s, %(name)s, %(cod)s)
            """, data)


    city_name = input("Ciudad: ")
    api_key = "437edbf43201768db42fabf3fc0f308e"
    api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"

    # Crear un objeto ConfigParser
    config = configparser.ConfigParser()

    # Leer el archivo de configuración
    config.read('desafio/config.ini')

    # Acceder a las variables de entorno
    redshift_user = config['redshift']['user']
    redshift_pass = config['redshift']['password']
    redshift_host = config['redshift']['host']
    redshift_port = config['redshift']['port']
    redshift_database = config['redshift']['database']
    table_name = "clima_data1"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            weather_data = response.json()
            # Transformar datos JSON a cadenas JSON
            for key in weather_data:
                if isinstance(weather_data[key], dict):
                    weather_data[key] = json.dumps(weather_data[key])

            # Conectar
            engine = create_engine(
                f'redshift+psycopg2://{redshift_user}:{redshift_pass}@{redshift_host}:{redshift_port}/{redshift_database}'
            )

            # crea la tabla si no existe
            create_table(engine)

            # Inserta los datos en la tabla
            insert_data(engine, weather_data)

            print(f"Datos cargados en la tabla {table_name} en Redshift.")
        else:
            print(
                f"Error en la solicitud HTTP. Código de estado: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud HTTP. {e}")
    except Exception as ex:
        print(f"Ocurrió un error al cargar los datos en Redshift: {ex}")