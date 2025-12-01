from flask import Blueprint, request, jsonify
from .services import register_user, authenticate_user

main = Blueprint('main', __name__)

@main.route('/signup', methods=['POST', 'OPTIONS'])
def signup():
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

@main.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    data = request.json
    try:
        user = authenticate_user(data.get('username'), data.get('password'))
        return jsonify({'success': True, 'msg': 'Login successful', 'user_id': user.id}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 401
    except Exception as e:
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

from .services import create_chatbot, get_chatbot, get_chatbot_tree, list_chatbots, delete_chatbot, ask_chatbot

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
        # Assuming user_id is passed in body for now (until JWT auth is fully implemented)
        # In a real app, we'd get this from the token
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
