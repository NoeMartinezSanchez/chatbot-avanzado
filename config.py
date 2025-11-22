import os
from typing import Dict, Any

class Config:
    """Configuración centralizada del chatbot"""
    
    # Configuración de la aplicación
    DEBUG = True
    SECRET_KEY = 'chatbot-propedeutico-secret-key'
    
    # Rutas de archivos
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    INTENTS_FILE = os.path.join(BASE_DIR, 'data', 'intents.json')
    CONVERSATIONS_DIR = os.path.join(BASE_DIR, 'data', 'conversations')
    
    # Configuración del chatbot
    MIN_CONFIDENCE = 0.3
    MAX_RESPONSES = 5
    ENABLE_LOGGING = True
    
    # Configuración de NLP (para futuras fases)
    USE_NLP = False
    NLP_MODEL = "spacy"  # "nltk", "spacy", "transformers"
    
    @classmethod
    def get_settings(cls) -> Dict[str, Any]:
        """Retorna todas las configuraciones"""
        return {
            key: value for key, value in cls.__dict__.items() 
            if not key.startswith('_') and not callable(value)
        }