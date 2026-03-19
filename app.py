# import os
# from flask import Flask
# from config import Config
# from db.database import db

# def create_app(config_class=Config):
#     app = Flask(__name__)
#     app.config.from_object(config_class)

#     # Ensure upload folder exists
#     os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
#     # Initialize DB
#     db.init_app(app)

#     # Ensure vector store data folder exists
#     os.makedirs('data/chroma_db', exist_ok=True)

#     # Import and register blueprints
#     from routes.public_routes import public_bp
#     from routes.admin_routes import admin_bp
#     from routes.auth_routes import auth_bp
    
#     app.register_blueprint(public_bp)
#     app.register_blueprint(admin_bp, url_prefix='/admin')
#     app.register_blueprint(auth_bp, url_prefix='/admin')

#     return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True, port=5000)


import os
from flask import Flask
from config import Config
from db.database import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Handle different environments
    if os.environ.get('RENDER'):
        # On Render, use /tmp for uploads (ephemeral)
        os.makedirs('/tmp/uploads', exist_ok=True)
        os.makedirs('/tmp/chroma_db', exist_ok=True)
    else:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        os.makedirs('data/chroma_db', exist_ok=True)
    
    db.init_app(app)
    
    # Register blueprints
    from routes.public_routes import public_bp
    from routes.admin_routes import admin_bp
    from routes.auth_routes import auth_bp
    
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/admin')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)