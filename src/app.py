from flask import Flask
from routes import configure_routes, api_bp
from config import config
import os


def create_app(config_name):
    app = Flask(__name__)
    app.debug = True
    
    app.config.from_object(config["development"])
    app.config.from_object(config[config_name])
    configure_routes.configure_routes(app)
    
    


    app.register_blueprint(api_bp, url_prefix="/api")
    
    return app



if __name__ == "__main__":
    app = create_app("development")
    app.run(debug=True)
    
