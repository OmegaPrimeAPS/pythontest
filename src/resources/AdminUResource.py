from flask import request , jsonify ,render_template
from flask_restful import Resource
from databases.db_pg import get_db_connection
from models.entitites.AdminUser import AdminUser

class AdminUserResource(Resource):
    def get(self):
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM AdminUsers WHERE id = %s", (admin_id,))
            admin_user = cursor.fetchone()

        if admin_user:
            # El administrador existe, devolver información
            admin_data = {
                "id": admin_user[0],
                "username": admin_user[1],
                "email": admin_user[3]
            }
            return jsonify(admin_data)
        else:
            # El administrador no existe, devolver error
            return jsonify({"error": "Administrador no encontrado"}), 404


    def post(self):
        username = request.form["username_reg"]
        email = request.form["email_reg"]
        password1 = request.form["password1"]

        admin_user = AdminUser(
            username=username,
            password=password1,
            email=email
        )

        with get_db_connection() as connection:
              # Verificar si la tabla AdminUsers existe
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM AdminUsers WHERE email = %s", (email,))
            existing_user = cursor.fetchone()
            if existing_user:
                # El usuario ya existe, mostrar mensaje de alerta
                error_message = "El usuario ya existe."
                return render_template("register.html", error_message=error_message)
            cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name='AdminUsers')")
            table_exists = cursor.fetchone()[0]

            if not table_exists:
                # Crear la tabla AdminUsers
                cursor.execute(
                    """
                    CREATE TABLE AdminUsers (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(255) NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        email VARCHAR(255) NOT NULL
                    )
                    """
                )
                connection.commit()
                print('Tabla AdminUsers creada')
                
            print('Conexión exitosa a la base de datos')
            cursor = connection.cursor()
            cursor.execute(
                'INSERT INTO AdminUsers (username, password, email) VALUES (%s, %s, %s)',
                (admin_user.username, admin_user.password, admin_user.email)
            )
            connection.commit()

        return {'message': 'Usuario administrador agregado correctamente'}, 201


    def put(self, admin_id):
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")

        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM AdminUsers WHERE id = %s", (admin_id,))
            admin_user = cursor.fetchone()

            if admin_user:
                # El administrador existe, actualizar información
                cursor.execute("UPDATE AdminUsers SET username = %s, email = %s WHERE id = %s",
                            (username, email, admin_id))
                connection.commit()
                return jsonify({"message": "Administrador actualizado correctamente"})
            else:
                # El administrador no existe, devolver error
                return jsonify({"error": "Administrador no encontrado"}), 404


    def delete(self, admin_id):
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM AdminUsers WHERE id = %s", (admin_id,))
            admin_user = cursor.fetchone()

        if admin_user:
            # El administrador existe, eliminarlo
            cursor.execute("DELETE FROM AdminUsers WHERE id = %s", (admin_id,))
            connection.commit()
            return jsonify({"message": "Administrador eliminado correctamente"})
        else:
            # El administrador no existe, devolver error
            return jsonify({"error": "Administrador no encontrado"}), 404
