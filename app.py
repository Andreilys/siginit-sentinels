import os
from datetime import timedelta
from flask import Flask, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

csrf = CSRFProtect()
from flask_jwt_extended import JWTManager
jwt = JWTManager()

db = SQLAlchemy(model_class=Base)
migrate = Migrate(directory='migrations')
socketio = SocketIO(
    cors_allowed_origins="*",
    async_mode='gevent',
    ping_timeout=60,
    ping_interval=25,
    transport='websocket'
)
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Enhanced Configuration
    app.config.update(
        JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY", os.urandom(24).hex()),
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1),
        SECRET_KEY=os.environ.get("FLASK_SECRET_KEY", os.urandom(24).hex()),
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL"),
        SQLALCHEMY_ENGINE_OPTIONS={
            "pool_recycle": 300,
            "pool_pre_ping": True,
            "pool_timeout": 30,
            "pool_size": 30,
            "max_overflow": 0,
            "connect_args": {"connect_timeout": 10}
        },
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        PERMANENT_SESSION_LIFETIME=1800,  # 30 minutes
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        REMEMBER_COOKIE_SECURE=True,
        REMEMBER_COOKIE_HTTPONLY=True,
        REMEMBER_COOKIE_DURATION=timedelta(days=14),
        WTF_CSRF_CHECK_DEFAULT=False
    )
    
    # Configure session interface for better security
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = os.path.join(os.getcwd(), 'flask_session')
    app.config['SESSION_FILE_THRESHOLD'] = 500  # Maximum number of sessions stored on disk
    
    # Enhanced database initialization and connection handling
    try:
        db.init_app(app)
        with app.app_context():
            # Test database connection with timeout
            connection = db.engine.connect()
            connection.execute(db.text('SELECT 1'))
            connection.close()
            app.logger.info("Database connection successful")
            
            # Set up connection pooling monitor
            @app.before_request
            def check_db_connection():
                try:
                    db.session.execute(db.text('SELECT 1'))
                except Exception as e:
                    app.logger.error(f"Database connection lost: {str(e)}")
                    db.session.rollback()
                    return "Database connection error. Please try again.", 503
                
            @app.teardown_request
            def cleanup_db_session(exc=None):
                if exc:
                    db.session.rollback()
                    app.logger.error(f"Request error occurred: {str(exc)}")
                db.session.remove()
                
    except Exception as e:
        app.logger.error(f"Database initialization failed: {str(e)}", exc_info=True)
        raise
        
    socketio.init_app(app, 
    async_mode='gevent',
    ping_timeout=60,
    ping_interval=25,
    transport='websocket',
    cors_allowed_origins='*'
)
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
