from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'creator', 'user', name='user_roles'), default='user', nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    chatbots = db.relationship('Chatbot', backref='creator', lazy=True)
    messages = db.relationship('Message', backref='sender', lazy=True)

class Chatbot(db.Model):
    __tablename__ = 'chatbots'
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text)
    visibility = db.Column(db.Enum('public', 'private', 'link_only', name='visibility_types'), default='private', nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    nodes = db.relationship('Node', backref='chatbot', lazy=True, cascade="all, delete-orphan")
    chat_sessions = db.relationship('ChatSession', backref='chatbot', lazy=True)

class Node(db.Model):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True)
    chatbot_id = db.Column(db.Integer, db.ForeignKey('chatbots.id'), nullable=False)
    label = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    parent_node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'), nullable=True)

    children = db.relationship('Node', backref=db.backref('parent', remote_side=[id]), lazy=True)

class ChatSession(db.Model):
    __tablename__ = 'chat_sessions'
    id = db.Column(db.Integer, primary_key=True)
    chatbot_id = db.Column(db.Integer, db.ForeignKey('chatbots.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # Nullable for guest AI chat
    type = db.Column(db.Enum('ai_conversation', 'human_support', name='session_types'), nullable=False)
    status = db.Column(db.Enum('active', 'resolved', 'archived', name='session_status'), default='active', nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    messages = db.relationship('Message', backref='chat_session', lazy=True, cascade="all, delete-orphan")

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    chat_session_id = db.Column(db.Integer, db.ForeignKey('chat_sessions.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # Null if sender is AI or System
    sender_type = db.Column(db.Enum('user', 'creator', 'ai', 'system', name='sender_types'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
