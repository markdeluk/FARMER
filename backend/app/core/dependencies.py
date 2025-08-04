from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core.auth import get_current_active_user, require_role
from app.models.user import User

# Re-export delle dipendenze di autenticazione comuni
def get_current_user(current_user: User = Depends(get_current_active_user)) -> User:
    """Ottieni l'utente corrente attivo"""
    return current_user

# Dipendenze per ruoli specifici
def get_admin_user(current_user: User = Depends(require_role("admin"))) -> User:
    return current_user

def get_farmer_user(current_user: User = Depends(require_role("farmer"))) -> User:
    return current_user

def get_consumer_user(current_user: User = Depends(require_role("consumer"))) -> User:
    return current_user

def get_restaurant_owner_user(current_user: User = Depends(require_role("restaurant_owner"))) -> User:
    return current_user

def get_workshop_host_user(current_user: User = Depends(require_role("workshop_host"))) -> User:
    return current_user

def get_event_organizer_user(current_user: User = Depends(require_role("event_organizer"))) -> User:
    return current_user

# Dipendenze comuni per la validazione
def validate_positive_int(value: int) -> int:
    """Valida che un intero sia positivo"""
    if value <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Value must be positive"
        )
    return value

def validate_pagination(skip: int = 0, limit: int = 100) -> tuple[int, int]:
    """Valida i parametri di paginazione"""
    if skip < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Skip must be non-negative"
        )
    if limit <= 0 or limit > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be between 1 and 1000"
        )
    return skip, limit
