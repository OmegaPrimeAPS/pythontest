from decouple import config
import os

class Config:
    SECRET_KEY = config('SECRET_KEY')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_TLS = True
    MAIL_USERNAME = 'octaviojauregui31@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASS')
    

class DevelopmentConfig(Config):
    DEBUG = True
    
class TestingConfig(Config):
    DEBUG = True
    

config = {
    'development': DevelopmentConfig,
    "testing": TestingConfig
}

# Resto del código...

