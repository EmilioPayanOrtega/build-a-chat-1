from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from .models import db
from flask_login import LoginManager
from flask_mail import Mail

load_dotenv()

socketio = SocketIO(
    cors_allowed_origins="*",
    async_mode="eventlet",  # MUY IMPORTANTE
    manage_session=False
)

mail = Mail()

def create_app(test_config=None):
    app = Flask(__name__)

    # SECRET KEY
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "fallback-secret")

    # DATABASE (Render)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Mail
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', app.config['MAIL_USERNAME'])

    db.init_app(app)
    mail.init_app(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    socketio.init_app(app)

    # Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/api')

    # Event Handlers
    from . import events
    import importlib
    importlib.reload(events)

    return app
