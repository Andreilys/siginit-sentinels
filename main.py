from flask.cli import FlaskGroup
from dotenv import load_dotenv
import os
from app import create_app, socketio, db
from flask_migrate import Migrate, upgrade
import logging

# Load environment variables from .env file
load_dotenv()

app = create_app()

# Configure production logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    try:
        # Initialize database tables
        with app.app_context():
            db.create_all()
            
        socketio.run(app,
                    host="0.0.0.0",
                    port=5001,
                    debug=False,
                    log_output=True,
                    use_reloader=False,
                    allow_unsafe_werkzeug=True)
    except Exception as e:
        app.logger.error(f"Server error: {str(e)}")
        raise
