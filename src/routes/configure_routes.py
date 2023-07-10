from flask import render_template, request, redirect, session, url_for
from resources.ProductResource import ProductResource
from resources.AdminUResource import AdminUserResource
from databases.CreateDT import create_admin_users_table
from databases.db_pg import get_db_connection
import traceback
from models.ProductModel import Product
from models.AdminUsersModel import AdminUsers
import os, psycopg2

from flask import jsonify




def configure_routes(app):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/cerrar_session", methods=["GET"])
    def cerrar_session():
        session.clear()  # Limpiar todos los datos de sesión
        return redirect(url_for("index"))  # Redireccionar a la página de inicio

    @app.route("/lista_usuarios", methods=["GET","POST"])
    def lista_usuarios():
        return render_template("lista_usuarios.html")
    
    @app.route("/productos", methods=["GET","POST"])
    def form():
        return render_template("agregar_productos.html")
    
    @app.route("/users", methods=["GET","POST"])
    def users():
        return render_template("agregar_usuarios.html")
    
    @app.route("/inicio", methods=["GET","POST"])
    def inicio():
        return render_template("login.html")

    @app.route("/register", methods = ["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form["username_reg"]
            email = request.form["email_reg"]
            password1 = request.form["password1"]
            password2 = request.form["password2"]
        
            if password1 != password2:
                error_message = "Las contraseñas no coinciden. Inténtalo de nuevo."
                return render_template("register.html", error_message=error_message)
            
            # Crear el nuevo usuario
            admin_user = AdminUserResource.post({
                    'username': username,
                    'email': email,
                    'password': password1
                })
            print(admin_user)
            if admin_user:
                session["logged_in"] = True
                session["admin_user_id"] = admin_user.id
                session["admin_user_username"] = admin_user.username
                with get_db_connection() as connection:
                    print('Conexión exitosa a la base de datos')
                    if not connection.dialect.has_table(connection,'AdminUsers'):
                        print('no se pudo crear base de datos')
                        create_admin_users_table()  
                return redirect(url_for("index"))  # Redireccionar a la página de dashboard o cualquier otra página después del registro exitoso
            else:
                error_message = "Error al crear el usuario. Inténtalo de nuevo."
                return render_template("register.html", error_message=error_message)
        else:
            return render_template("register.html")
    
    @app.route("/login", methods=["GET","POST"])
    def login():
        username = request.form["username"]
        password = request.form["password"]

        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM AdminUsers WHERE username = %s AND password = %s", (username, password))
            admin_user = cursor.fetchone()

        if admin_user:
            # El administrador existe, iniciar sesión y almacenar información en la sesión
            session["logged_in"] = True
            session["admin_user_id"] = admin_user[0]
            session["admin_user_username"] = admin_user[1]
            return redirect(url_for("index"))  # Redireccionar a la página de dashboard o cualquier otra página después del inicio de sesión
        else:
            error_message = "Credenciales inválidas. Inténtalo de nuevo."
            return render_template("login.html", error_message=error_message)
    

    
    @app.route("/list_users", methods=["GET"])
    def list_users():
        try:
            users = AdminUsers.get_all_users()
            print(AdminUsers)
            user_list = []
            for row in users:
                user = {
                    "id": row[0],
                    "username": row[1],
                    "email": row[2],
                }
                user_list.append(user)
            return jsonify({"users": user_list})
        except Exception as ex:
            return jsonify({"error": "Error al obtener los usuarios de la base de datos"}), 500
    
    @app.route("/list_products", methods=["GET"])
    def list_products():
        try:
            products = Product.get_all_products()
            print(products)
            product_list = []
            for row in products:
                product = {
                    "id": row[0],
                    "sku": row[1],
                    "name": row[2],
                    "price": str(row[3]),
                    "brand": row[4]
                }
                product_list.append(product)
            return jsonify({"products": product_list})
        except Exception as ex:
            return jsonify({"error": "Error al obtener los productos de la base de datos"}), 500
        
    @app.route("/delete_product/<int:product_id>", methods=['GET', 'DELETE'])
    def delete_product(product_id):
            with get_db_connection() as connection:
                cursor = connection.cursor()
                cursor.execute('SELECT * FROM public."Products" WHERE id = %s', (product_id,))
                product = cursor.fetchone()
                #username = session.get("admin_user_username")

                if product:
                    cursor.execute('DELETE FROM public."Products" WHERE id = %s', (product_id,))
                    #####aqui llamo la libreria mail######
                    ''' mails = AdminUsers.get_all_emails()  # Obtener las direcciones de correo electrónico de los administradores
                    msg = Message('Eliminación de producto',
                                sender=app.config['MAIL_USERNAME'],
                                recipients=mails)
                    msg.html = render_template('email.html', username=username, product_name=product[2])
                    
                    mail.send(msg) '''
                    return redirect(url_for("index"))
                else:
                    return redirect(url_for("index"))   

            
    @app.route("/delete_user/<int:id>", methods=['GET', 'DELETE'])
    def delete_user(id):
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM adminusers WHERE id = %s', (id,))
            product = cursor.fetchone()

            if product:
                cursor.execute('DELETE FROM adminusers WHERE id = %s', (id,))
                connection.commit()
                return redirect(url_for("lista_usuarios"))
            else:
                return redirect(url_for("lista_usuarios"))
      
    @app.route("/agregar_producto", methods=["GET", "POST"])
    def agregar_producto():
        if request.method == "POST":
            sku = request.form.get("sku")
            name = request.form.get("name")
            price = request.form.get("price")
            brand = request.form.get("brand")
            
            with get_db_connection() as connection:
                cursor = connection.cursor()
                cursor.execute('INSERT INTO public."Products" (sku, name, price, brand) VALUES (%s, %s, %s, %s)',
                            (sku, name, price, brand))
                connection.commit()

                return redirect(url_for("index"))

            

        return render_template("agregar_producto.html") 
        
    @app.route("/agregar_usuario", methods=["GET", "POST"])
    def agregar_usuario():
        if request.method == "POST":
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")

            
            with get_db_connection() as connection:
                cursor = connection.cursor()
                cursor.execute('INSERT INTO adminusers(username, email, password) VALUES (%s, %s, %s)',
                            (username, email, password))
                connection.commit()

                return redirect(url_for("users"))

            

        return redirect(url_for('lista_usuarios')) 
      
    @app.route('/editar_producto/<int:id>', methods=['GET', 'POST'])
    def editar_producto(id):
        if request.method == 'GET':
            with get_db_connection() as connection:
                cursor = connection.cursor()
                cursor.execute('SELECT * FROM public."Products" WHERE id = %s', (id,))
                product = cursor.fetchone()
                print(product)
            
            # Renderizar la plantilla de edición y pasar los datos del producto
            return render_template('editar_producto.html', product=product)
        
        elif request.method == 'POST':
            # Obtener los datos actualizados del formulario
            sku = request.form.get('sku')
            name = request.form.get('name')
            price = request.form.get('price')
            brand = request.form.get('brand')
            
            # Realizar la actualización en la base de datos usando el ID
            with get_db_connection() as connection:
                cursor = connection.cursor()
                cursor.execute('UPDATE public."Products" SET sku = %s, name = %s, price = %s, brand = %s WHERE id = %s',
                            (sku, name, price, brand, id))
                connection.commit()
            
            # Redirigir a la página de listado de productos después de la actualización
            return redirect(url_for('index'))
    @app.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
    def editar_usuario(id):
            if request.method == 'GET':
                with get_db_connection() as connection:
                    cursor = connection.cursor()
                    cursor.execute('SELECT * FROM adminusers WHERE id = %s', (id,))
                    user = cursor.fetchone()
                    print(user)
                
                # Renderizar la plantilla de edición y pasar los datos del producto
                return render_template('editar_usuario.html', user=user)
            
            elif request.method == 'POST':
                # Obtener los datos actualizados del formulario
                
                username = request.form.get('username')
                email = request.form.get('email')
                password = request.form.get('password')
                
                # Realizar la actualización en la base de datos usando el ID
                with get_db_connection() as connection:
                    cursor = connection.cursor()
                    cursor.execute('UPDATE adminusers SET username = %s, email = %s, password = %s WHERE id = %s',
                                (username, email, password, id))
                    connection.commit()
                
                # Redirigir a la página de listado de productos después de la actualización
                return redirect(url_for('lista_usuarios'))
        
 
    
    # Agrega más rutas según tus necesidades
    #API
    