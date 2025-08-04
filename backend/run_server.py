#!/usr/bin/env python3
"""
Script per avviare il server FastAPI con configurazione personalizzata per Swagger
"""

import uvicorn
import os
import sys

# Aggiungi il path dell'app al PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings

if __name__ == "__main__":
    print("🌾 Starting Farmer Market Platform API Server...")
    print(f"📚 Swagger UI available at: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"📖 ReDoc available at: http://{settings.HOST}:{settings.PORT}/redoc")
    print(f"🔍 Advanced docs available at: http://{settings.HOST}:{settings.PORT}/docs-advanced")
    print(f"📊 OpenAPI JSON at: http://{settings.HOST}:{settings.PORT}/openapi.json")
    print(f"🚀 API endpoints at: http://{settings.HOST}:{settings.PORT}/api/v1/")
    print(f"🗑️  Reset DB on startup: {settings.RESET_DB_ON_STARTUP}")
    print("-" * 60)
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        reload_dirs=["app"],
        log_level="info" if not settings.DEBUG else "debug",
        access_log=True
    )
