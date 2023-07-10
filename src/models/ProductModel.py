import psycopg2
from psycopg2 import DatabaseError
from flask import jsonify
from databases.db_pg import get_db_connection

class Product:
    def __init__(self, id, sku, name, price, brand):
        self.id = id
        self.sku = sku
        self.name = name
        self.price = price
        self.brand = brand

    def get_all_products():
        try:
            connection = get_db_connection()
            print(connection)
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM public."Products"')
            
            data = cursor.fetchall()
            
            return data

        except DatabaseError as ex:
            print("Error:", ex)
            

    

    