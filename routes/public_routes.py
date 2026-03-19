import uuid
from flask import Blueprint, render_template, request, jsonify, session as flask_session
from db.database import db
from db.models import ChatSession, ChatMessage
from services.scope_detection_service import classify_intent
from services.retrieval_service import retrieve_context
from services.prompt_service import build_prompt
from services.llm_service import generate_response

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def chat_ui():
    if 'session_token' not in flask_session:
        flask_session['session_token'] = str(uuid.uuid4())
    return render_template('public/chat.html')

@public_bp.route('/chat/submit', methods=['POST'])
def chat_submit():
    data = request.json
    user_message_text = data.get('message', '').strip()
    session_token = flask_session.get('session_token')
    
    if not user_message_text or not session_token:
        return jsonify({"error": "Invalid request"}), 400
        
    # Get or create session
    chat_session = ChatSession.query.filter_by(session_token=session_token).first()
    if not chat_session:
        chat_session = ChatSession(session_token=session_token)
        db.session.add(chat_session)
        db.session.commit()
        
    # Save user message
    user_msg = ChatMessage(session_id=chat_session.id, sender_type='user', message_text=user_message_text)
    db.session.add(user_msg)
    
    # 1. Retrieve History (last 10 messages for context window)
    history = ChatMessage.query.filter_by(session_id=chat_session.id).order_by(ChatMessage.id.desc()).limit(10).all()
    history = history[::-1] # chronological
    
    # 2. Scope Detection
    scope = classify_intent(user_message_text)
    
    # 3. Retrieval
    context_chunks = []
    if scope in ['company_in_scope', 'mixed_scope', 'company_vague']:
        context_chunks = retrieve_context(user_message_text, top_k=3)
    
    # Check if context_chunks were actually found when expected
    if scope in ['company_in_scope', 'mixed_scope'] and not context_chunks:
         scope = 'company_vague'
        
    # 4. Build Prompt
    messages = build_prompt(user_message_text, history, context_chunks, scope)
    
    # 5. Generate Response
    assistant_text = generate_response(messages)
    
    # Save assistant message
    assistant_msg = ChatMessage(session_id=chat_session.id, sender_type='assistant', message_text=assistant_text)
    db.session.add(assistant_msg)
    
    chat_session.last_active_at = db.func.now()
    db.session.commit()
    
    return jsonify({
        "response": assistant_text,
        "scope_detected": scope # for debugging, hidden in UI
    })
