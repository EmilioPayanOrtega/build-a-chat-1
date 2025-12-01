import pytest
from app.services import create_chatbot, ask_chatbot, register_user
from app.models import Node

def test_ask_chatbot_success(app):
    with app.app_context():
        user = register_user("creator_ai", "ai@example.com", "pass")
        tree_json = {
            "label": "Root Topic",
            "content": "Root details",
            "children": [
                {"label": "Subtopic A", "content": "Details A", "children": []}
            ]
        }
        chatbot = create_chatbot(user.id, "AI Bot", "Desc", "public", tree_json)
        
        # Get root node id
        root_node = Node.query.filter_by(chatbot_id=chatbot.id, label="Root Topic").first()
        
        response = ask_chatbot(chatbot.id, root_node.id, "Tell me about this")
        
        assert "[MOCK AI RESPONSE]" in response
        assert "Root Topic" in response
        assert "Subtopic A" in response # Should include children in context

def test_ask_chatbot_invalid_node(app):
    with app.app_context():
        user = register_user("creator_ai2", "ai2@example.com", "pass")
        chatbot = create_chatbot(user.id, "AI Bot 2", "Desc", "public", {"label": "Root", "children": []})
        
        with pytest.raises(ValueError, match="Node not found"):
            ask_chatbot(chatbot.id, 9999, "Query")
