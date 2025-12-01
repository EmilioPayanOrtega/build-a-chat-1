import pytest
from app.services import create_chatbot, get_chatbot, get_chatbot_tree, list_chatbots, delete_chatbot, register_user
from app.models import Chatbot, Node

def test_create_chatbot_success(app):
    with app.app_context():
        user = register_user("creator", "creator@example.com", "pass")
        tree_json = {
            "label": "Root",
            "children": [
                {"label": "Child 1", "children": []}
            ]
        }
        
        chatbot = create_chatbot(user.id, "My Bot", "Desc", "public", tree_json)
        
        assert chatbot.id is not None
        assert chatbot.title == "My Bot"
        
        # Verify nodes
        nodes = Node.query.filter_by(chatbot_id=chatbot.id).all()
        assert len(nodes) == 2
        root = next(n for n in nodes if n.label == "Root")
        child = next(n for n in nodes if n.label == "Child 1")
        assert child.parent_node_id == root.id

def test_create_chatbot_invalid_tree(app):
    with app.app_context():
        user = register_user("creator2", "creator2@example.com", "pass")
        tree_json = {"invalid": "structure"}
        
        with pytest.raises(ValueError, match="Invalid tree format"):
            create_chatbot(user.id, "Bot", "Desc", "public", tree_json)

def test_get_chatbot_tree(app):
    with app.app_context():
        user = register_user("creator3", "creator3@example.com", "pass")
        tree_json = {
            "label": "Root",
            "children": [
                {"label": "Child 1", "children": []}
            ]
        }
        chatbot = create_chatbot(user.id, "Bot", "Desc", "public", tree_json)
        
        tree_root = get_chatbot_tree(chatbot.id)
        assert tree_root['label'] == "Root"
        assert len(tree_root['children']) == 1
        assert tree_root['children'][0]['label'] == "Child 1"

def test_list_chatbots(app):
    with app.app_context():
        user = register_user("creator4", "creator4@example.com", "pass")
        tree_json = {"label": "Root", "children": []}
        create_chatbot(user.id, "Public Bot", "Desc", "public", tree_json)
        create_chatbot(user.id, "Private Bot", "Desc", "private", tree_json)
        
        public_bots = list_chatbots()
        assert len(public_bots) == 1
        assert public_bots[0].title == "Public Bot"

def test_delete_chatbot(app):
    with app.app_context():
        user = register_user("creator5", "creator5@example.com", "pass")
        tree_json = {"label": "Root", "children": []}
        chatbot = create_chatbot(user.id, "To Delete", "Desc", "public", tree_json)
        
        delete_chatbot(chatbot.id, user.id)
        
        assert get_chatbot(chatbot.id) is None
        assert len(Node.query.filter_by(chatbot_id=chatbot.id).all()) == 0
