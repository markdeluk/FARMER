"""
Migration script per aggiornare la tabella users con i nuovi campi
Aggiunge: email, password_hash, phone, is_active e rinomina name/surname
"""

import sqlite3
import os

def migrate_users_table():
    """Migra la tabella users per includere i nuovi campi"""
    
    # Path al database
    db_path = os.path.join(os.path.dirname(__file__), '..', 'test.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Backup della tabella esistente
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users_backup AS 
            SELECT * FROM users
        """)
        
        # Rimuovi la tabella users esistente
        cursor.execute("DROP TABLE IF EXISTS users")
        
        # Crea la nuova tabella users con la struttura aggiornata
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email VARCHAR UNIQUE NOT NULL,
                password_hash VARCHAR NOT NULL,
                first_name VARCHAR NOT NULL,
                last_name VARCHAR NOT NULL,
                phone VARCHAR,
                profile_picture BLOB,
                is_active BOOLEAN DEFAULT 1 NOT NULL,
                role_type_id INTEGER NOT NULL,
                FOREIGN KEY (role_type_id) REFERENCES role_types (id)
            )
        """)
        
        # Crea indici
        cursor.execute("CREATE INDEX ix_users_id ON users (id)")
        cursor.execute("CREATE INDEX ix_users_email ON users (email)")
        
        # Se esistevano dati nella tabella backup, prova a migrarli
        cursor.execute("SELECT COUNT(*) FROM users_backup")
        backup_count = cursor.fetchone()[0]
        
        if backup_count > 0:
            print(f"Trovati {backup_count} utenti da migrare...")
            
            # Migra i dati esistenti (adattando i nomi dei campi)
            # Nota: dovrai adattare questa parte in base ai tuoi dati esistenti
            cursor.execute("""
                INSERT INTO users (email, password_hash, first_name, last_name, phone, profile_picture, is_active, role_type_id)
                SELECT 
                    COALESCE(email, 'user' || id || '@example.com') as email,  -- Email di default se non presente
                    COALESCE(password_hash, 'temp_password') as password_hash,  -- Password temporanea
                    COALESCE(name, first_name, 'Nome') as first_name,
                    COALESCE(surname, last_name, 'Cognome') as last_name,
                    phone,
                    profile_picture,
                    COALESCE(is_active, 1) as is_active,
                    role_type_id
                FROM users_backup
            """)
            
            print("Migrazione completata!")
        
        conn.commit()
        print("Tabella users aggiornata con successo!")
        
    except sqlite3.Error as e:
        print(f"Errore durante la migrazione: {e}")
        conn.rollback()
    except Exception as e:
        print(f"Errore generico: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    migrate_users_table()
