import pytest
from app import create_app
from app.models import db

@pytest.fixture
def app():
    from sqlalchemy.pool import StaticPool
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_POOLCLASS": StaticPool,
        "SQLALCHEMY_ENGINE_OPTIONS": {"connect_args": {"check_same_thread": False}}
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def socket_client(app):
    from app import socketio
    return socketio.test_client(app, flask_test_client=app.test_client())

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
