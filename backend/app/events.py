from flask import request
from flask_socketio import emit, join_room, leave_room
from . import socketio
from .services import validate_session_access, save_message

@socketio.on('join')
def on_join(data):
    """
    Client joins a chat session room.
    Data: { 'session_id': int, 'user_id': int }
    """
    session_id = data.get('session_id')
    user_id = data.get('user_id')
    print(f"DEBUG: on_join called for session {session_id}, user {user_id}")
    
    if not session_id or not user_id:
        return
        
    if validate_session_access(session_id, user_id):
        room = f"session_{session_id}"
        join_room(room)
        emit('status', {'msg': f'User {user_id} has entered the room.'}, room=room)
    else:
        emit('error', {'msg': 'Unauthorized access to this session.'})

@socketio.on('message')
def on_message(data):
    """
    Client sends a message.
    Data: { 'session_id': int, 'user_id': int, 'content': str }
    """
    session_id = data.get('session_id')
    user_id = data.get('user_id')
    content = data.get('content')
    
    if not (session_id and user_id and content):
        return

    # Validate again to be safe (though usually done on join)
    try:
        if validate_session_access(session_id, user_id):
            # 1. Save to DB
            save_message(session_id, user_id, content)
            
            # 2. Emit to Room (Real-time)
            room = f"session_{session_id}"
            emit('message', {'user_id': user_id, 'content': content}, room=room)
        else:
            emit('error', {'msg': 'Unauthorized'})
    except Exception as e:
        print(f"ERROR in on_message: {e}")
        emit('error', {'msg': str(e)})

@socketio.on('request_human')
def on_request_human(data):
    """
    Client requests human support.
    Data: { 'session_id': int, 'user_id': int }
    """
    session_id = data.get('session_id')
    user_id = data.get('user_id')
    
    if not session_id or not user_id:
        return

    try:
        if validate_session_access(session_id, user_id):
            from .services import switch_session_to_human
            switch_session_to_human(session_id)
            
            room = f"session_{session_id}"
            emit('status', {'msg': 'Human support requested. Waiting for an agent...'}, room=room)
            emit('session_updated', {'type': 'human_support'}, room=room)
        else:
            emit('error', {'msg': 'Unauthorized'})
    except Exception as e:
        print(f"ERROR in on_request_human: {e}")
        emit('error', {'msg': str(e)})

@socketio.on('disconnect')
def handle_disconnect():
    print(f"Client disconnected: {request.sid}")
