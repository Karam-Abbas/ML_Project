import os
from pathlib import Path

class Config:
    """Base configuration"""
    BASE_DIR = Path(__file__).parent.parent
    MODEL_PATH = os.getenv('MODEL_PATH', str(BASE_DIR / 'models' / 'best_vit_brain_tumor.pth'))
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', '/tmp')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    
    # Model configuration
    IMG_SIZE = 224
    CLASS_NAMES = ['glioma', 'meningioma', 'no tumor', 'pituitary']
    
    # Device configuration - CPU for production (EC2)
    DEVICE = 'cpu'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    ENV = 'production'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}