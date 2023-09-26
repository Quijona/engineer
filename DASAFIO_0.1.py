import requests
import pandas as pd
from sqlalchemy import create_engine

city_name = input("Ciudad: ")
api_key = "437edbf43201768db42fabf3fc0f308e"
api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"

#conection
redshift_user = "joniquiroga251022_coderhouse"
redshift_pass = ""
redshift_host = "data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com"
redshift_port = "5439"  
redshift_database = "data-engineer-database"
table_name = "clima_data"


try:
    response = requests.get(api_url)
    if response.status_code == 200:
        weather_data = response.json()
        df = pd.DataFrame([weather_data])

        # Conectar 
        engine = create_engine(
            f"postgresql://{redshift_user}:{redshift_pass}@{redshift_host}:{redshift_port}/{redshift_database}"
        )
        df.to_sql(table_name, engine, if_exists="replace", index=False)

        print(f"Datos cargados en la tabla {table_name} en Redshift.")
    else:
        print(f"Error en la solicitud HTTP. Código de estado: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Error en la solicitud HTTP. {e}")
except Exception as ex:
    print(f"Ocurrió un error al cargar los datos en Redshift: {ex}")
