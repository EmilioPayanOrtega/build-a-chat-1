from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User

def register_user(username, email, password):
    if not (username and email and password):
        raise ValueError('Missing data')
    
    if User.query.filter((User.username == username) | (User.email == email)).first():
        raise ValueError('Username or email already exists')

    try:
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except Exception as e:
        db.session.rollback()
        raise e

def authenticate_user(username, password):
    if not (username and password):
        raise ValueError('Incomplete data')
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password_hash, password):
        raise ValueError('Invalid username or password')

    return user
