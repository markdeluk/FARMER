#!/usr/bin/env python3
"""
Script per avviare il server FastAPI con configurazione personalizzata per Swagger
"""

import uvicorn
import os
import sys

# Aggiungi il path dell'app al PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🌾 Starting Farmer Market Platform API Server...")
    print("📚 Swagger UI available at: http://localhost:8000/docs")
    print("📖 ReDoc available at: http://localhost:8000/redoc")
    print("🔍 Advanced docs available at: http://localhost:8000/docs-advanced")
    print("📊 OpenAPI JSON at: http://localhost:8000/openapi.json")
    print("🚀 API endpoints at: http://localhost:8000/api/v1/")
    print("-" * 60)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["app"],
        log_level="info",
        access_log=True
    )
