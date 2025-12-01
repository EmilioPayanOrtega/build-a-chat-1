import pytest
from app import socketio
from app.services import register_user, create_chatbot, create_chat_session
from app.models import Message

def test_join_room_authorized(app):
    print(f"DEBUG: Test socketio id: {id(socketio)}")
    with app.app_context():
        # Setup
        creator = register_user("creator_sock", "sock@example.com", "pass")
        user = register_user("user_sock", "user_sock@example.com", "pass")
        chatbot = create_chatbot(creator.id, "Sock Bot", "Desc", "public", {"label": "Root", "children": []})
        session = create_chat_session(chatbot.id, user.id)
        
        # Create client inside context
        client = socketio.test_client(app, flask_test_client=app.test_client())
        if not client.is_connected():
            client.connect()
        
        try:
            # Join first
            client.emit('join', {'session_id': session.id, 'user_id': user.id})
            received = client.get_received()
            
            # Check for status message in room
            assert len(received) > 0
            assert received[0]['name'] == 'status'
            assert 'entered the room' in received[0]['args'][0]['msg']
        finally:
            client.disconnect()

def test_join_room_unauthorized(app):
    with app.app_context():
        # Setup
        creator = register_user("creator_sock2", "sock2@example.com", "pass")
        user = register_user("user_sock2", "user_sock2@example.com", "pass")
        intruder = register_user("intruder", "intruder@example.com", "pass")
        chatbot = create_chatbot(creator.id, "Sock Bot 2", "Desc", "public", {"label": "Root", "children": []})
        session = create_chat_session(chatbot.id, user.id)
        
        client = socketio.test_client(app, flask_test_client=app.test_client())
        if not client.is_connected():
            client.connect()
        
        try:
            # Intruder tries to join
            client.emit('join', {'session_id': session.id, 'user_id': intruder.id})
            received = client.get_received()
            
            # Check for error
            assert len(received) > 0
            assert received[0]['name'] == 'error'
            assert 'Unauthorized' in received[0]['args'][0]['msg']
        finally:
            client.disconnect()

def test_send_message_persistence(app):
    with app.app_context():
        # Setup
        creator = register_user("creator_sock3", "sock3@example.com", "pass")
        user = register_user("user_sock3", "user_sock3@example.com", "pass")
        chatbot = create_chatbot(creator.id, "Sock Bot 3", "Desc", "public", {"label": "Root", "children": []})
        session = create_chat_session(chatbot.id, user.id)
        
        client = socketio.test_client(app, flask_test_client=app.test_client())
        if not client.is_connected():
            client.connect()
        
        try:
            # Join first
            client.emit('join', {'session_id': session.id, 'user_id': user.id})
            
            # Send message
            client.emit('message', {
                'session_id': session.id,
                'user_id': user.id,
                'content': 'Hello World'
            })
            
            # Check DB persistence
            msg = Message.query.filter_by(chat_session_id=session.id).first()
            assert msg is not None
            assert msg.content == 'Hello World'
            
            # Check broadcast
            received = client.get_received()
            # Filter for message event
            message_events = [e for e in received if e['name'] == 'message']
            assert len(message_events) > 0
            
            args = message_events[0]['args']
            if isinstance(args, list):
                content = args[0]['content']
            else:
                content = args['content']
                
            assert content == 'Hello World'
        finally:
            client.disconnect()
