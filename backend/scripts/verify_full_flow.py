import sys
import os
import json

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db, socketio
from app.models import User, Chatbot, ChatSession, Message

def run_verification():
    print("=== Starting End-to-End Verification ===")
    
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    }
    app = create_app(test_config)
    
    with app.app_context():
        db.create_all()
        client = app.test_client()
        
        try:
            # 1. Register Creator
            print("\n[1] Registering Creator...")
            res = client.post('/auth/register', json={
                'username': 'creator_bob',
                'email': 'bob@example.com',
                'password': 'password123',
                'role': 'creator'
            })
            if res.status_code != 201:
                print(f"FAILED: Status {res.status_code}, Body: {res.data}")
            assert res.status_code == 201
            print("    -> Creator registered.")
            
            # Login Creator
            res = client.post('/auth/login', json={
                'email': 'bob@example.com',
                'password': 'password123'
            })
            if res.status_code != 200:
                print(f"FAILED: Status {res.status_code}, Body: {res.data}")
            assert res.status_code == 200
            creator_id = res.json['user_id']
            print(f"    -> Creator Logged in. ID: {creator_id}")
            
            # 2. Create Chatbot
            print("\n[2] Creating Chatbot...")
            tree_data = {
                "label": "Tech Support",
                "content": "Welcome to Tech Support",
                "children": [
                    {
                        "label": "Hardware",
                        "content": "Hardware issues",
                        "children": []
                    },
                    {
                        "label": "Software",
                        "content": "Software issues",
                        "children": []
                    }
                ]
            }
            res = client.post('/chatbots', json={
                'title': 'Bob Tech Support',
                'description': 'Help with tech',
                'visibility': 'public',
                'tree_json': tree_data
            })
            assert res.status_code == 201
            chatbot_id = res.json['id']
            print(f"    -> Chatbot created. ID: {chatbot_id}")
            
            # Logout Creator
            client.get('/auth/logout') 
            
            # 3. Register User
            print("\n[3] Registering User...")
            res = client.post('/auth/register', json={
                'username': 'user_alice',
                'email': 'alice@example.com',
                'password': 'password123',
                'role': 'user'
            })
            assert res.status_code == 201
            
            res = client.post('/auth/login', json={
                'email': 'alice@example.com',
                'password': 'password123'
            })
            assert res.status_code == 200
            user_id = res.json['user_id']
            print(f"    -> User Logged in. ID: {user_id}")
            
            # 4. Search Chatbot
            print("\n[4] Searching Chatbot...")
            res = client.get('/chatbots?search=Bob')
            assert res.status_code == 200
            assert len(res.json['chatbots']) > 0
            assert res.json['chatbots'][0]['id'] == chatbot_id
            print("    -> Chatbot found.")
            
            # 5. Ask AI
            print("\n[5] Asking AI...")
            # Need to find a node ID first
            res = client.get(f'/chatbots/{chatbot_id}')
            root_node_id = res.json['tree']['id']
            
            res = client.post(f'/chatbots/{chatbot_id}/ask-ai', json={
                'current_node_id': root_node_id,
                'query': 'What do you support?'
            })
            assert res.status_code == 200
            print(f"    -> AI Response: {res.json['response']}")
            
            # 6. Starting Real-time Chat
            print("\n[6] Starting Real-time Chat...")
            # Create session (User is currently logged in)
            res = client.post('/chat-sessions', json={'chatbot_id': chatbot_id})
            assert res.status_code == 201
            session_id = res.json['session_id']
            print(f"    -> Session created via API. ID: {session_id}")
            
            # 7. Socket.IO Interaction (Two-Party Verification)
            print("\n[7] Socket.IO Interaction (Two-Party)...")
            
            # We need two separate clients to simulate two users
            # client (User) is already logged in as User (ID 2)
            user_http = client
            
            # Create a new client for Creator (ID 1)
            creator_http = app.test_client()
            # Login Creator
            res = creator_http.post('/auth/login', json={
                'email': 'bob@example.com', # Login creator_bob, not alice
                'password': 'password123'
            })
            assert res.status_code == 200
            print("    -> Creator (re)logged in for chat.")

            # Connect both to Socket.IO
            # Note: socketio.test_client(app, flask_test_client=...) uses the cookies from the http client
            user_socket = socketio.test_client(app, flask_test_client=user_http)
            creator_socket = socketio.test_client(app, flask_test_client=creator_http)
            
            # Both join the room
            user_socket.emit('join', {'session_id': session_id, 'user_id': user_id})
            creator_socket.emit('join', {'session_id': session_id, 'user_id': creator_id})
            
            # Verify Join
            received_u = user_socket.get_received()
            received_c = creator_socket.get_received()
            # Expect 'status' events
            assert any(e['name'] == 'status' for e in received_u)
            assert any(e['name'] == 'status' for e in received_c)
            print("    -> Both users joined the room.")
            
            # User sends message
            user_socket.emit('message', {'session_id': session_id, 'user_id': user_id, 'content': 'Hello Creator!'})
            print("    -> User sent message: 'Hello Creator!'")
            
            # Verify Creator received it
            received_c = creator_socket.get_received()
            message_event = next((e for e in received_c if e['name'] == 'message'), None)
            print(f"DEBUG: Message Event: {message_event}")
            assert message_event is not None
            # Handle potential dict vs list inconsistency in test client
            args = message_event['args']
            if isinstance(args, list):
                payload = args[0]
            else:
                payload = args
            
            assert payload['content'] == 'Hello Creator!'
            assert payload['user_id'] == user_id
            print("    -> Creator RECEIVED message! (Verification Successful)")
            
            # Verify User also received it (echo/broadcast)
            received_u = user_socket.get_received()
            message_event_u = next((e for e in received_u if e['name'] == 'message'), None)
            assert message_event_u is not None
            # Handle potential dict vs list inconsistency in test client
            args_u = message_event_u['args']
            if isinstance(args_u, list):
                payload_u = args_u[0]
            else:
                payload_u = args_u
            
            assert payload_u['content'] == 'Hello Creator!'
            print("    -> User received echo.")

            user_socket.disconnect()
            creator_socket.disconnect()

        except AssertionError as e:
            print(f"ASSERTION FAILED: {e}")
            # Print last response if available
            if 'res' in locals() and hasattr(res, 'status_code'):
                 print(f"Last Response Status: {res.status_code}")
                 if res.content_type == 'application/json':
                     print(f"Last Response Body: {res.json}")
                 else:
                     print(f"Last Response Body: {res.data}")
            raise e
        except Exception as e:
            print(f"ERROR: {e}")
            raise e
        
    print("\n=== Verification Complete ===")

if __name__ == '__main__':
    run_verification()
