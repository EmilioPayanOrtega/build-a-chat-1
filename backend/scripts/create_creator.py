import sys
import os

# Add the parent directory to the path so we can import the app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.services import register_user
from app.models import User

app = create_app()

def create_creator_account():
    with app.app_context():
        username = 'creator_demo'
        email = 'creator@demo.com'
        password = 'password123'
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"User '{username}' already exists.")
            return

        try:
            user = register_user(username, email, password, role='creator')
            print(f"Successfully created creator account:")
            print(f"Username: {username}")
            print(f"Email: {email}")
            print(f"Password: {password}")
        except Exception as e:
            print(f"Error creating user: {e}")

if __name__ == '__main__':
    create_creator_account()
