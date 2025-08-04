from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.auth import (
    authenticate_user, create_access_token, get_current_active_user,
    get_password_hash
)
from app.core.config import settings
from app.services.user_service import UserService
from app.models.user import User
from app.schemas import (
    UserLogin, UserRegister, UserResponse, Token, 
    ErrorResponse, SuccessResponse
)

router = APIRouter(
    prefix="/auth", 
    tags=["🔐 Authentication"],
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        422: {"model": ErrorResponse, "description": "Validation Error"}
    }
)

user_service = UserService()

@router.post(
    "/register", 
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registra nuovo utente",
    description="Crea un nuovo account utente nella piattaforma",
    responses={
        201: {"description": "Utente creato con successo"},
        400: {"description": "Email già in uso"}
    }
)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    **Registra un nuovo utente**
    
    Crea un nuovo account utente con i seguenti passi:
    1. Verifica che l'email non sia già utilizzata
    2. Hash sicuro della password
    3. Creazione dell'utente nel database
    4. Ritorna i dati dell'utente (senza password)
    
    **Ruoli disponibili:**
    - 1: admin
    - 2: farmer  
    - 3: consumer
    - 4: restaurant_owner
    - 5: workshop_host
    - 6: event_organizer
    """
    # Verifica se l'utente esiste già
    existing_user = user_service.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash della password
    hashed_password = get_password_hash(user_data.password)
    
    # Crea l'utente usando il metodo corretto
    new_user = user_service.create_user(
        db=db,
        email=user_data.email,
        password_hash=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone=user_data.phone,
        role_type_id=user_data.role_id,
        profile_picture=user_data.profile_picture
    )
    
    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        phone=new_user.phone,
        is_active=new_user.is_active,
        role_name=new_user.role_type.name,
        profile_picture=new_user.profile_picture
    )

@router.post(
    "/login", 
    response_model=Token,
    summary="Login utente",
    description="Autentica un utente e restituisce il token JWT",
    responses={
        200: {"description": "Login effettuato con successo"},
        401: {"description": "Credenziali non valide"}
    }
)
def login(
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    **Effettua il login**
    
    Autentica l'utente e restituisce:
    - Token JWT con scadenza (30 minuti)
    - Informazioni utente
    - Tipo di token (bearer)
    
    **Utilizzare il token negli header:**
    ```
    Authorization: Bearer <access_token>
    ```
    """
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crea token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # in secondi
        user=UserResponse(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            is_active=user.is_active,
            role_name=user.role.name
        )
    )

@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """Informazioni utente corrente"""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        phone=current_user.phone,
        is_active=current_user.is_active,
        role_name=current_user.role.name
    )

@router.post("/refresh", response_model=Token)
def refresh_token(
    current_user: User = Depends(get_current_active_user)
):
    """Rinnova il token di accesso"""
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(current_user.id)}, expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse(
            id=current_user.id,
            email=current_user.email,
            first_name=current_user.first_name,
            last_name=current_user.last_name,
            phone=current_user.phone,
            is_active=current_user.is_active,
            role_name=current_user.role.name
        )
    )

@router.post("/logout")
def logout():
    """Logout utente (placeholder)"""
    # In un'implementazione reale, si potrebbe gestire una blacklist di token
    return {"message": "Successfully logged out"}

@router.get("/roles")
def get_available_roles(db: Session = Depends(get_db)):
    """Lista dei ruoli disponibili per la registrazione"""
    roles = user_service.get_all_roles(db)
    return {"roles": [{"id": role.id, "name": role.name} for role in roles]}

# Endpoint di test per verificare i ruoli
@router.get("/test/admin")
def test_admin_access(
    current_user: User = Depends(get_current_active_user)
):
    """Test accesso admin"""
    if current_user.role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required"
        )
    return {"message": "Admin access granted", "user": current_user.email}

@router.get("/test/farmer")
def test_farmer_access(
    current_user: User = Depends(get_current_active_user)
):
    """Test accesso farmer"""
    if current_user.role.name != "farmer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Farmer role required"
        )
    return {"message": "Farmer access granted", "user": current_user.email}
