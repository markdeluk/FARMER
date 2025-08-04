"""
Migrazione per aggiungere il campo description a RoleType
"""
from sqlalchemy import text
from app.db.session import SessionLocal


def upgrade():
    """Applica la migrazione"""
    db = SessionLocal()
    try:
        # Aggiungi la colonna description alla tabella role_types
        db.execute(text("ALTER TABLE role_types ADD COLUMN description TEXT;"))
        
        # Aggiorna i ruoli esistenti con descrizioni appropriate
        db.execute(text("""
            UPDATE role_types SET description = 
            CASE 
                WHEN name = 'consumer' THEN 'Utente finale che acquista prodotti dal mercato agricolo'
                WHEN name = 'farmer' THEN 'Produttore agricolo che vende direttamente i propri prodotti'
                WHEN name = 'producer' THEN 'Produttore che trasforma materie prime in prodotti finiti'
                WHEN name = 'restaurant_owner' THEN 'Proprietario di ristorante che acquista ingredienti freschi'
                WHEN name = 'workshop_host' THEN 'Organizzatore di workshop ed eventi educativi'
                WHEN name = 'event_organizer' THEN 'Organizzatore di eventi e manifestazioni del mercato'
                WHEN name = 'admin' THEN 'Amministratore del sistema con accesso completo'
                ELSE 'Ruolo utente'
            END;
        """))
        
        db.commit()
        print("✓ Migrazione 003 applicata con successo")
    except Exception as e:
        db.rollback()
        print(f"✗ Errore durante la migrazione 003: {e}")
        raise
    finally:
        db.close()


def downgrade():
    """Reverte la migrazione"""
    db = SessionLocal()
    try:
        # Rimuovi la colonna description
        db.execute(text("ALTER TABLE role_types DROP COLUMN description;"))
        db.commit()
        print("✓ Migrazione 003 revertita con successo")
    except Exception as e:
        db.rollback()
        print(f"✗ Errore durante il rollback della migrazione 003: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    upgrade()
