import pytest
from app import create_app, db
from app.models import User, Chatbot, ChatSession
from app.services import create_chat_session, resolve_chat_session, get_creator_sessions, validate_session_access

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_resolve_chat_session(app):
    with app.app_context():
        # Setup
        creator = User(username='creator', email='c@test.com', password_hash='hash', role='creator')
        user = User(username='user', email='u@test.com', password_hash='hash', role='user')
        db.session.add_all([creator, user])
        db.session.commit()
        
        bot = Chatbot(creator_id=creator.id, title='Bot', visibility='public')
        db.session.add(bot)
        db.session.commit()
        
        session = create_chat_session(bot.id, user.id)
        
        # Verify initial state
        assert session.status == 'active'
        assert len(get_creator_sessions(creator.id)) == 1
        
        # Resolve session
        resolved_session = resolve_chat_session(session.id, creator.id)
        assert resolved_session.status == 'resolved'
        
        # Verify filtered out
        assert len(get_creator_sessions(creator.id)) == 0

def test_resolve_chat_session_unauthorized(app):
    with app.app_context():
        # Setup
        creator = User(username='creator', email='c@test.com', password_hash='hash', role='creator')
        other = User(username='other', email='o@test.com', password_hash='hash', role='user')
        db.session.add_all([creator, other])
        db.session.commit()
        
        bot = Chatbot(creator_id=creator.id, title='Bot', visibility='public')
        db.session.add(bot)
        db.session.commit()
        
        session = create_chat_session(bot.id, None) # Guest session
        
        # Try to resolve as unrelated user
        with pytest.raises(ValueError, match="Unauthorized"):
            resolve_chat_session(session.id, other.id)
