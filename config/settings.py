"""
Configuration Management for AI-Accelerate
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Google Cloud Settings
    GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "ai-accelerate-demo")
    GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    # Elasticsearch Settings
    ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
    
    # Streamlit Settings
    STREAMLIT_SERVER_PORT = int(os.getenv("STREAMLIT_SERVER_PORT", "8501"))
    STREAMLIT_SERVER_ADDRESS = os.getenv("STREAMLIT_SERVER_ADDRESS", "0.0.0.0")
    
    # Voice Settings
    VOICE_LANGUAGE = os.getenv("VOICE_LANGUAGE", "en-US")
    VOICE_TIMEOUT = int(os.getenv("VOICE_TIMEOUT", "5"))
    
    # Search Settings
    DEFAULT_SEARCH_LIMIT = int(os.getenv("DEFAULT_SEARCH_LIMIT", "10"))
    ENABLE_SEMANTIC_SEARCH = os.getenv("ENABLE_SEMANTIC_SEARCH", "true").lower() == "true"
    
    # Development Settings
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    MOCK_SERVICES = os.getenv("MOCK_SERVICES", "true").lower() == "true"