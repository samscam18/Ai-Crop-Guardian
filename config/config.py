
import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

class Config:
    """System configuration"""
    
    # Base paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / 'data' / 'datasets'
    MODEL_DIR = BASE_DIR / 'models' / 'saved_models'
    UPLOAD_DIR = BASE_DIR / 'uploads'
    
    # Model parameters
    IMG_SIZE = (224, 224)
    BATCH_SIZE = 32
    EPOCHS = 32
    LEARNING_RATE = 0.001
    MODEL_ARCHITECTURE = 'resnet50'  # resnet50, vgg16, mobilenet
    
    # Disease classes (example - expand based on dataset)
    DISEASE_CLASSES = [
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Pepper_bell___Bacterial_spot',
    'Pepper_bell___healthy'
    ]
    
    # API keys (use environment variables in production)
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_PORT = 5000
    FLASK_HOST = '0.0.0.0'
    
    DEFAULT_LOCATION = 'Bengaluru, India'

    # Multilingual support
    SUPPORTED_LANGUAGES = ['en', 'hi', 'te', 'ta', 'kn', 'mr']
    DEFAULT_LANGUAGE = 'en'
    
    # Thresholds
    CONFIDENCE_THRESHOLD = 0.3
    
    @staticmethod
    def create_directories():
        """Create necessary directories"""
        for directory in [Config.DATA_DIR, Config.MODEL_DIR, Config.UPLOAD_DIR]:
            directory.mkdir(parents=True, exist_ok=True)

