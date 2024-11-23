from app import create_app, socketio
import logging

app = create_app()

# Configure production logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    try:
        socketio.run(app, 
                    host="0.0.0.0", 
                    port=5000,
                    debug=False,
                    use_reloader=False,
                    log_output=True,
                    allow_unsafe_werkzeug=False)
    except Exception as e:
        app.logger.error(f"Server error: {str(e)}")
        raise
