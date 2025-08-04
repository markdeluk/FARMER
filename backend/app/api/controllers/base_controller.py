from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import get_db
from app.services import user_service, location_service
from app.models.user import User

router = APIRouter()

# Dependency per ottenere l'utente corrente (da implementare con autenticazione)
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.auth import (
    get_current_user as auth_get_current_user,
    get_current_active_user,
    require_role as auth_require_role,
    require_roles as auth_require_roles,
    AuthenticationError,
    AuthorizationError
)
from app.models.user import User

# Re-export delle funzioni di autenticazione per compatibilità
get_current_user = auth_get_current_user
require_role = auth_require_role
require_roles = auth_require_roles

# Dipendenze di ruolo predefinite
require_admin = auth_require_role("admin")
require_farmer = auth_require_role("farmer") 
require_consumer = auth_require_role("consumer")
require_restaurant_owner = auth_require_role("restaurant_owner")
require_workshop_host = auth_require_role("workshop_host")
require_event_organizer = auth_require_role("event_organizer")

# Dipendenze per ruoli multipli
require_vendor_role = auth_require_roles("farmer", "restaurant_owner", "workshop_host")
require_organizer_role = auth_require_roles("workshop_host", "event_organizer")

def get_current_user_id(current_user: User = Depends(get_current_user)) -> int:
    """Helper per ottenere solo l'ID dell'utente corrente"""
    return current_user.id

def check_resource_ownership(resource_owner_id: int, current_user: User) -> None:
    """Verifica che l'utente corrente sia il proprietario della risorsa"""
    if resource_owner_id != current_user.id and current_user.role.name != "admin":
        raise AuthorizationError("You don't have permission to access this resource")

def require_owner_or_admin(resource_owner_id: int):
    """Factory per creare dipendenze che richiedono di essere proprietari o admin"""
    def ownership_checker(current_user: User = Depends(get_current_user)) -> User:
        check_resource_ownership(resource_owner_id, current_user)
        return current_user
    return ownership_checker

# Dependency per verificare il ruolo utente
def require_role(required_role: str):
    """Factory per creare dependency che verifica il ruolo"""
    def check_role(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        if current_user.role_type.name != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {required_role}"
            )
        return current_user
    return check_role

@router.get("/")
def root():
    return {"message": "ASP Platform API", "version": "1.0"}

@router.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}

@router.get("/locations/search")
def search_locations(
    search: str,
    db: Session = Depends(get_db)
):
    """Cerca location per indirizzo - disponibile a tutti"""
    return location_service.search_by_address(db, search)