import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key_change_in_production')
    
    # Database Configuration
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    # Fallback database config for local development
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'Marvin20nisan21.')
    DB_NAME = os.environ.get('DB_NAME', 'postgres')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    
    # CORS Configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # Session Configuration
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = './flask_session'
    PERMANENT_SESSION_LIFETIME = 900  # 15 minutes
    
    # Cache Configuration
    CACHE_TYPE = 'simple'
    
    # Environment
    ENV = os.environ.get('FLASK_ENV', 'development')
    DEBUG = ENV == 'development'
