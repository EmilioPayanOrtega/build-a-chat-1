from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from .services import (
    register_user, authenticate_user, 
    create_chatbot, get_chatbot, get_chatbot_tree, list_chatbots, delete_chatbot, 
    ask_chatbot, create_chat_session
)

main = Blueprint('main', __name__)

@main.route('/auth/register', methods=['POST'])
def register():
    
    data = request.json
    try:
        user = register_user(data.get('username'), data.get('email'), data.get('password'), data.get('role', 'user'))
        return jsonify({'success': True, 'msg': 'User registered successfully'}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@main.route('/auth/login', methods=['POST'])
def login():
    
    data = request.json
    try:
        # Support login by username or email
        identifier = data.get('username') or data.get('email')
        user = authenticate_user(identifier, data.get('password'))
        login_user(user)
        return jsonify({'success': True, 'msg': 'Login successful', 'user_id': user.id, 'role': user.role}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 401
    except Exception as e:
        print(f"LOGIN ERROR: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@main.route('/auth/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return jsonify({'success': True, 'msg': 'Logged out'}), 200

@main.route('/chat-sessions', methods=['POST'])
def create_chat_session_route():
        
    data = request.json
    chatbot_id = data.get('chatbot_id')
    
    if not chatbot_id:
        return jsonify({'success': False, 'error': 'Missing chatbot_id'}), 400
        
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
        
    try:
        session = create_chat_session(chatbot_id, current_user.id)
        return jsonify({'success': True, 'session_id': session.id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/chatbots/<int:chatbot_id>/ask-ai', methods=['POST'])
def ask_ai_route(chatbot_id):
    
    data = request.json
    current_node_id = data.get('current_node_id')
    query = data.get('query')
    
    if not current_node_id or not query:
        return jsonify({'success': False, 'error': 'Missing current_node_id or query'}), 400
        
    try:
        response = ask_chatbot(chatbot_id, current_node_id, query)
        return jsonify({'success': True, 'response': response}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@main.route('/chatbots', methods=['POST'])
def create_chatbot_route():
    
    data = request.json
    try:
        if not current_user.is_authenticated:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 401
        
        if current_user.role != 'creator':
            return jsonify({'success': False, 'error': 'Only creators can create chatbots'}), 403
        
        user_id = current_user.id

        chatbot = create_chatbot(
            user_id, 
            data.get('title'), 
            data.get('description'), 
            data.get('visibility'), 
            data.get('tree_json')
        )
        return jsonify({'success': True, 'msg': 'Chatbot created', 'id': chatbot.id}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@main.route('/chatbots/<int:chatbot_id>', methods=['GET'])
def get_chatbot_route(chatbot_id):
    
    chatbot = get_chatbot(chatbot_id)
    if not chatbot:
        return jsonify({'success': False, 'error': 'Chatbot not found'}), 404
    
    tree = get_chatbot_tree(chatbot_id)
    
    return jsonify({
        'success': True,
        'chatbot': {
            'id': chatbot.id,
            'title': chatbot.title,
            'description': chatbot.description,
            'visibility': chatbot.visibility,
            'creator_id': chatbot.creator_id
        },
        'tree': tree
    }), 200

@main.route('/chatbots', methods=['GET'])
def list_chatbots_route():
    search = request.args.get('search')
    chatbots = list_chatbots(search)
    return jsonify({
        'success': True,
        'chatbots': [{'id': c.id, 'title': c.title, 'description': c.description} for c in chatbots]
    }), 200

@main.route('/chatbots/<int:chatbot_id>', methods=['DELETE'])
def delete_chatbot_route(chatbot_id):

    data = request.json # Need user_id for auth
    user_id = data.get('user_id')

    try:
        delete_chatbot(chatbot_id, user_id)
        return jsonify({'success': True, 'msg': 'Chatbot deleted'}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 403 # Unauthorized or Not Found
    except Exception as e:
        return jsonify({'success': False, 'error': 'Internal server error'}), 500
@main.route('/creator/sessions', methods=['GET'])
@login_required
def list_creator_sessions_route():
    if current_user.role != 'creator':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
    sessions = get_creator_sessions(current_user.id)
    
    return jsonify({
        'success': True,
        'sessions': [{
            'id': s.id,
            'chatbot_title': s.chatbot.title,
            'user_id': s.user_id, # Could fetch username if needed
            'created_at': s.created_at.isoformat()
        } for s in sessions]
    }), 200
