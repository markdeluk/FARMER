from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.services.user_service import user_service
from app.models.user import User
from app.api.controllers.base_controller import get_current_user
from app.schemas import (
    UserResponse, ProfilePictureResponse, 
    ErrorResponse, SuccessResponse
)

router = APIRouter(
    prefix="/users", 
    tags=["👤 User Management"],
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "User not found"},
        422: {"model": ErrorResponse, "description": "Validation Error"}
    }
)

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Ottieni profilo utente corrente",
    description="Restituisce le informazioni del profilo dell'utente autenticato"
)
def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """Ottiene le informazioni del profilo dell'utente corrente"""
    return current_user

@router.put(
    "/me/profile-picture",
    response_model=SuccessResponse,
    summary="Aggiorna foto profilo",
    description="Carica e aggiorna la foto profilo dell'utente corrente"
)
def update_profile_picture(
    file: UploadFile = File(..., description="File immagine per la foto profilo"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    **Aggiorna la foto profilo dell'utente corrente**
    
    - Accetta file immagine (JPEG, PNG, etc.)
    - Massima dimensione: 5MB
    - Il file viene memorizzato come binary data nel database
    """
    # Validazione del tipo di file
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Il file deve essere un'immagine"
        )
    
    # Validazione della dimensione (5MB max)
    max_size = 5 * 1024 * 1024  # 5MB
    file_content = file.file.read()
    if len(file_content) > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Il file è troppo grande. Dimensione massima: 5MB"
        )
    
    # Aggiorna la foto profilo
    updated_user = user_service.update_profile_picture(
        db=db, 
        user_id=current_user.id, 
        profile_picture=file_content
    )
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utente non trovato"
        )
    
    return {"message": "Foto profilo aggiornata con successo"}

@router.get(
    "/me/profile-picture",
    response_class=Response,
    summary="Ottieni foto profilo",
    description="Restituisce la foto profilo dell'utente corrente"
)
def get_profile_picture(
    current_user: User = Depends(get_current_user)
):
    """Ottiene la foto profilo dell'utente corrente"""
    if not current_user.profile_picture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nessuna foto profilo trovata"
        )
    
    return Response(
        content=current_user.profile_picture,
        media_type="image/jpeg"  # Assumiamo JPEG come default
    )

@router.delete(
    "/me/profile-picture",
    response_model=SuccessResponse,
    summary="Rimuovi foto profilo",
    description="Rimuove la foto profilo dell'utente corrente"
)
def delete_profile_picture(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Rimuove la foto profilo dell'utente corrente"""
    updated_user = user_service.remove_profile_picture(
        db=db, 
        user_id=current_user.id
    )
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utente non trovato"
        )
    
    return {"message": "Foto profilo rimossa con successo"}

@router.get(
    "/{user_id}/profile-picture",
    response_class=Response,
    summary="Ottieni foto profilo utente",
    description="Restituisce la foto profilo di un utente specifico (pubblico)"
)
def get_user_profile_picture(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Ottiene la foto profilo di un utente specifico"""
    user = user_service.get_by_id(db=db, id=user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utente non trovato"
        )
    
    if not user.profile_picture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nessuna foto profilo trovata per questo utente"
        )
    
    return Response(
        content=user.profile_picture,
        media_type="image/jpeg"  # Assumiamo JPEG come default
    )
