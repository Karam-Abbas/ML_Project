from flask import Flask
import logging
import os

def create_app(config_name='default'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load config
    from .config import config
    app.config.from_object(config[config_name])
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Register blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    # Create upload folder
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Preload model
    with app.app_context():
        from .model import initialize_model
        initialize_model(
            model_path=app.config['MODEL_PATH'],
            device=app.config['DEVICE']
        )
        logging.info("Application initialized successfully")

    return app