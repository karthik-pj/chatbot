import os
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
from db.database import db
from db.models import Document, ChatSession, ChatMessage, UploadLog
from services.ingestion_service import process_and_ingest_file

admin_bp = Blueprint('admin', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    total_docs = Document.query.count()
    active_docs = Document.query.filter_by(status='active').count()
    total_sessions = ChatSession.query.count()
    total_messages = ChatMessage.query.count()
    
    return render_template('admin/dashboard.html', 
                          total_docs=total_docs,
                          active_docs=active_docs,
                          total_sessions=total_sessions,
                          total_messages=total_messages)

@admin_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        files = request.files.getlist('documents')
        success_count = 0
        
        for file in files:
            if file and file.filename:
                try:
                    process_and_ingest_file(file, current_app.config, session.get('admin_id'))
                    success_count += 1
                except Exception as e:
                    flash(f"Error processing {file.filename}: {str(e)}", "error")
        
        if success_count > 0:
            flash(f"Successfully processed {success_count} files.", "success")
        return redirect(url_for('admin.documents'))
        
    return render_template('admin/upload.html')

@admin_bp.route('/documents')
@login_required
def documents():
    docs = Document.query.order_by(Document.uploaded_at.desc()).all()
    return render_template('admin/documents.html', documents=docs)

@admin_bp.route('/documents/<int:doc_id>/toggle', methods=['POST'])
@login_required
def toggle_document(doc_id):
    doc = Document.query.get_or_404(doc_id)
    if doc.status == 'active':
        doc.status = 'inactive'
    elif doc.status == 'inactive':
        doc.status = 'active'
    db.session.commit()
    # In a real app we'd also update the metadata in ChromaDB to is_active=False
    flash(f"Document {doc.file_name} status toggled.", "success")
    return redirect(url_for('admin.documents'))

@admin_bp.route('/documents/<int:doc_id>/delete', methods=['POST'])
@login_required
def delete_document(doc_id):
    doc = Document.query.get_or_404(doc_id)
    # Remove from Chroma (omitted for brevity, would delete by document_id)
    # Remove from disk
    if os.path.exists(doc.storage_path):
        try:
            os.remove(doc.storage_path)
        except OSError:
            pass
    db.session.delete(doc)
    db.session.commit()
    flash(f"Document {doc.file_name} deleted.", "success")
    return redirect(url_for('admin.documents'))

@admin_bp.route('/history')
@login_required
def history():
    sessions = ChatSession.query.order_by(ChatSession.last_active_at.desc()).all()
    return render_template('admin/history.html', sessions=sessions)

@admin_bp.route('/history/<int:session_id>')
@login_required
def view_session(session_id):
    chat_session = ChatSession.query.get_or_404(session_id)
    messages = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.created_at.asc()).all()
    return render_template('admin/session_view.html', session=chat_session, messages=messages)
