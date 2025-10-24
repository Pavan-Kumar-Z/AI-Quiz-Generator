import os

class Config:
    """Configuration settings for the application"""
    
    # Base directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.path.join(os.path.dirname(BASE_DIR), 'uploads')
    
    # File upload settings
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
    
    # Model settings
    MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Quiz settings
    MIN_QUESTIONS = 5
    MAX_QUESTIONS = 20
    DEFAULT_QUESTIONS = 10
    
    # CORS settings
    CORS_ORIGINS = [
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5501",
        "http://127.0.0.1:5501"
    ]
    
    # Secret key for session management (change in production)
    SECRET_KEY = "your-secret-key-change-in-production"