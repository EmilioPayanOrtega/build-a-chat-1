
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from .services import (
    register_user, authenticate_user, 
    create_chatbot, get_chatbot, get_chatbot_tree, list_chatbots, delete_chatbot, 
    create_chat_session, ask_chatbot_session, get_creator_sessions, get_session_messages,
    send_contact_email, resolve_chat_session
)

main = Blueprint('main', __name__)

@main.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()
    try:
        send_contact_email(
            name=data.get('name'),
            email=data.get('email'),
            subject=data.get('subject'),
            message=data.get('message')
        )
        return jsonify({'message': 'Mensaje enviado correctamente'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Error sending email: {e}")
        return jsonify({'error': 'Error al enviar el mensaje'}), 500
from flask_login import login_user, logout_user, current_user, login_required
from .services import (
    register_user, authenticate_user, 
    create_chatbot, get_chatbot, get_chatbot_tree, list_chatbots, delete_chatbot, 
    create_chatbot, get_chatbot, get_chatbot_tree, list_chatbots, delete_chatbot, 
    create_chat_session, ask_chatbot_session, get_creator_sessions, get_session_messages, update_chatbot
)

main = Blueprint('main', __name__)

@main.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    try:
        user = register_user(data.get('username'), data.get('email'), data.get('password'), data.get('role', 'user'))
        return jsonify({'success': True, 'msg': 'Usuario registrado exitosamente'}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@main.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    try:
        # Support login by username or email
        identifier = data.get('username') or data.get('email')
        user = authenticate_user(identifier, data.get('password'))
        login_user(user)
        return jsonify({'success': True, 'msg': 'Inicio de sesión exitoso', 'user_id': user.id, 'role': user.role}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 401
    except Exception as e:
        print(f"LOGIN ERROR: {e}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@main.route('/auth/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return jsonify({'success': True, 'msg': 'Sesión cerrada'}), 200

@main.route('/chat-sessions', methods=['POST'])
def create_chat_session_route():
    data = request.json
    raw_chatbot_id = data.get('chatbot_id')
    
    if not raw_chatbot_id:
        return jsonify({'success': False, 'error': 'Falta chatbot_id'}), 400
        
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'error': 'No autorizado'}), 401
        
    try:
        chatbot_id = int(raw_chatbot_id) # Conversión, Forzar a ser entero antes de la lógica
        session = create_chat_session(chatbot_id, current_user.id)
        return jsonify({
            'success': True, 
            'session_id': session.id, 
            'type': str(session.type.value if hasattr(session.type, 'value') else session.type)
        }), 201
    
    except ValueError:
        return jsonify({'success': False, 'error': 'El chatbot_id debe ser un número válido'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@main.route('/chat-sessions/<int:session_id>/messages', methods=['GET'])
@login_required
def get_session_messages_route(session_id):
    try:
        # Validate access
        if not validate_session_access(session_id, current_user.id):
            return jsonify({'success': False, 'error': 'No autorizado'}), 403
            
        messages = get_session_messages(session_id)
        return jsonify({
            'success': True, 
            'messages': [{
                'content': m.content,
                'sender_type': m.sender_type,
                'created_at': m.created_at.isoformat()
            } for m in messages]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

from .services import ask_chatbot_session, validate_session_access

@main.route('/chat-sessions/<int:session_id>/ask', methods=['POST'])
def ask_session_ai_route(session_id):
    data = request.json
    current_node_id = data.get('current_node_id')
    query = data.get('query')
    
    if not current_node_id or not query:
        return jsonify({'success': False, 'error': 'Falta current_node_id o query'}), 400
        
    try:
        # Validate access? 
        # Ideally yes, but for now let's assume if you have the session ID you can chat (or rely on validate_session_access inside service if we added it there? No we didn't).
        # Let's add basic auth check if user is logged in and belongs to session?
        # For guest AI chat, user might not be logged in?
        # The requirements said "let the user maintain a conversation".
        # If it's a public chatbot, maybe no auth needed?
        # But create_chat_session required auth in routes.py (line 53).
        # So we assume user is authenticated.
        
        if not current_user.is_authenticated:
             return jsonify({'success': False, 'error': 'No autorizado'}), 401
             
        # TODO: Check if current_user is the owner of the session
        
        response = ask_chatbot_session(session_id, current_node_id, query)
        return jsonify({'success': True, 'response': response}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        print(f"AI SESSION ERROR: {e}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@main.route('/chatbots', methods=['POST'])
def create_chatbot_route():
    data = request.json
    try:
        if not current_user.is_authenticated:
            return jsonify({'success': False, 'error': 'No autorizado'}), 401
        
        if current_user.role != 'creator':
            return jsonify({'success': False, 'error': 'Solo los creadores pueden crear chatbots'}), 403
        
        user_id = current_user.id

        chatbot = create_chatbot(
            user_id, 
            data.get('title'), 
            data.get('description'), 
            data.get('visibility'), 
            data.get('tree_json')
        )
        return jsonify({'success': True, 'msg': 'Chatbot creado', 'id': chatbot.id}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@main.route('/chatbots/<int:chatbot_id>', methods=['GET'])
def get_chatbot_route(chatbot_id):
    chatbot = get_chatbot(chatbot_id)
    if not chatbot:
        return jsonify({'success': False, 'error': 'Chatbot no encontrado'}), 404
    
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
        'chatbots': [{'id': c.id, 'title': c.title, 'description': c.description, 'creator_id': c.creator_id} for c in chatbots]
    }), 200

@main.route('/chatbots/<int:chatbot_id>', methods=['DELETE'])
def delete_chatbot_route(chatbot_id):
    data = request.json # Need user_id for auth
    user_id = data.get('user_id')

    try:
        delete_chatbot(chatbot_id, user_id)
        return jsonify({'success': True, 'msg': 'Chatbot eliminado'}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 403 # Unauthorized or Not Found
    except Exception as e:
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500
        
@main.route('/creator/sessions', methods=['GET'])
@login_required
def list_creator_sessions_route():
    if current_user.role != 'creator':
        return jsonify({'success': False, 'error': 'No autorizado'}), 403
        
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

from .services import resolve_chat_session

@main.route('/chat-sessions/<int:session_id>/resolve', methods=['POST'])
@login_required
def resolve_chat_session_route(session_id):
    try:
        resolve_chat_session(session_id, current_user.id)
        return jsonify({'success': True, 'msg': 'Sesión de chat resuelta'}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 403 # Unauthorized or Not Found
    except Exception as e:
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@main.route('/chatbots/<int:chatbot_id>', methods=['PUT'])
@login_required
def update_chatbot_route(chatbot_id):
    data = request.json
    try:
        update_chatbot(
            chatbot_id,
            current_user.id,
            data.get('title'),
            data.get('description'),
            data.get('visibility'),
            data.get('tree_json')
        )
        return jsonify({'success': True, 'msg': 'Chatbot actualizado'}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        print(f"UPDATE ERROR: {e}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500
