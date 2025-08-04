from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import api_router
from app.db.session import engine
from app.db.base import Base

app = FastAPI(
    title="Farmer Market Platform API",
    description="API per la piattaforma di mercato agricolo con gestione stakeholder",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crea le tabelle al primo avvio
Base.metadata.create_all(bind=engine)

# Include tutti i router API
app.include_router(api_router)

@app.get("/")
def read_root():
    return {
        "message": "Farmer Market Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "stakeholders": [
            "consumer", 
            "farmer", 
            "restaurant_owner", 
            "admin", 
            "workshop_host", 
            "event_organizer"
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
