from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User

def register_user(username, email, password, role='user'):
    if not (username and email and password):
        raise ValueError('Datos faltantes')
    
    if User.query.filter((User.username == username) | (User.email == email)).first():
        raise ValueError('El usuario o correo ya existe')

    try:
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password_hash=password_hash, role=role)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except Exception as e:
        db.session.rollback()
        raise e

def authenticate_user(identifier, password):
    if not (identifier and password):
        raise ValueError('Datos incompletos')
    
    # Check if identifier is email or username
    user = User.query.filter((User.username == identifier) | (User.email == identifier)).first()
    
    if not user or not check_password_hash(user.password_hash, password):
        raise ValueError('Usuario/correo o contraseña inválidos')

    return user

from .models import Chatbot, Node
from .utils.tree_parser import validate_tree, nodes_to_json
from .utils.ai_client import generate_response

def create_chatbot(user_id, title, description, visibility, tree_json):
    if not (title and visibility):
        raise ValueError('Faltan campos requeridos')
    
    # Validate tree
    if tree_json:
        if not validate_tree(tree_json):
             raise ValueError("Formato de árbol inválido")

    try:
        new_chatbot = Chatbot(
            creator_id=user_id,
            title=title,
            description=description,
            visibility=visibility
        )
        db.session.add(new_chatbot)
        db.session.flush() # Get ID

        if tree_json:
            _save_tree_nodes(new_chatbot.id, tree_json)

        db.session.commit()
        return new_chatbot
    except Exception as e:
        db.session.rollback()
        raise e

def _save_tree_nodes(chatbot_id, tree_data, parent_id=None):
    node = Node(
        chatbot_id=chatbot_id,
        label=tree_data['label'],
        parent_node_id=parent_id,
        content=tree_data.get('content', '') # Save content if present
    )
    db.session.add(node)
    db.session.flush()

    for child in tree_data.get('children', []):
        _save_tree_nodes(chatbot_id, child, node.id)

def get_chatbot(chatbot_id):
    return db.session.get(Chatbot, chatbot_id)

def get_chatbot_tree(chatbot_id):
    nodes = Node.query.filter_by(chatbot_id=chatbot_id).all()
    return nodes_to_json(nodes)

def list_chatbots(search_query=None):
    query = Chatbot.query.filter_by(is_active=True, visibility='public')
    if search_query:
        query = query.filter(Chatbot.title.ilike(f'%{search_query}%'))
    return query.all()

def delete_chatbot(chatbot_id, user_id):
    chatbot = db.session.get(Chatbot, chatbot_id)
    if not chatbot:
        raise ValueError('Chatbot no encontrado')
    if chatbot.creator_id != user_id:
        raise ValueError('No autorizado')
    
    db.session.delete(chatbot)
    db.session.commit()

def update_chatbot(chatbot_id, user_id, title, description, visibility, tree_json=None):
    chatbot = db.session.get(Chatbot, chatbot_id)
    if not chatbot:
        raise ValueError('Chatbot no encontrado')
    
    if chatbot.creator_id != user_id:
        raise ValueError('No autorizado')

    if not (title and visibility):
        raise ValueError('Faltan campos requeridos')

    # Validate tree if provided
    if tree_json:
        if not validate_tree(tree_json):
             raise ValueError("Formato de árbol inválido")

    try:
        chatbot.title = title
        chatbot.description = description
        chatbot.visibility = visibility
        
        if tree_json:
            # Delete existing nodes
            # First, unlink all nodes to avoid foreign key constraints (self-referencing)
            Node.query.filter_by(chatbot_id=chatbot_id).update({Node.parent_node_id: None})
            db.session.flush()
            
            # Now delete them
            Node.query.filter_by(chatbot_id=chatbot_id).delete()
            db.session.flush()
            # Save new nodes
            _save_tree_nodes(chatbot.id, tree_json)

        db.session.commit()
        return chatbot
    except Exception as e:
        db.session.rollback()
        raise e

# --- Chat Session Services ---
from .models import ChatSession, Message
from datetime import datetime, timezone

def create_chat_session(chatbot_id, user_id, session_type='ai_conversation'):
    # Check for existing active session
    existing_session = ChatSession.query.filter_by(
        chatbot_id=chatbot_id, 
        user_id=user_id, 
        status='active'
    ).first()
    
    if existing_session:
        return existing_session

    session = ChatSession(
        chatbot_id=chatbot_id,
        user_id=user_id,
        type=session_type,
        status='active'
    )
    db.session.add(session)
    db.session.commit()
    return session

def get_chat_session(session_id):
    return db.session.get(ChatSession, session_id)

def get_creator_sessions(creator_id):
    return ChatSession.query.join(Chatbot).filter(Chatbot.creator_id == creator_id).all()

def validate_session_access(session_id, user_id):
    """
    Checks if the user is a participant (User or Creator) of the session.
    """
    session = get_chat_session(session_id)
    if not session:
        return False
    
    # Check if user is the session starter
    if session.user_id == user_id:
        return True
        
    # Check if user is the creator of the chatbot
    chatbot = get_chatbot(session.chatbot_id)
    if chatbot and chatbot.creator_id == user_id:
        return True
        
    return False

def save_message(session_id, sender_id, content):
    session = get_chat_session(session_id)
    if not session:
        raise ValueError("Sesión no encontrada")
        
    sender_type = 'user' if sender_id == session.user_id else 'creator'

    message = Message(
        chat_session_id=session_id,
        sender_id=sender_id,
        sender_type=sender_type,
        content=content,
        created_at=datetime.now(timezone.utc)
    )
    db.session.add(message)
    db.session.commit()
    return message

