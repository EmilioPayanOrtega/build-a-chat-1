from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from .models import db
from flask_login import LoginManager

load_dotenv()

socketio = SocketIO()

def create_app(test_config=None):
    app = Flask(__name__)
    
    # Config
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret!')
    app.config['DEBUG'] = True
    
    if test_config:
        app.config.update(test_config)
    else:
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

    socket_kwargs = {
        'manage_session': False,
        'cors_allowed_origins': ["http://localhost:5173", "http://localhost:3000"]
    }
    
    # Force threading for tests to avoid eventlet issues
    if test_config and test_config.get('TESTING'):
        socket_kwargs['async_mode'] = 'threading'
        socket_kwargs['cors_allowed_origins'] = '*'
    else:
        # For production/dev, we can use default (eventlet/gevent) or force threading if needed.
        # Given run.py uses gevent, we might want to let it auto-detect or force gevent.
        # But for now, let's stick to what it was (threading forced in previous code, or auto).
        # The original code forced threading.
        socket_kwargs['async_mode'] = 'threading'

    socketio.init_app(app, **socket_kwargs)

    # Init LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Import events to register handlers
    from . import events
    import importlib
    importlib.reload(events)
    
    return app