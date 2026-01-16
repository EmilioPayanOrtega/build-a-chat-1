# backend/app/__init__.py
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
import os
import logging # Temporal, solo para ver logs
from dotenv import load_dotenv
from .models import db
from flask_login import LoginManager
from flask_mail import Mail

load_dotenv()

socketio = SocketIO(
    cors_allowed_origins="*",
    async_mode="eventlet",
    manage_session=False
)

mail = Mail()

def create_app(test_config=None):
    app = Flask(__name__)

    # Temporal. Imprime los logs en Render
    if not app.debug:
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.INFO)
    
    # SECRET KEY
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "fallback-secret")

        # DATABASE URL (Render)
    raw_db_uri = os.environ.get("DATABASE_URL", "").strip()

    if raw_db_uri:
        # Render usa postgres:// → convertir a SQLAlchemy + driver explícito para psycopg3
        if raw_db_uri.startswith("postgresql://"):
            # convertir postgres:// -> postgresql+psycopg://
            raw_db_uri = raw_db_uri.replace("postgresql://", "postgresql+psycopg://", 1)
        elif raw_db_uri.startswith("postgresql://"):
            raw_db_uri = raw_db_uri.replace("postgresql://", "postgresql+psycopg://", 1)

        # Asegurar SSL obligatorio en Render si no viene (Render Postgres requiere SSL)
        if "?sslmode=" not in raw_db_uri and "?" not in raw_db_uri:
            raw_db_uri += "?sslmode=require"
        elif "?sslmode=" not in raw_db_uri and "?" in raw_db_uri:
            raw_db_uri += "&sslmode=require"

        db_uri = raw_db_uri
    else:
        db_uri = "sqlite:///../dev.sqlite3"
        app.logger.warning("DATABASE_URL no definida: usando SQLite de fallback")


    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # MAIL CONFIG
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', app.config['MAIL_USERNAME'])

    # Init extensions
    db.init_app(app)
    mail.init_app(app)
    socketio.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Importar modelos para que SQLAlchemy los registre
    from .models import User, Chatbot, Node, ChatSession, Message
    
    # Crear las tablas automaticamente si no existen
    with app.app_context():
        db.create_all()
        app.logger.info("Tablas de la base de datos creadas o verificadas.")
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/api')

    # Socket events
    from . import events
    import importlib
    importlib.reload(events)

    # Logging de la URI (enmascarada)
    try:
        masked = db_uri
        if "@" in masked:
            pre, post = masked.split("@", 1)
            if ":" in pre:
                userinfo = pre.split("://", 1)[-1]
                masked = masked.replace(userinfo + "@", "****@")
        app.logger.info("DB URI cargada: %s", masked)
    except Exception:
        pass

    return app
