import sys
import os
import requests
import json

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User, Chatbot, Node

def run_test():
    print("=== Testing Stateful AI Chat (Test Client) ===")
    
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    with app.app_context():
        db.create_all()
        client = app.test_client()
        
        # 1. Setup Data (Register User & Creator, Create Chatbot)
        print("\n[1] Setting up data...")
        # Creator
        client.post('/api/auth/register', json={'username': 'creator', 'email': 'creator@example.com', 'password': 'pass', 'role': 'creator'})
        client.post('/api/auth/login', json={'email': 'creator@example.com', 'password': 'pass'})
        
        # Chatbot
        tree = {"label": "Root", "content": "Root Content", "children": []}
        res = client.post('/api/chatbots', json={'title': 'AI Bot', 'description': 'Desc', 'visibility': 'public', 'tree_json': tree})
        chatbot_id = res.json['id']
        
        # Logout Creator
        client.get('/api/auth/logout')
        
        # User
        client.post('/api/auth/register', json={'username': 'user', 'email': 'user@example.com', 'password': 'pass'})
        client.post('/api/auth/login', json={'email': 'user@example.com', 'password': 'pass'})
        print("    -> Data setup complete.")
        
        # 2. Create Session
        print("\n[2] Creating Chat Session...")
        res = client.post('/api/chat-sessions', json={"chatbot_id": chatbot_id})
        assert res.status_code == 201
        session_id = res.json['session_id']
        print(f"    -> Session Created: {session_id}")
        
        # 3. Get Root Node
        res = client.get(f'/api/chatbots/{chatbot_id}')
        root_node_id = res.json['tree']['id']
        
        # 4. Ask AI (First Query)
        print("\n[4] Asking AI (Q1: What is this bot about?)...")
        res = client.post(f'/api/chat-sessions/{session_id}/ask', json={
            "current_node_id": root_node_id,
            "query": "What is this bot about?"
        })
        print(f"    -> Status: {res.status_code}")
        if res.status_code == 200:
            print(f"    -> Response: {res.json.get('response')}")
        else:
            print(f"    -> Error: {res.json}")
            
        # 5. Ask AI (Follow-up)
        print("\n[5] Asking AI (Q2: Can you elaborate?)...")
        res = client.post(f'/api/chat-sessions/{session_id}/ask', json={
            "current_node_id": root_node_id,
            "query": "Can you elaborate?"
        })
        print(f"    -> Status: {res.status_code}")
        if res.status_code == 200:
            print(f"    -> Response: {res.json.get('response')}")
        else:
            print(f"    -> Error: {res.json}")

    print("\n=== Test Complete ===")

if __name__ == "__main__":
    run_test()
