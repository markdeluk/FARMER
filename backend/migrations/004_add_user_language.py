"""
Migrazione per aggiungere il campo language al modello User
"""
from sqlalchemy import text
from app.db.session import SessionLocal


def upgrade():
    """Applica la migrazione"""
    db = SessionLocal()
    try:
        # Aggiungi la colonna language alla tabella users
        db.execute(text("ALTER TABLE users ADD COLUMN language VARCHAR DEFAULT 'it' NOT NULL;"))
        
        # Aggiorna tutti gli utenti esistenti con lingua italiana come default
        db.execute(text("UPDATE users SET language = 'it' WHERE language IS NULL;"))
        
        db.commit()
        print("✓ Migrazione 004 applicata con successo")
    except Exception as e:
        db.rollback()
        print(f"✗ Errore durante la migrazione 004: {e}")
        raise
    finally:
        db.close()


def downgrade():
    """Reverte la migrazione"""
    db = SessionLocal()
    try:
        # Rimuovi la colonna language
        db.execute(text("ALTER TABLE users DROP COLUMN language;"))
        db.commit()
        print("✓ Migrazione 004 revertita con successo")
    except Exception as e:
        db.rollback()
        print(f"✗ Errore durante il rollback della migrazione 004: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    upgrade()
