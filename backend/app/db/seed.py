"""
Modulo per il seeding del database con dati iniziali
"""

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.user_service import user_service
from app.models.enums import RoleType
from app.core.auth import get_password_hash
import logging

logger = logging.getLogger(__name__)

def create_role_types(db: Session):
    """Crea i tipi di ruolo predefiniti se non esistono"""
    roles = [
        {"id": 1, "name": "admin", "description": "Amministratore del sistema con accesso completo"},
        {"id": 2, "name": "farmer", "description": "Produttore agricolo che vende direttamente i propri prodotti"},
        {"id": 3, "name": "consumer", "description": "Utente finale che acquista prodotti dal mercato agricolo"},
        {"id": 4, "name": "restaurant_owner", "description": "Proprietario di ristorante che acquista ingredienti freschi"},
        {"id": 5, "name": "workshop_host", "description": "Organizzatore di workshop ed eventi educativi"},
        {"id": 6, "name": "event_organizer", "description": "Organizzatore di eventi e manifestazioni del mercato"},
    ]
    
    for role_data in roles:
        existing_role = db.query(RoleType).filter(RoleType.id == role_data["id"]).first()
        if not existing_role:
            role = RoleType(**role_data)
            db.add(role)
            logger.info(f"Ruolo creato: {role_data['name']}")
        else:
            # Aggiorna la descrizione se il ruolo esiste già ma senza descrizione
            if existing_role.description is None:
                existing_role.description = role_data["description"]
                logger.info(f"Descrizione aggiornata per ruolo: {role_data['name']}")
    
    db.commit()

def create_default_admin(db: Session):
    """Crea un utente admin di default se non esiste"""
    admin_email = "admin@example.com"
    
    existing_admin = user_service.get_user_by_email(db, admin_email)
    if not existing_admin:
        # Assicurati che il ruolo admin esista
        admin_role = db.query(RoleType).filter(RoleType.name == "admin").first()
        if admin_role:
            password_hash = get_password_hash("admin123")
            
            admin = user_service.create_user(
                db=db,
                email=admin_email,
                password_hash=password_hash,
                first_name="Admin",
                last_name="User",
                phone="+39 000 000 0000",
                role_type_id=admin_role.id
            )
            logger.info(f"Admin utente creato: {admin.email}")
        else:
            logger.error("Ruolo admin non trovato - non posso creare l'utente admin")

def create_sample_users(db: Session):
    """Crea utenti di esempio per tutti i ruoli"""
    users_data = [
        {
            "email": "farmer@example.com", 
            "password": "password123",
            "first_name": "Mario",
            "last_name": "Rossi",
            "phone": "+39 123 456 7891",
            "role_name": "farmer"
        },
        {
            "email": "consumer@example.com",
            "password": "password123", 
            "first_name": "Giulia",
            "last_name": "Bianchi",
            "phone": "+39 123 456 7892",
            "role_name": "consumer"
        },
        {
            "email": "restaurant@example.com",
            "password": "password123",
            "first_name": "Antonio",
            "last_name": "Verdi",
            "phone": "+39 123 456 7893", 
            "role_name": "restaurant_owner"
        },
        {
            "email": "workshop@example.com",
            "password": "password123",
            "first_name": "Elena",
            "last_name": "Neri",
            "phone": "+39 123 456 7894",
            "role_name": "workshop_host"
        },
        {
            "email": "events@example.com",
            "password": "password123",
            "first_name": "Marco",
            "last_name": "Blu",
            "phone": "+39 123 456 7895",
            "role_name": "event_organizer"
        }
    ]
    
    for user_data in users_data:
        # Trova il ruolo
        role = db.query(RoleType).filter(RoleType.name == user_data["role_name"]).first()
        if role:
            existing_user = user_service.get_user_by_email(db, user_data["email"])
            if not existing_user:
                password_hash = get_password_hash(user_data["password"])
                
                user = user_service.create_user(
                    db=db,
                    email=user_data["email"],
                    password_hash=password_hash,
                    first_name=user_data["first_name"],
                    last_name=user_data["last_name"],
                    phone=user_data["phone"],
                    role_type_id=role.id
                )
                logger.info(f"Utente creato: {user.email} ({user_data['role_name']})")
            else:
                logger.info(f"Utente già esistente: {user_data['email']}")
        else:
            logger.error(f"Ruolo {user_data['role_name']} non trovato")

def seed_initial_data():
    """Popola il database con i dati iniziali necessari"""
    db = SessionLocal()
    
    try:
        logger.info("Inizio seeding dati iniziali...")
        
        # Crea ruoli base
        create_role_types(db)
        
        # Crea admin di default
        create_default_admin(db)
        
        # Crea utenti di esempio
        create_sample_users(db)
        
        logger.info("Seeding completato con successo")
        logger.info("Utenti disponibili:")
        logger.info("  - admin@example.com (admin123) - Admin")
        logger.info("  - farmer@example.com (password123) - Farmer")
        logger.info("  - consumer@example.com (password123) - Consumer")
        logger.info("  - restaurant@example.com (password123) - Restaurant Owner")
        logger.info("  - workshop@example.com (password123) - Workshop Host")
        logger.info("  - events@example.com (password123) - Event Organizer")
        
    except Exception as e:
        logger.error(f"Errore durante il seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def is_database_empty() -> bool:
    """Verifica se il database è vuoto (prima inizializzazione)"""
    db = SessionLocal()
    try:
        # Controlla se esistono ruoli
        role_count = db.query(RoleType).count()
        return role_count == 0
    finally:
        db.close()
