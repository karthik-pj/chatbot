import os
import uuid
from werkzeug.utils import secure_filename
from utils.parsers import extract_text, chunk_text
from services.embedding_service import get_embeddings
from vector_store.chroma_client import chroma_client
from db.models import Document, UploadLog
from db.database import db

def process_and_ingest_file(file_storage, app_config, admin_user_id=None):
    filename = secure_filename(file_storage.filename)
    file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    storage_path = os.path.join(app_config['UPLOAD_FOLDER'], filename)
    file_storage.save(storage_path)
    
    # Create Document record
    doc = Document(
        file_name=filename,
        original_name=file_storage.filename,
        file_type=file_ext,
        storage_path=storage_path,
        status='processing',
        uploaded_by=admin_user_id
    )
    db.session.add(doc)
    db.session.commit()
    
    log_action(doc.id, 'upload', 'success', 'File saved to disk')
    
    try:
        # 1. Extract
        text = extract_text(storage_path, file_ext)
        if not text:
            raise ValueError("No text extracted from document.")
        log_action(doc.id, 'parse', 'success', 'Text extracted')

        # 2. Chunk
        chunks = chunk_text(text)
        log_action(doc.id, 'chunk', 'success', f'Created {len(chunks)} chunks')

        # 3. Embed & 4. Store
        if chunks:
            embeddings = get_embeddings(chunks)
            collection = chroma_client.get_collection()
            
            ids = [f"{doc.id}_{i}" for i in range(len(chunks))]
            metadatas = [{"document_id": doc.id, "file_name": filename, "file_type": file_ext, "is_active": True} for _ in chunks]
            
            collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=chunks,
                metadatas=metadatas
            )
            
            log_action(doc.id, 'embed_store', 'success', f'Stored {len(chunks)} chunks in Chroma')
            
        doc.status = 'active'
        doc.chunk_count = len(chunks)
        db.session.commit()
        
    except Exception as e:
        doc.status = 'error'
        db.session.commit()
        log_action(doc.id, 'process', 'error', str(e))
        raise e

def log_action(doc_id, action, status, message):
    log = UploadLog(document_id=doc_id, action=action, status=status, message=message)
    db.session.add(log)
    db.session.commit()
