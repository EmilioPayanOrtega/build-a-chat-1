import pytest
import unittest.mock
import os
from app.services import create_chatbot, create_chat_session, ask_chatbot_session, register_user
from app.models import Node, Message

def test_ask_chatbot_session_success(app):
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
        
        # Create session
        session = create_chat_session(chatbot.id, user.id, 'ai_conversation')
        
        # Get root node id
        root_node = Node.query.filter_by(chatbot_id=chatbot.id, label="Root Topic").first()
        
        # Mock the Gemini API
        with unittest.mock.patch('app.utils.ai_client.genai') as mock_genai:
            mock_model = unittest.mock.Mock()
            mock_response = unittest.mock.Mock()
            mock_response.text = "Mocked Gemini Response"
            mock_model.generate_content.return_value = mock_response
            mock_genai.GenerativeModel.return_value = mock_model
            
            with unittest.mock.patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'}):
                response = ask_chatbot_session(session.id, root_node.id, "Tell me about this")
                
                assert "Mocked Gemini Response" in response
                
                # Verify Messages Saved
                msgs = Message.query.filter_by(chat_session_id=session.id).all()
                assert len(msgs) == 2
                assert msgs[0].content == "Tell me about this"
                assert msgs[0].sender_type == 'user'
                assert msgs[1].content == "Mocked Gemini Response"
                assert msgs[1].sender_type == 'ai'

def test_ask_chatbot_session_invalid_node(app):
    with app.app_context():
        user = register_user("creator_ai2", "ai2@example.com", "pass")
        chatbot = create_chatbot(user.id, "AI Bot 2", "Desc", "public", {"label": "Root", "children": []})
        session = create_chat_session(chatbot.id, user.id, 'ai_conversation')
        
        with pytest.raises(ValueError, match="Node not found"):
            ask_chatbot_session(session.id, 9999, "Query")
