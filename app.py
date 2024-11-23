import os
from flask import Flask, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

csrf = CSRFProtect()

db = SQLAlchemy(model_class=Base)
socketio = SocketIO(
    cors_allowed_origins="*",
    async_mode='gevent',
    ping_timeout=60,
    ping_interval=25
)
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config.update(
        SECRET_KEY=os.environ.get("FLASK_SECRET_KEY", "a secret key"),
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL"),
        SQLALCHEMY_ENGINE_OPTIONS={
            "pool_recycle": 300,
            "pool_pre_ping": True,
            "pool_timeout": 30,
            "pool_size": 30,
            "max_overflow": 0,
        },
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        PERMANENT_SESSION_LIFETIME=1800,  # 30 minutes
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True
    )
    
    # Initialize extensions
    try:
        db.init_app(app)
        with app.app_context():
            db.engine.connect()
            app.logger.info("Database connection successful")
    except Exception as e:
        app.logger.error(f"Database connection failed: {str(e)}")
        raise
        
    socketio.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'  # type: ignore
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'
    login_manager.session_protection = 'strong'
    
    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))
    
    # SocketIO event handlers
    @socketio.on_error()
    def error_handler(e):
        app.logger.error(f'SocketIO error: {str(e)}')

    @socketio.on('connect')
    def handle_connect():
        app.logger.info('Client connected to SocketIO')

    @socketio.on('disconnect')
    def handle_disconnect():
        app.logger.info('Client disconnected from SocketIO')


    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    with app.app_context():
        try:
            import models
            db.create_all()
            
            # Check if admin user exists, if not create one
            from models import User
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User()
                admin.username = 'admin'
                admin.email = 'admin@intelligence.mil'
                admin.role = 'admin'
                admin.set_password('admin123')  # Initial password that should be changed
                db.session.add(admin)
                db.session.commit()
                app.logger.info('Created initial admin user')
        except Exception as e:
            app.logger.error(f'Error during initialization: {str(e)}')
            raise

    return app
