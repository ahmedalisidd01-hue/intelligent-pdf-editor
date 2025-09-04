import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    UPLOAD_FOLDER = 'uploads'
    OUTPUT_FOLDER = 'outputs'
    ALLOWED_EXTENSIONS = {'pdf'}
    
    # Hugging Face Configuration
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
    HUGGINGFACE_MODEL = os.getenv('HUGGINGFACE_MODEL', 'mistralai/Mistral-7B-Instruct-v0.1')
    
    # Humanization settings
    HUMANIZATION_PROMPT = """
    Rewrite the following text to make it sound more human and natural while preserving the original meaning. 
    Use varied sentence structures, natural phrasing, and avoid repetitive patterns. 
    Make it sound like it was written by a human expert in the field.
    Add some natural variations in sentence length and structure.
    """
EOL