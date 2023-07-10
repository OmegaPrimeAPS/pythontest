import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

class TestEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
   
    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to the Index page", response.data)
    
    def test_register(self):
        with self.client:
            # Simular una solicitud POST al endpoint /register con datos simulados
            response = self.client.post("/register", data={
                "username_reg": "testuser",
                "email_reg": "testuser@example.com",
                "password1": "password123",
                "password2": "password123"
            })
            
            # Verificar que la respuesta tenga el código 302 (redirección)
            self.assertEqual(response.status_code, 302)
            
            # Verificar que la sesión esté configurada correctamente
            with self.app.session_transaction() as sess:
                self.assertTrue(sess["logged_in"])
                self.assertEqual(sess["admin_user_username"], "testuser")
            
            # Verificar que la redirección sea correcta
            self.assertEqual(response.location, "http://localhost/")  # Ajusta la URL de redirección según tu configuración
    
    def test_login(self):
        with self.client:
            # Simular una solicitud POST al endpoint /login con datos simulados
            response = self.client.post("/login", data={
                "username": "testuser",
                "password": "password123"
            })
            
            # Verificar que la respuesta tenga el código 302 (redirección)
            self.assertEqual(response.status_code, 302)
            
            # Verificar que la sesión esté configurada correctamente
            with self.app.session_transaction() as sess:
                self.assertTrue(sess["logged_in"])
                self.assertEqual(sess["admin_user_username"], "testuser")
            
            # Verificar que la redirección sea correcta
            self.assertEqual(response.location, "http://localhost/")  # Ajusta la URL de redirección según tu configuración
    
    
    def test_list_users(self):
        response = self.client.get("/list_users")
        self.assertEqual(response.status_code, 200)
        # Aquí puedes agregar más aserciones para verificar el contenido de la respuesta
    
    def test_list_products(self):
        response = self.client.get("/list_products")
        self.assertEqual(response.status_code, 200)
        # Aquí puedes agregar más aserciones para verificar el contenido de la respuesta
    
    # Agrega más pruebas para los demás endpoints
    
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
