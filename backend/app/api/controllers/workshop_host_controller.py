from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
from app.db.session import get_db
from app.api.controllers.base_controller import get_current_user, require_role
from app.services import (
    activity_service, vendor_service, product_service, 
    location_service, user_service, event_request_flow_service
)
from app.models.user import User

router = APIRouter(prefix="/workshop-host", tags=["Workshop Host"])

# Dipendenza per verificare che l'utente sia un workshop host
require_workshop_host_role = require_role("workshop_host")

# === GESTIONE ATTIVITÀ/WORKSHOP ===
@router.get("/activities")
def get_my_activities(
    current_user: User = Depends(require_workshop_host_role),
    db: Session = Depends(get_db)
):
    """Le mie attività/workshop"""
    activities = activity_service.get_activities_by_host(db, current_user.id)
    return {"activities": activities}

@router.get("/activities/{activity_id}")
def get_activity_details(
    activity_id: int,
    current_user: User = Depends(require_workshop_host_role),
    db: Session = Depends(get_db)
):
    """Dettagli di una mia attività"""
    activity = activity_service.get_activity_with_bookings(db, activity_id)
    if not activity or activity.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    return {"activity": activity}

@router.post("/activities")
def create_activity(
    activity_data: dict,
    current_user: User = Depends(require_workshop_host_role),
    db: Session = Depends(get_db)
):
    """Crea una nuova attività/workshop"""
    activity_data["owner_id"] = current_user.id
    activity = activity_service.create(db, activity_data)
    return {"message": "Activity created successfully", "activity": activity}

@router.put("/activities/{activity_id}")
def update_activity(
    activity_id: int,
    activity_data: dict,
    current_user: User = Depends(require_workshop_host_role),
    db: Session = Depends(get_db)
):
    """Aggiorna una mia attività"""
    # Verifica proprietà
    activity = activity_service.get(db, activity_id)
    if not activity or activity.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    updated_activity = activity_service.update(db, activity_id, activity_data)
    return {"message": "Activity updated successfully", "activity": updated_activity}

@router.delete("/activities/{activity_id}")
def delete_activity(
    activity_id: int,
    current_user: User = Depends(require_workshop_host_role),
    db: Session = Depends(get_db)
):
    """Elimina una mia attività"""
    # Verifica proprietà
    activity = activity_service.get(db, activity_id)
    if not activity or activity.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    success = activity_service.delete(db, activity_id)
    if success:
        return {"message": "Activity deleted successfully"}
    else:
        raise HTTPException(status_code=400, detail="Could not delete activity")

# === GESTIONE PRENOTAZIONI WORKSHOP ===
@router.get("/activities/{activity_id}/bookings")
def get_activity_bookings(
    activity_id: int,
    status: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    current_user: User = Depends(require_workshop_host_role),
    db: Session = Depends(get_db)
):
    """Prenotazioni per una mia attività"""
    # Verifica proprietà
    activity = activity_service.get(db, activity_id)
    if not activity or activity.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    bookings = activity_service.get_activity_bookings_filtered(
        db, activity_id, status, date_from, date_to
    )
    return {"bookings": bookings}

@router.post("/activities/{activity_id}/bookings/{booking_id}/confirm")
def confirm_booking(
    activity_id: int,
    booking_id: int,
    current_user: User = Depends(require_workshop_host_role),
    db: Session = Depends(get_db)
):
    """Conferma una prenotazione"""
    # Verifica proprietà attività
    activity = activity_service.get(db, activity_id)
    if not activity or activity.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    booking = activity_service.confirm_activity_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    return {"message": "Booking confirmed successfully", "booking": booking}

@router.post("/activities/{activity_id}/bookings/{booking_id}/cancel")
def cancel_booking(
    activity_id: int,
    booking_id: int,
    current_user: User = Depends(require_workshop_host_role),
    db: Session = Depends(get_db)
):
    """Cancella una prenotazione"""
    # Verifica proprietà attività
    activity = activity_service.get(db, activity_id)
    if not activity or activity.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    booking = activity_service.cancel_activity_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    return {"message": "Booking cancelled successfully", "booking": booking}

# === GESTIONE SESSIONI/ORARI ===
@router.get("/activities/{activity_id}/sessions")
def get_activity_sessions(
    activity_id: int,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    current_user: User = Depends(require_workshop_host_role),
    db: Session = Depends(get_db)
):
    """Sessioni/orari di una mia attività"""
    # Verifica proprietà
    activity = activity_service.get(db, activity_id)
    if not activity or activity.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    sessions = activity_service.get_activity_sessions_in_period(
        db, activity_id, date_from, date_to
    )
    return {"sessions": sessions}

