#!/usr/bin/env python3
"""
Script per popolare il database con dati di esempio
Utilizza i services esistenti per mantenere la coerenza
"""

import sys
import os
from datetime import datetime

# Aggiungi il path dell'app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.services.user_service import user_service
from app.models.enums import RoleType
from app.core.auth import get_password_hash

def create_role_types(db: Session):
    """Crea i tipi di ruolo predefiniti"""
    roles = [
        {"id": 1, "name": "admin", "description": "Amministratore del sistema"},
        {"id": 2, "name": "farmer", "description": "Agricoltore/Produttore"},
        {"id": 3, "name": "consumer", "description": "Consumatore/Cliente"},
        {"id": 4, "name": "restaurant_owner", "description": "Proprietario di ristorante"},
        {"id": 5, "name": "workshop_host", "description": "Organizzatore di workshop"},
        {"id": 6, "name": "event_organizer", "description": "Organizzatore di eventi"},
    ]
    
    for role_data in roles:
        # Verifica se il ruolo esiste già
        existing_role = db.query(RoleType).filter(RoleType.id == role_data["id"]).first()
        if not existing_role:
            role = RoleType(**role_data)
            db.add(role)
    
    db.commit()
    print("✅ Ruoli creati con successo")

def create_sample_users(db: Session):
    """Crea utenti di esempio utilizzando il service"""
    users_data = [
        {
            "email": "admin@example.com",
            "password": "password123",
            "first_name": "Admin",
            "last_name": "User",
            "phone": "+39 123 456 7890",
            "role_type_id": 1  # admin
        },
        {
            "email": "farmer@example.com", 
            "password": "password123",
            "first_name": "Mario",
            "last_name": "Rossi",
            "phone": "+39 123 456 7891",
            "role_type_id": 2  # farmer
        },
        {
            "email": "consumer@example.com",
            "password": "password123", 
            "first_name": "Giulia",
            "last_name": "Bianchi",
            "phone": "+39 123 456 7892",
            "role_type_id": 3  # consumer
        },
        {
            "email": "restaurant@example.com",
            "password": "password123",
            "first_name": "Antonio",
            "last_name": "Verdi",
            "phone": "+39 123 456 7893", 
            "role_type_id": 4  # restaurant_owner
        },
        {
            "email": "workshop@example.com",
            "password": "password123",
            "first_name": "Elena",
            "last_name": "Neri",
            "phone": "+39 123 456 7894",
            "role_type_id": 5  # workshop_host
        },
        {
            "email": "events@example.com",
            "password": "password123",
            "first_name": "Marco",
            "last_name": "Blu",
            "phone": "+39 123 456 7895",
            "role_type_id": 6  # event_organizer
        }
    ]
    
    for user_data in users_data:
        # Verifica se l'utente esiste già
        existing_user = user_service.get_user_by_email(db, user_data["email"])
        if not existing_user:
            # Hash della password
            password_hash = get_password_hash(user_data["password"])
            
            # Crea l'utente usando il service
            user = user_service.create_user(
                db=db,
                email=user_data["email"],
                password_hash=password_hash,
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                phone=user_data["phone"],
                role_type_id=user_data["role_type_id"]
            )
            print(f"✅ Utente creato: {user.email} ({user.first_name} {user.last_name})")
        else:
            print(f"⚠️  Utente già esistente: {user_data['email']}")

def create_sample_products(db: Session):
    """Crea prodotti di esempio"""
    # Il modello Product attuale ha una struttura più complessa
    # con market_id, category_id, unit_measure_id
    # Per ora saltiamo la creazione dei prodotti
    # finché non abbiamo i dati di riferimento necessari
    
    print("⚠️  Creazione prodotti saltata - necessari market, category e unit_measure")
    print("   Puoi aggiungere questi dati manualmente o estendere questo script")

def seed_database():
    """Funzione principale per popolare il database"""
    print("🌱 Inizio popolazione database...")
    
    # Crea le tabelle se non esistono
    Base.metadata.create_all(bind=engine)
    
    # Crea una sessione database
    db = SessionLocal()
    
    try:
        # Popola in ordine di dipendenza
        create_role_types(db)
        create_sample_users(db)
        create_sample_products(db)
        
        print("🎉 Database popolato con successo!")
        print("\n📋 Utenti creati:")
        print("   - admin@example.com (password123) - Admin")
        print("   - farmer@example.com (password123) - Farmer") 
        print("   - consumer@example.com (password123) - Consumer")
        print("   - restaurant@example.com (password123) - Restaurant Owner")
        print("   - workshop@example.com (password123) - Workshop Host")
        print("   - events@example.com (password123) - Event Organizer")
        
    except Exception as e:
        print(f"❌ Errore durante la popolazione: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def reset_database():
    """Elimina e ricrea tutte le tabelle, poi popola con dati di esempio"""
    print("🗑️  Eliminazione database esistente...")
    Base.metadata.drop_all(bind=engine)
    
    print("🔨 Ricreazione tabelle...")
    Base.metadata.create_all(bind=engine)
    
    print("🌱 Popolazione con dati di esempio...")
    seed_database()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset_database()
    else:
        seed_database()
