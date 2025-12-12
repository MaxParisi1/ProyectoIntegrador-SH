"""
Configuración centralizada del sistema.
Carga las variables de entorno y proporciona acceso a la configuración.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Configurar tokenizers antes de cargar cualquier cosa
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Cargar variables de entorno
load_dotenv()

class Config:
    """Clase de configuración centralizada"""
    
    # Directorio base del proyecto
    BASE_DIR = Path(__file__).parent.parent.parent
    
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    
    # Modelos
    LLM_MODEL = os.getenv("LLM_MODEL", "llama3-70b-8192")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    
    # Rutas de archivos
    DATA_CSV_PATH = BASE_DIR / os.getenv("DATA_CSV_PATH", "data/saldos.csv")
    KNOWLEDGE_BASE_PATH = BASE_DIR / os.getenv("KNOWLEDGE_BASE_PATH", "knowledge_base/")
    VECTORSTORE_PATH = BASE_DIR / os.getenv("VECTORSTORE_PATH", "vectorstore/")
    
    # Configuración de la aplicación
    APP_TITLE = os.getenv("APP_TITLE", "Sistema de Atención al Cliente - BANCO HENRY")
    APP_PORT = int(os.getenv("APP_PORT", "8501"))
    
    @classmethod
    def validate(cls):
        """Valida que las configuraciones necesarias estén presentes"""
        errors = []
        
        if not cls.GROQ_API_KEY:
            errors.append("GROQ_API_KEY no configurada")
        
        if not cls.DATA_CSV_PATH.exists():
            errors.append(f"Archivo CSV no encontrado: {cls.DATA_CSV_PATH}")
        
        if not cls.KNOWLEDGE_BASE_PATH.exists():
            errors.append(f"Directorio de knowledge base no encontrado: {cls.KNOWLEDGE_BASE_PATH}")
        
        if errors:
            raise ValueError(
                "Errores de configuración:\n" + "\n".join(f"- {error}" for error in errors)
            )
        
        return True

# Validar configuración al importar
try:
    Config.validate()
except ValueError as e:
    print(f"⚠️  Advertencia: {e}")