@router.post("/activities/{activity_id}/sessions")
def create_activity_session(
    activity_id: int,
    session_data: dict,
    current_user: User = Depends(require_workshop_host_role),
    db: Session = Depends(get_db)
):
    """Crea una nuova sessione per l'attività"""
    # Verifica proprietà
    activity = activity_service.get(db, activity_id)
    if not activity or activity.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    session_data["activity_id"] = activity_id
    session = activity_service.create_activity_session(db, session_data)
    return {"message": "Session created successfully", "session": session}

@router.put("/activities/{activity_id}/sessions/{session_id}")
def update_activity_session(
    activity_id: int,
    session_id: int,
    session_data: dict,
    current_user: User = Depends(require_workshop_host_role),
    db: Session = Depends(get_db)
):
    """Aggiorna una sessione dell'attività"""
    # Verifica proprietà
    activity = activity_service.get(db, activity_id)
    if not activity or activity.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    session = activity_service.update_activity_session(db, session_id, session_data)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"message": "Session updated successfully", "session": session}

@router.delete("/activities/{activity_id}/sessions/{session_id}")
def delete_activity_session(
    activity_id: int,
    session_id: int,
    current_user: User = Depends(require_workshop_host_role),
    db: Session = Depends(get_db)
):
    """Elimina una sessione dell'attività"""
    # Verifica proprietà
    activity = activity_service.get(db, activity_id)
    if not activity or activity.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    success = activity_service.delete_activity_session(db, session_id)
    if success:
        return {"message": "Session deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")

# === MATERIALI E RISORSE ===
@router.get("/activities/{activity_id}/materials")
def get_activity_materials(
    activity_id: int,
    current_user: User = Depends(require_workshop_host_role),
    db: Session = Depends(get_db)
):
    """Materiali necessari per l'attività"""
    # Verifica proprietà
    activity = activity_service.get(db, activity_id)
    if not activity or activity.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    materials = activity_service.get_activity_materials(db, activity_id)
    return {"materials": materials}

@router.post("/activities/{activity_id}/materials")
def add_activity_material(
    activity_id: int,
    material_data: dict,
    current_user: User = Depends(require_workshop_host_role),
    db: Session = Depends(get_db)
):
    """Aggiungi materiale all'attività"""
    # Verifica proprietà
    activity = activity_service.get(db, activity_id)
    if not activity or activity.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    material_data["activity_id"] = activity_id
    material = activity_service.add_activity_material(db, material_data)
    return {"message": "Material added successfully", "material": material}

# === DASHBOARD E STATISTICHE ===
@router.get("/dashboard")
def get_workshop_host_dashboard(
    current_user: User = Depends(require_workshop_host_role),
    db: Session = Depends(get_db)
):
    """Dashboard workshop host"""
    # Statistiche attività
    my_activities = activity_service.get_activities_by_host(db, current_user.id)
    total_activities = len(my_activities)
    
    # Prenotazioni recenti
    recent_bookings = activity_service.get_recent_bookings_for_host(db, current_user.id, 10)
    
    # Prossime sessioni
    upcoming_sessions = activity_service.get_upcoming_sessions_for_host(db, current_user.id, 5)
    
    # Statistiche mensili
    monthly_stats = activity_service.get_monthly_stats_for_host(db, current_user.id)
    
    return {
        "activities": {
            "total": total_activities,
            "list": my_activities
        },
        "recent_bookings": recent_bookings,
        "upcoming_sessions": upcoming_sessions,
        "monthly_stats": monthly_stats
    }

@router.get("/analytics/bookings")
def get_booking_analytics(
    period: str = Query("month", regex="^(week|month|quarter|year)$"),
    current_user: User = Depends(require_workshop_host_role),
    db: Session = Depends(get_db)
):
    """Analytics sulle prenotazioni"""
    analytics = activity_service.get_booking_analytics_for_host(
        db, current_user.id, period
    )
    
    return {"analytics": analytics, "period": period}

@router.get("/analytics/participants")
def get_participant_analytics(
    current_user: User = Depends(require_workshop_host_role),
    db: Session = Depends(get_db)
):
    """Analytics sui partecipanti"""
    participant_stats = activity_service.get_participant_analytics_for_host(
        db, current_user.id
    )
    
    return {"participant_analytics": participant_stats}

# === COMUNICAZIONE ===
@router.post("/activities/{activity_id}/notify-participants")
def notify_participants(
    activity_id: int,
    message: str,
    current_user: User = Depends(require_workshop_host_role),
    db: Session = Depends(get_db)
):
    """Invia notifica ai partecipanti di un'attività"""
    # Verifica proprietà
    activity = activity_service.get(db, activity_id)
    if not activity or activity.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # In un'implementazione reale, questo invierebbe notifiche effettive
    participants = activity_service.get_activity_participants(db, activity_id)
    
    return {
        "message": "Notifications sent successfully",
        "participants_notified": len(participants)
    }
