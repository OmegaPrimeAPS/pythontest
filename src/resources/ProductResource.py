from flask import request
from flask_restful import Resource
from databases.db_pg import get_db_connection
from models.ProductModel import Product

class ProductResource(Resource):
    def get(self, product_id=None):
        with get_db_connection() as connection:
            cursor = connection.cursor()
            if product_id:
                cursor.execute("SELECT * FROM Products WHERE id = %s", (product_id,))
                product = cursor.fetchone()
                if product:
                    return {
                        'sku': product[1],
                        'name': product[2],
                        'price': product[3],
                        'brand': product[4]
                    }
                else:
                    return {'error': 'Producto no encontrado'}, 404
            else:
                cursor.execute("SELECT * FROM Products")
                products = cursor.fetchall()
                result = []
                for product in products:
                    result.append({
                        'sku': product[1],
                        'name': product[2],
                        'price': product[3],
                        'brand': product[4]
                    })
                return result

    def post(self):
        data = request.get_json()
        product = Product(
            sku=data['sku'],
            name=data['name'],
            price=data['price'],
            brand=data['brand']
        )
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                'INSERT INTO Products (sku, name, price, brand) VALUES (%s, %s, %s, %s)',
                (product.sku, product.name, product.price, product.brand)
            )
            connection.commit()
        return {'message': 'Producto agregado correctamente'}, 201

    def put(self, product_id):
        product = Product.query.get(product_id)
        print(product)
        if product:
            data = request.get_json()
            print(data)
            product.sku = data['sku']
            product.name = data['name']
            product.price = data['price']
            product.brand = data['brand']
            with get_db_connection() as connection:
                cursor = connection.cursor()
                cursor.execute('UPDATE public."Products" SET sku = %s, name = %s, price = %s, brand = %s WHERE id = %s',
                            (product.sku, product.name, product.price, product.brand, product_id))
                connection.commit()
            return {'message': 'Producto actualizado correctamente'}
        else:
            return {'error': 'Producto no encontrado'}, 404

    def delete(self, product_id):
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM public."Products" WHERE id = %s', (product_id,))
            product = cursor.fetchone()

        if product:
            cursor.execute('DELETE FROM public."Products" WHERE id = %s', (product_id,))
            connection.commit()
            return {'message': 'Producto eliminado correctamente'}
        else:
            return {'error': 'Producto no encontrado'}, 404
