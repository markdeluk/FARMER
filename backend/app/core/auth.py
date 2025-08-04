from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.user_service import UserService
from app.models.user import User

# Configurazione JWT
SECRET_KEY = "your-secret-key-here-change-in-production"  # Cambiare in produzione!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configurazione password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security scheme
security = HTTPBearer()

user_service = UserService()

class AuthenticationError(HTTPException):
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

class AuthorizationError(HTTPException):
    def __init__(self, detail: str = "Not enough permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica la password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash della password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crea un token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    """Verifica e decodifica un token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise AuthenticationError()
        return {"user_id": user_id}
    except JWTError:
        raise AuthenticationError()

def authenticate_user(db: Session, email: str, password: str) -> Union[User, bool]:
    """Autentica un utente con email e password"""
    user = user_service.get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Dipendenza per ottenere l'utente corrente dal token"""
    token_data = verify_token(credentials.credentials)
    user = user_service.get(db, token_data["user_id"])
    if user is None:
        raise AuthenticationError()
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Dipendenza per ottenere l'utente corrente attivo"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def require_role(required_role: str):
    """Factory per creare dipendenze che richiedono un ruolo specifico"""
    def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role.name != required_role:
            raise AuthorizationError(
                detail=f"Role '{required_role}' required"
            )
        return current_user
    return role_checker

def require_roles(*required_roles: str):
    """Factory per creare dipendenze che richiedono uno dei ruoli specificati"""
    def roles_checker(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role.name not in required_roles:
            raise AuthorizationError(
                detail=f"One of roles {required_roles} required"
            )
        return current_user
    return roles_checker

# Dipendenze di ruolo pre-configurate
require_admin = require_role("admin")
require_farmer = require_role("farmer")
require_consumer = require_role("consumer")
require_restaurant_owner = require_role("restaurant_owner")
require_workshop_host = require_role("workshop_host")
require_event_organizer = require_role("event_organizer")

# Dipendenze per ruoli multipli
require_vendor_role = require_roles("farmer", "restaurant_owner", "workshop_host")
require_organizer_role = require_roles("workshop_host", "event_organizer")
