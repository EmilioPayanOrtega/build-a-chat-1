from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User

def register_user(username, email, password):
    if not (username and email and password):
        raise ValueError('Missing data')
    
    if User.query.filter((User.username == username) | (User.email == email)).first():
        raise ValueError('Username or email already exists')

    try:
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except Exception as e:
        db.session.rollback()
        raise e

def authenticate_user(username, password):
    if not (username and password):
        raise ValueError('Incomplete data')
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password_hash, password):
        raise ValueError('Invalid username or password')

    return user

from .models import Chatbot, Node
from .utils.tree_parser import validate_tree, nodes_to_json
from .utils.ai_client import generate_response

def create_chatbot(user_id, title, description, visibility, tree_json):
    if not (title and visibility):
        raise ValueError('Missing required fields')
    
    # Validate tree
    if tree_json:
        if not validate_tree(tree_json):
             raise ValueError("Invalid tree format")

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
    chatbot = db.session.get(Chatbot, chatbot_id)
    if not chatbot:
        return None
    return chatbot

def get_chatbot_tree(chatbot_id):
    nodes = Node.query.filter_by(chatbot_id=chatbot_id).all()
    return nodes_to_json(nodes)

def ask_chatbot(chatbot_id, current_node_id, query):
    """
    Queries the AI with context from the current node and its immediate children.
    """
    # 1. Fetch current node
    current_node = db.session.get(Node, current_node_id)
    if not current_node or current_node.chatbot_id != chatbot_id:
        raise ValueError("Node not found or does not belong to this chatbot")
        
    # 2. Fetch children
    children = Node.query.filter_by(parent_node_id=current_node_id).all()
    
    # 3. Construct Context
    context_parts = []
    context_parts.append(f"Current Topic: {current_node.label}")
    if current_node.content:
        context_parts.append(f"Details: {current_node.content}")
        
    if children:
        context_parts.append("Sub-topics:")
        for child in children:
            child_info = f"- {child.label}"
            if child.content:
                child_info += f": {child.content}"
            context_parts.append(child_info)
            
    context = "\n".join(context_parts)
    
    # 4. Call AI
    return generate_response(context, query)

def list_chatbots(search_query=None):
    query = Chatbot.query.filter_by(is_active=True, visibility='public')
    if search_query:
        query = query.filter(Chatbot.title.ilike(f'%{search_query}%'))
    return query.all()

def delete_chatbot(chatbot_id, user_id):
    chatbot = db.session.get(Chatbot, chatbot_id)
    if not chatbot:
        raise ValueError('Chatbot not found')
    if chatbot.creator_id != user_id:
        raise ValueError('Unauthorized')
    
    db.session.delete(chatbot)
    db.session.commit()
