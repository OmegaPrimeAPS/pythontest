import psycopg2
from psycopg2 import DatabaseError
from decouple import config
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_connection():
    try:
        host = os.getenv("DB_HOST")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        database = os.getenv("DB_NAME")
        connection = psycopg2.connect(
            host=host, user=user, password=password, database=database
        )
        print(connection)
        print("Conexión exitosa a la base de datos")

        return connection

    except DatabaseError as ex:
        print("Error al establecer la conexión a la base de datos:", ex)
        raise ex


get_db_connection()
