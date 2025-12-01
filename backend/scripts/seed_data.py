import sys
import os

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.services import register_user
from app.models import User

def seed_data():
    app = create_app()
    with app.app_context():
        print("=== Seeding Database ===")
        
        # Creators
        creators = [
            {'username': 'creator_alice', 'email': 'alice@example.com', 'password': 'password123'},
            {'username': 'creator_bob', 'email': 'bob@example.com', 'password': 'password123'}
        ]
        
        for c in creators:
            if not User.query.filter_by(email=c['email']).first():
                try:
                    register_user(c['username'], c['email'], c['password'], role='creator')
                    print(f"Created Creator: {c['username']} ({c['email']})")
                except Exception as e:
                    print(f"Failed to create {c['username']}: {e}")
            else:
                print(f"Creator {c['username']} already exists.")

        # Users
        users = [
            {'username': 'user_charlie', 'email': 'charlie@example.com', 'password': 'password123'},
            {'username': 'user_dave', 'email': 'dave@example.com', 'password': 'password123'}
        ]
        
        for u in users:
            if not User.query.filter_by(email=u['email']).first():
                try:
                    register_user(u['username'], u['email'], u['password'], role='user')
                    print(f"Created User: {u['username']} ({u['email']})")
                except Exception as e:
                    print(f"Failed to create {u['username']}: {e}")
            else:
                print(f"User {u['username']} already exists.")
                
        print("\n=== Seeding Complete ===")
        print("Credentials (Password for all: password123):")
        for c in creators:
            print(f"- Creator: {c['username']}")
        for u in users:
            print(f"- User: {u['username']}")

if __name__ == "__main__":
    seed_data()
