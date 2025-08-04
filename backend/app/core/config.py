"""
Configurazione dell'applicazione utilizzando variabili d'ambiente
"""

import os
from typing import List

# Carica le variabili d'ambiente dal file .env se esiste
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv non installato, usa solo variabili d'ambiente del sistema
    pass

class Settings:
    """Configurazioni dell'applicazione"""
    
    # Database
    RESET_DB_ON_STARTUP: bool = os.getenv("RESET_DB_ON_STARTUP", "true").lower() == "true"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
    
    # Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    @property
    def database_url(self) -> str:
        """Ritorna l'URL del database con path assoluto per SQLite"""
        if self.DATABASE_URL.startswith("sqlite:///"):
            # Converte path relativo in assoluto
            db_path = self.DATABASE_URL.replace("sqlite:///", "")
            if not os.path.isabs(db_path):
                db_path = os.path.join(self.BASE_DIR, db_path)
            return f"sqlite:///{db_path}"
        return self.DATABASE_URL

# Istanza globale delle configurazioni
settings = Settings()

# Per compatibilità con il codice esistente
RESET_DB_ON_STARTUP = settings.RESET_DB_ON_STARTUP
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
