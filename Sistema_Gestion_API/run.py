from flask import Flask
from flask_cors import CORS
from config import Config
from app.models import db
from app.routes import main
from flask import Flask
from app.routes import main

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS
    app.config.from_object(Config)  # Load config from Config class

    db.init_app(app)  # Initialize the database with the app
    app.register_blueprint(main)  # Register routes
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
