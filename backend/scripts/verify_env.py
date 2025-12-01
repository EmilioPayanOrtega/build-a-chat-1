import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
app = create_app()

def verify_env():
    print(f"DB_USER from env: {os.getenv('DB_USER')}")
    print(f"DB_NAME from env: {os.getenv('DB_NAME')}")
    
    with app.app_context():
        try:
            db.engine.connect()
            print("Database connection successful.")
        except Exception as e:
            print(f"Database connection failed: {e}")

if __name__ == "__main__":
    verify_env()