def switch_session_to_human(session_id):
    session = get_chat_session(session_id)
    if not session:
        raise ValueError("Sesión no encontrada")
    session.type = 'human_support'
    db.session.commit()
    return session

def ask_chatbot_session(session_id, current_node_id, query):
    from . import socketio
    from flask_socketio import emit
    """
    Stateful AI chat.
    1. Fetches session and validates.
    2. Fetches full tree and current node for context.
    3. Fetches conversation history.
    4. Constructs prompt.
    5. Calls AI.
    6. Saves AI response.
    """
    # 1. Fetch Session
    session = get_chat_session(session_id)
    if not session:
        raise ValueError("Sesión no encontrada")
    
    # User message is already saved via socket event before calling this API
    # save_message(session_id, session.user_id, query)
    
    # 3. Fetch Context (Tree + Node)
    chatbot = get_chatbot(session.chatbot_id)
    tree_json = get_chatbot_tree(session.chatbot_id)
    current_node = db.session.get(Node, current_node_id)
    
    if not current_node or current_node.chatbot_id != session.chatbot_id:
        raise ValueError("Nodo no encontrado o no pertenece a este chatbot")
        
    # 4. Fetch History (Last 10 messages)
    messages = Message.query.filter_by(chat_session_id=session_id).order_by(Message.created_at.desc()).limit(10).all()
    messages.reverse() # Oldest first
    
    # 5. Construct Prompt
    # System Instruction
    system_prompt = (
        f"Eres un asistente de soporte útil para el chatbot '{chatbot.title}'. "
        "Tu objetivo es responder a las preguntas de los usuarios basándote ESTRICTAMENTE en la Base de Conocimiento proporcionada. "
        "Si la respuesta no está en la Base de Conocimiento, di cortésmente que no lo sabes. "
        "RESPONDE SIEMPRE EN ESPAÑOL."
    )
    
    # Knowledge Base (Full Tree)
    import json
    kb_str = json.dumps(tree_json, indent=2)
    
    # Current Context
    node_context = f"El usuario está viendo el nodo: '{current_node.label}'"
    if current_node.content:
        node_context += f" - Contenido: {current_node.content}"
        
    # History
    history_str = ""
    for msg in messages:
        role = "Usuario" if msg.sender_type == 'user' else "IA"
        history_str += f"{role}: {msg.content}\n"
        
    # Final Prompt Construction
    full_prompt = (
        f"{system_prompt}\n\n"
        f"--- Base de Conocimiento ---\n{kb_str}\n\n"
        f"--- Contexto Actual ---\n{node_context}\n\n"
        f"--- Historial de Conversación ---\n{history_str}\n"
        f"--- Pregunta del Usuario ---\n{query}"
    )
    
    # 6. Call AI
    complex_context = (
        f"{system_prompt}\n\n"
        f"--- Base de Conocimiento ---\n{kb_str}\n\n"
        f"--- Contexto Actual ---\n{node_context}\n\n"
        f"--- Historial de Conversación ---\n{history_str}"
    )
    
    ai_response_text = generate_response(complex_context, query)
    
    # 7. Save AI Response
    ai_msg = Message(
        chat_session_id=session_id,
        sender_id=None,
        sender_type='ai',
        content=ai_response_text,
        created_at=datetime.now(timezone.utc)
    )
    db.session.add(ai_msg)
    db.session.commit()
    
    # 8. Emit to Room
    room = f"session_{session_id}"
    socketio.emit('message', {'user_id': None, 'content': ai_response_text}, room=room)
    
    return ai_response_text

def get_creator_sessions(creator_id):
    """
    Returns all chat sessions for chatbots owned by the creator, excluding resolved ones.
    """
    sessions = db.session.query(ChatSession).join(Chatbot).filter(
        Chatbot.creator_id == creator_id,
        ChatSession.status != 'resolved',
        ChatSession.type == 'human_support'
    ).all()
    return sessions

def get_session_messages(session_id):
    return Message.query.filter_by(chat_session_id=session_id).order_by(Message.created_at.asc()).all()

def switch_session_to_human(session_id):
    """
    Updates session type to human_support.
    """
    session = get_chat_session(session_id)
    if not session:
        raise ValueError("Sesión no encontrada")
    
    session.type = 'human_support'
    db.session.commit()
    return session

def switch_session_to_ai(session_id):
    """
    Updates session type to ai.
    """
    session = get_chat_session(session_id)
    if not session:
        raise ValueError("Sesión no encontrada")
    
    session.type = 'ai_conversation'
    db.session.commit()
    return session

def resolve_chat_session(session_id, user_id):
    """
    Marks a chat session as resolved.
    """
    session = get_chat_session(session_id)
    if not session:
        raise ValueError("Sesión no encontrada")
    
    # Check permission (must be participant)
    if not validate_session_access(session_id, user_id):
        raise ValueError("No autorizado")

    session.status = 'resolved'
    db.session.commit()
    return session

from flask_mail import Message as MailMessage
from . import mail

def send_contact_email(name, email, subject, message):
    if not (name and email and subject and message):
        raise ValueError('Todos los campos son obligatorios')
        
    msg = MailMessage(
        subject=f"[Contacto WebApp] {subject}",
        recipients=[mail.default_sender], # Send to self/admin
        body=f"Has recibido un nuevo mensaje de contacto:\n\nNombre: {name}\nEmail: {email}\n\nMensaje:\n{message}",
        reply_to=email
    )
    mail.send(msg)
