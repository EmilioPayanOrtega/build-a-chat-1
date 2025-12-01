import pytest
from app.services import register_user, authenticate_user
from app.models import User, db

def test_register_user_success(app):
    with app.app_context():
        user = register_user("testuser", "test@example.com", "password123")
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.id is not None
        
        db_user = db.session.get(User, user.id)
        assert db_user is not None
        assert db_user.role == 'user'

def test_register_creator_success(app):
    with app.app_context():
        user = register_user("creator", "creator@example.com", "password123", role="creator")
        assert user.role == "creator"

def test_register_user_missing_data(app):
    with app.app_context():
        with pytest.raises(ValueError, match="Missing data"):
            register_user("", "test@example.com", "password123")

def test_register_user_duplicate(app):
    with app.app_context():
        register_user("testuser", "test@example.com", "password123")
        with pytest.raises(ValueError, match="Username or email already exists"):
            register_user("testuser", "other@example.com", "password456")

def test_authenticate_user_success(app):
    with app.app_context():
        register_user("testuser", "test@example.com", "password123")
        user = authenticate_user("testuser", "password123")
        assert user.username == "testuser"

def test_authenticate_user_invalid_credentials(app):
    with app.app_context():
        register_user("testuser", "test@example.com", "password123")
        with pytest.raises(ValueError, match="Invalid username/email or password"):
            authenticate_user("testuser", "wrongpassword")

def test_authenticate_user_missing_data(app):
    with app.app_context():
        with pytest.raises(ValueError, match="Incomplete data"):
            authenticate_user("", "password123")
