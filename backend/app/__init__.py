from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from .models import db

load_dotenv()

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    
    # Config
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret!')
    app.config['DEBUG'] = True
    
    DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'chatbotdb')
    DB_PORT = os.getenv('DB_PORT', '3306')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Init extensions
    db.init_app(app)
    CORS(app, resources={r"/*": {
        "origins": ["http://localhost:5173", "http://localhost:3000"],
        "supports_credentials": True
    }})
    socketio.init_app(app, async_mode='gevent', manage_session=False, cors_allowed_origins=["http://localhost:5173", "http://localhost:3000"])

    # Register Blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Import events to register handlers
    from . import events



    return app
