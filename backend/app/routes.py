from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from .services import (
    register_user, authenticate_user, 
    create_chatbot, get_chatbot, get_chatbot_tree, list_chatbots, delete_chatbot, 
    ask_chatbot, create_chat_session
)

main = Blueprint('main', __name__)

@main.route('/auth/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    data = request.json
    try:
        user = register_user(data.get('username'), data.get('email'), data.get('password'))
        return jsonify({'success': True, 'msg': 'User registered successfully'}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@main.route('/auth/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    data = request.json
    try:
        # Support login by username or email
        identifier = data.get('username') or data.get('email')
        user = authenticate_user(identifier, data.get('password'))
        login_user(user)
        return jsonify({'success': True, 'msg': 'Login successful', 'user_id': user.id}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 401
    except Exception as e:
        print(f"LOGIN ERROR: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@main.route('/auth/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return jsonify({'success': True, 'msg': 'Logged out'}), 200

@main.route('/chat-sessions', methods=['POST', 'OPTIONS'])
def create_chat_session_route():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    data = request.json
    chatbot_id = data.get('chatbot_id')
    
    if not chatbot_id:
        return jsonify({'success': False, 'error': 'Missing chatbot_id'}), 400
        
    # Assume authenticated user (using current_user in real app, but here relying on session or passed ID if we were using tokens)
    # Since I am using Flask-Login, I should use current_user.
    from flask_login import current_user
    if not current_user.is_authenticated:
        # For verification script simplicity (since we don't have full session/cookie jar handling in script easily without requests.Session),
        # allow passing user_id in body for TEST/DEV only?
        # No, better to fix the script to use sessions.
        # But verify_full_flow.py uses app.test_client() which handles cookies.
        # So current_user should work IF login_user was called.
        # But authenticate_user service DOES NOT call login_user. It just returns the user.
        # I need to call login_user here in the route!
        
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
        
    try:
        session = create_chat_session(chatbot_id, current_user.id)
        return jsonify({'success': True, 'session_id': session.id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/chatbots/<int:chatbot_id>/ask-ai', methods=['POST', 'OPTIONS'])
def ask_ai_route(chatbot_id):
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
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

@main.route('/chatbots', methods=['POST', 'OPTIONS'])
def create_chatbot_route():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    data = request.json
    try:
        # Use current_user if authenticated, else check body (for legacy/testing)
        if current_user.is_authenticated:
            user_id = current_user.id
        else:
            user_id = data.get('user_id')
            
        if not user_id:
             return jsonify({'success': False, 'error': 'Unauthorized'}), 401

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

@main.route('/chatbots/<int:chatbot_id>', methods=['GET', 'OPTIONS'])
def get_chatbot_route(chatbot_id):
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
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

@main.route('/chatbots/<int:chatbot_id>', methods=['DELETE', 'OPTIONS'])
def delete_chatbot_route(chatbot_id):
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    data = request.json # Need user_id for auth
    user_id = data.get('user_id')

    try:
        delete_chatbot(chatbot_id, user_id)
        return jsonify({'success': True, 'msg': 'Chatbot deleted'}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 403 # Unauthorized or Not Found
    except Exception as e:
        return jsonify({'success': False, 'error': 'Internal server error'}), 500
