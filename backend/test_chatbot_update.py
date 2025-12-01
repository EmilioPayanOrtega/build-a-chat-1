import pytest
from app import create_app, db
from app.models import User, Chatbot, Node
from app.services import create_chatbot, update_chatbot

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def creator(app):
    user = User(username="creator", email="creator@test.com", password_hash="hash", role="creator")
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def other_user(app):
    user = User(username="other", email="other@test.com", password_hash="hash", role="creator")
    db.session.add(user)
    db.session.commit()
    return user

def test_update_chatbot_metadata(app, creator):
    chatbot = create_chatbot(creator.id, "Original Title", "Desc", "public", None)
    
    updated_chatbot = update_chatbot(chatbot.id, creator.id, "New Title", "New Desc", "private", None)
    
    assert updated_chatbot.title == "New Title"
    assert updated_chatbot.description == "New Desc"
    assert updated_chatbot.visibility == "private"

def test_update_chatbot_tree(app, creator):
    tree_json = {
        "label": "Root",
        "children": [
            {"label": "Child 1", "children": []}
        ]
    }
    chatbot = create_chatbot(creator.id, "Title", "Desc", "public", tree_json)
    
    # Verify initial tree
    assert Node.query.filter_by(chatbot_id=chatbot.id).count() == 2
    
    new_tree_json = {
        "label": "New Root",
        "children": [
            {"label": "New Child 1", "children": []},
            {"label": "New Child 2", "children": []}
        ]
    }
    
    update_chatbot(chatbot.id, creator.id, "Title", "Desc", "public", new_tree_json)
    
    # Verify updated tree
    nodes = Node.query.filter_by(chatbot_id=chatbot.id).all()
    assert len(nodes) == 3
    root = Node.query.filter_by(chatbot_id=chatbot.id, parent_node_id=None).first()
    assert root.label == "New Root"
    children = Node.query.filter_by(chatbot_id=chatbot.id, parent_node_id=root.id).all()
    assert len(children) == 2

def test_update_chatbot_permissions(app, creator, other_user):
    chatbot = create_chatbot(creator.id, "Title", "Desc", "public", None)
    
    with pytest.raises(ValueError, match="No autorizado"):
        update_chatbot(chatbot.id, other_user.id, "New Title", "Desc", "public", None)
