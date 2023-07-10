import psycopg2
from psycopg2 import DatabaseError
from flask import jsonify
from databases.db_pg import get_db_connection


class AdminUsers:
    def __init__(self, id, usarname, email, password):
        self.id = id
        self.usarname = usarname
        self.email = email
        self.password = password

    def get_all_users():
        try:
            connection = get_db_connection()
            print(connection)
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM adminusers')

            data = cursor.fetchall()

            return data

        except DatabaseError as ex:
            print("Error:", ex)
            
    def get_all_emails():
        try:
            connection = get_db_connection()
            print(connection)
            cursor = connection.cursor()
            cursor.execute('SELECT email FROM adminusers')

            data = cursor.fetchall()

            return data

        except DatabaseError as ex:
            print("Error:", ex)
        
