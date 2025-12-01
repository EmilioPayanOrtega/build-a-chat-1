import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import db, User, Chatbot, Node, ChatSession, Message

app = create_app()

def verify_models():
    with app.app_context():
        # Create tables
        db.create_all()
        print("Tables created.")

        # Create a test user
        user = User.query.filter_by(username='testuser').first()
        if not user:
            user = User(username='testuser', email='test@example.com', password_hash='hashed_password')
            db.session.add(user)
            db.session.commit()
            print("Test user created.")
        else:
            print("Test user already exists.")

        # Create a chatbot
        chatbot = Chatbot(creator_id=user.id, title='Test Bot', description='A test bot', visibility='public')
        db.session.add(chatbot)
        db.session.commit()
        print("Test chatbot created.")

        # Create nodes
        root_node = Node(chatbot_id=chatbot.id, label='Root', content='Root content')
        db.session.add(root_node)
        db.session.commit()
        
        child_node = Node(chatbot_id=chatbot.id, label='Child', content='Child content', parent_node_id=root_node.id)
        db.session.add(child_node)
        db.session.commit()
        print("Test nodes created.")

        # Verify relationships
        fetched_chatbot = Chatbot.query.get(chatbot.id)
        print(f"Chatbot '{fetched_chatbot.title}' has {len(fetched_chatbot.nodes)} nodes.")
        
        fetched_root = Node.query.get(root_node.id)
        print(f"Root node '{fetched_root.label}' has {len(fetched_root.children)} children.")

        # Create chat session and message
        session = ChatSession(chatbot_id=chatbot.id, user_id=user.id, type='ai_conversation')
        db.session.add(session)
        db.session.commit()
        
        message = Message(chat_session_id=session.id, sender_id=user.id, sender_type='user', content='Hello')
        db.session.add(message)
        db.session.commit()
        print("Chat session and message created.")

        # Verify message
        fetched_session = ChatSession.query.get(session.id)
        print(f"Session has {len(fetched_session.messages)} messages.")

        print("Verification complete.")

if __name__ == "__main__":
    verify_models()
