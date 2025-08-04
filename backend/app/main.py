from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from app.api.routes import api_router
from app.db.session import engine
from app.db.base import Base
from app.core.config import settings

# Configurazione Swagger/OpenAPI avanzata
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="🌾 Farmer Market Platform API",
        version="1.0.0",
        description="""
        ## API completa per la piattaforma di mercato agricolo

        Questa API gestisce un sistema completo di mercato agricolo con diversi stakeholder:

        ### 🔐 **Autenticazione**
        - Sistema JWT per autenticazione sicura
        - Registrazione e login utenti
        - Controllo accessi basato su ruoli

        ### 👥 **Stakeholder Supportati**
        - **🛒 Consumer**: Ricerca prodotti, prenotazioni ristoranti, recensioni
        - **🚜 Farmer**: Gestione prodotti, inventario, vendite
        - **🍽️ Restaurant Owner**: Menu, prenotazioni, gestione tavoli
        - **🎨 Workshop Host**: Organizzazione laboratori e attività
        - **🎪 Event Organizer**: Gestione eventi e coordinamento
        - **👨‍💼 Admin**: Amministrazione completa del sistema

        ### 📊 **Funzionalità Principali**
        - Gestione completa prodotti agricoli
        - Sistema di prenotazioni multi-tipo
        - Reviews e rating
        - Analytics e dashboard personalizzate
        - Gestione location e vendor
        - Sistema di richieste e approvazioni

        ### 🔗 **Come iniziare**
        1. Registrati con `/api/v1/auth/register`
        2. Effettua login con `/api/v1/auth/login`
        3. Usa il token JWT negli header: `Authorization: Bearer <token>`
        4. Accedi agli endpoint del tuo ruolo

        ---
        **🚀 Sviluppato per il progetto ASP - Farmer Market Platform**
        """,
        routes=app.routes,
    )
    
    # Aggiunge informazioni di contatto e licenza
    openapi_schema["info"]["contact"] = {
        "name": "ASP Development Team",
        "email": "support@farmermarket.com",
    }
    openapi_schema["info"]["license"] = {
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    }
    
    # Aggiunge servers per diversi ambienti
    openapi_schema["servers"] = [
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://api.farmermarket.com",
            "description": "Production server"
        }
    ]
    
    # Configura schema di sicurezza JWT
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your JWT token in the format: Bearer <token>"
        }
    }
    
    # Applica sicurezza globalmente (eccetto auth endpoints)
    for path, path_item in openapi_schema["paths"].items():
        if not path.startswith("/api/v1/auth"):
            for operation in path_item.values():
                if isinstance(operation, dict) and "operationId" in operation:
                    operation["security"] = [{"bearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app = FastAPI(
    title="🌾 Farmer Market Platform API",
    description="API per la piattaforma di mercato agricolo con gestione stakeholder",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Applica lo schema OpenAPI personalizzato
app.openapi = custom_openapi

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gestione database: ricrea ad ogni avvio in sviluppo
if settings.RESET_DB_ON_STARTUP:
    print("Eliminazione database esistente...")
    Base.metadata.drop_all(bind=engine)
    
    print("Ricreazione tabelle...")
    Base.metadata.create_all(bind=engine)
    
    print("Popolazione con dati iniziali...")
    from app.db.seed import seed_initial_data
    seed_initial_data()
    print("Database ricreato e popolato!")
else:
    # Crea solo le tabelle se non esistono
    Base.metadata.create_all(bind=engine)
    from app.db.seed import seed_initial_data, is_database_empty
    if is_database_empty():
        print("🌱 Prima inizializzazione - popolazione database...")
        seed_initial_data()

print("-" * 60)

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
