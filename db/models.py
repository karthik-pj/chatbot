from datetime import datetime, timezone
from db.database import db

class AdminUser(db.Model):
    __tablename__ = 'admin_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class ChatSession(db.Model):
    __tablename__ = 'chat_sessions'
    id = db.Column(db.Integer, primary_key=True)
    session_token = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_active_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    messages = db.relationship('ChatMessage', backref='session', lazy=True, cascade="all, delete-orphan")

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('chat_sessions.id'), nullable=False)
    sender_type = db.Column(db.String(20), nullable=False) # 'user' or 'assistant'
    message_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), nullable=False) # name on disk
    original_name = db.Column(db.String(255), nullable=False) # uploaded name
    file_type = db.Column(db.String(50), nullable=False)
    storage_path = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(50), default='pending') # pending, processing, active, error, inactive
    chunk_count = db.Column(db.Integer, default=0)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('admin_users.id'), nullable=True)
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    logs = db.relationship('UploadLog', backref='document', lazy=True, cascade="all, delete-orphan")

class UploadLog(db.Model):
    __tablename__ = 'upload_logs'
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False) # e.g. 'parse', 'embed', 'upload'
    status = db.Column(db.String(50), nullable=False) # e.g. 'success', 'error'
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
