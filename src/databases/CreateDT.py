from databases.db_pg import get_db_connection

def create_admin_users_table():
    with get_db_connection() as connection:
        cursor = connection.cursor()
        create_table_query = '''
        CREATE TABLE AdminUsers (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL
        )
        '''
        cursor.execute(create_table_query)
        connection.commit()

def create_product_table():
    with get_db_connection() as connection:
        cursor = connection.cursor()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS Product (
            id SERIAL PRIMARY KEY,
            sku VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            price NUMERIC(10, 2) NOT NULL,
            brand VARCHAR(255) NOT NULL
        )
        '''
        cursor.execute(create_table_query)
        connection.commit()
