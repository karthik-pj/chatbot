# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-fallback')
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
#     LLM_MODEL_NAME = os.environ.get('LLM_MODEL_NAME', 'llama3-70b-8192')
#     UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
#     MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-fallback')
    # This will use Render's PostgreSQL URL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
    LLM_MODEL_NAME = os.environ.get('LLM_MODEL_NAME', 'llama3-70b-8192')
    # For Render, use /tmp for uploads (ephemeral storage)
    UPLOAD_FOLDER = os.path.join('/tmp', 'uploads') if os.environ.get('RENDER') else os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024