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
from flask_mail import Mail
mail = Mail()

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
    
    # Mail Config
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', app.config['MAIL_USERNAME'])
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Init extensions
    db.init_app(app)
    mail.init_app(app)
    
    # Relaxed CORS for debugging
    CORS(app, resources={r"/*": {"origins": "*"}})

    socket_kwargs = {
        'manage_session': False,
        'cors_allowed_origins': "*"
    }
    
    if test_config and test_config.get('TESTING'):
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
    app.register_blueprint(main_blueprint, url_prefix='/api')

    # Import events to register handlers
    from . import events
    import importlib
    importlib.reload(events)
    
    return app