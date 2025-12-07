from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone
from sqlalchemy import Enum

db = SQLAlchemy()

# === ENUMS separados (PostgreSQL friendly) ===
user_roles_enum = Enum('admin', 'creator', 'user', name='user_roles')
visibility_enum = Enum('public', 'private', 'link_only', name='visibility_types')
session_types_enum = Enum('ai_conversation', 'human_support', name='session_types')
session_status_enum = Enum('active', 'resolved', 'archived', name='session_status')
sender_types_enum = Enum('user', 'creator', 'ai', 'system', name='sender_types')

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(user_roles_enum, default='user', nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    chatbots = db.relationship('Chatbot', backref='creator', lazy=True)
    messages = db.relationship('Message', backref='sender', lazy=True)

class Chatbot(db.Model):
    __tablename__ = 'chatbots'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text)
    visibility = db.Column(visibility_enum, default='private', nullable=False)
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

    children = db.relationship(
        'Node',
        backref=db.backref('parent', remote_side=[id]),
        lazy=True
    )

class ChatSession(db.Model):
    __tablename__ = 'chat_sessions'

    id = db.Column(db.Integer, primary_key=True)
    chatbot_id = db.Column(db.Integer, db.ForeignKey('chatbots.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    type = db.Column(session_types_enum, nullable=False)
    status = db.Column(session_status_enum, default='active', nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    messages = db.relationship('Message', backref='chat_session', lazy=True, cascade="all, delete-orphan")

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    chat_session_id = db.Column(db.Integer, db.ForeignKey('chat_sessions.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    sender_type = db.Column(sender_types_enum, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
