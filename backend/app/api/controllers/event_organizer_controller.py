from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
from app.db.session import get_db
from app.api.controllers.base_controller import get_current_user, require_role
from app.services import (
    event_request_flow_service, location_service, vendor_service,
    user_service, product_service
)
from app.models.user import User

router = APIRouter(prefix="/event-organizer", tags=["Event Organizer"])

# Dipendenza per verificare che l'utente sia un event organizer
require_event_organizer_role = require_role("event_organizer")

# === GESTIONE RICHIESTE EVENTI ===
@router.get("/requests")
def get_my_event_requests(
    status: Optional[str] = None,
    current_user: User = Depends(require_event_organizer_role),
    db: Session = Depends(get_db)
):
    """Le mie richieste eventi"""
    requests = event_request_flow_service.get_requests_by_organizer(
        db, current_user.id, status
    )
    return {"requests": requests}

@router.get("/requests/{request_id}")
def get_event_request_details(
    request_id: int,
    current_user: User = Depends(require_event_organizer_role),
    db: Session = Depends(get_db)
):
    """Dettagli di una mia richiesta evento"""
    request = event_request_flow_service.get_request_with_details(db, request_id)
    if not request or request.organizer_id != current_user.id:
        raise HTTPException(status_code=404, detail="Request not found")
    
    return {"request": request}

@router.post("/requests")
def create_event_request(
    request_data: dict,
    current_user: User = Depends(require_event_organizer_role),
    db: Session = Depends(get_db)
):
    """Crea una nuova richiesta evento"""
    request_data["organizer_id"] = current_user.id
    request_data["status"] = "pending"
    
    event_request = event_request_flow_service.create_event_request(db, request_data)
    return {"message": "Event request created successfully", "request": event_request}

@router.put("/requests/{request_id}")
def update_event_request(
    request_id: int,
    request_data: dict,
    current_user: User = Depends(require_event_organizer_role),
    db: Session = Depends(get_db)
):
    """Aggiorna una mia richiesta evento (solo se in pending)"""
    # Verifica proprietà e stato
    request = event_request_flow_service.get(db, request_id)
    if not request or request.organizer_id != current_user.id:
        raise HTTPException(status_code=404, detail="Request not found")
    
    if request.status != "pending":
        raise HTTPException(
            status_code=400, 
            detail="Can only update pending requests"
        )
    
    updated_request = event_request_flow_service.update(db, request_id, request_data)
    return {"message": "Request updated successfully", "request": updated_request}

@router.delete("/requests/{request_id}")
def delete_event_request(
    request_id: int,
    current_user: User = Depends(require_event_organizer_role),
    db: Session = Depends(get_db)
):
    """Elimina una mia richiesta evento (solo se in pending)"""
    # Verifica proprietà e stato
    request = event_request_flow_service.get(db, request_id)
    if not request or request.organizer_id != current_user.id:
        raise HTTPException(status_code=404, detail="Request not found")
    
    if request.status != "pending":
        raise HTTPException(
            status_code=400, 
            detail="Can only delete pending requests"
        )
    
    success = event_request_flow_service.delete(db, request_id)
    if success:
        return {"message": "Request deleted successfully"}
    else:
        raise HTTPException(status_code=400, detail="Could not delete request")

# === LOCATION E VENUE ===
@router.get("/locations")
def search_available_locations(
    city: Optional[str] = None,
    min_capacity: Optional[int] = None,
    event_date: Optional[date] = None,
    current_user: User = Depends(require_event_organizer_role),
    db: Session = Depends(get_db)
):
    """Cerca location disponibili per eventi"""
    locations = location_service.search_available_event_locations(
        db, city, min_capacity, event_date
    )
    return {"locations": locations}

@router.get("/locations/{location_id}")
def get_location_details(
    location_id: int,
    current_user: User = Depends(require_event_organizer_role),
    db: Session = Depends(get_db)
):
    """Dettagli di una location"""
    location = location_service.get_location_with_availability(db, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    return {"location": location}

@router.post("/locations/{location_id}/reserve")
def reserve_location(
    location_id: int,
    reservation_data: dict,
    current_user: User = Depends(require_event_organizer_role),
    db: Session = Depends(get_db)
):
    """Prenota una location per un evento"""
    reservation_data["organizer_id"] = current_user.id
    reservation_data["location_id"] = location_id
    
    reservation = location_service.create_location_reservation(db, reservation_data)
    if not reservation:
        raise HTTPException(
            status_code=400, 
            detail="Location not available for the requested dates"
        )
    
    return {"message": "Location reserved successfully", "reservation": reservation}

# === GESTIONE VENDOR PER EVENTI ===
@router.get("/vendors")
def search_event_vendors(
    location_id: Optional[int] = None,
    vendor_type: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(require_event_organizer_role),
    db: Session = Depends(get_db)
):
    """Cerca vendor per eventi"""
    if location_id:
        vendors = vendor_service.get_vendors_near_location(db, location_id)
    elif vendor_type:
        vendors = vendor_service.get_vendors_by_type(db, vendor_type)
    elif search:
        vendors = vendor_service.search_vendors_by_name(db, search)
    else:
        vendors = vendor_service.get_all(db, 0, 50)
    
    return {"vendors": vendors}

@router.post("/vendors/{vendor_id}/contact")
def contact_vendor(
    vendor_id: int,
    message: str,
    event_date: date,
    current_user: User = Depends(require_event_organizer_role),
    db: Session = Depends(get_db)
):
    """Contatta un vendor per un evento"""
    vendor = vendor_service.get(db, vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    
    # In un'implementazione reale, questo invierebbe un messaggio effettivo
    contact_record = vendor_service.create_vendor_contact(
        db, vendor_id, current_user.id, message, event_date
    )
    
    return {
        "message": "Vendor contacted successfully",
        "contact": contact_record
    }

# === GESTIONE PARTECIPANTI ===
@router.get("/requests/{request_id}/participants")
def get_event_participants(
    request_id: int,
    current_user: User = Depends(require_event_organizer_role),
    db: Session = Depends(get_db)
):
    """Partecipanti registrati all'evento"""
    # Verifica proprietà
    request = event_request_flow_service.get(db, request_id)
    if not request or request.organizer_id != current_user.id:
        raise HTTPException(status_code=404, detail="Request not found")
    
    participants = event_request_flow_service.get_event_participants(db, request_id)
    return {"participants": participants}

@router.post("/requests/{request_id}/participants/{user_id}/approve")
def approve_participant(
    request_id: int,
    user_id: int,
    current_user: User = Depends(require_event_organizer_role),
    db: Session = Depends(get_db)
):
    """Approva un partecipante all'evento"""
    # Verifica proprietà
    request = event_request_flow_service.get(db, request_id)
    if not request or request.organizer_id != current_user.id:
        raise HTTPException(status_code=404, detail="Request not found")
    
    participant = event_request_flow_service.approve_event_participant(
        db, request_id, user_id
    )
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    
    return {"message": "Participant approved successfully", "participant": participant}

# === MATERIALI E FORNITURE ===
@router.get("/requests/{request_id}/supplies")
def get_event_supplies(
    request_id: int,
    current_user: User = Depends(require_event_organizer_role),
    db: Session = Depends(get_db)
):
    """Forniture necessarie per l'evento"""
    # Verifica proprietà
    request = event_request_flow_service.get(db, request_id)
    if not request or request.organizer_id != current_user.id:
        raise HTTPException(status_code=404, detail="Request not found")
    
    supplies = event_request_flow_service.get_event_supplies(db, request_id)
    return {"supplies": supplies}

@router.post("/requests/{request_id}/supplies")
def add_event_supply(
    request_id: int,
    supply_data: dict,
    current_user: User = Depends(require_event_organizer_role),
    db: Session = Depends(get_db)
):
    """Aggiungi fornitura all'evento"""
    # Verifica proprietà
    request = event_request_flow_service.get(db, request_id)
    if not request or request.organizer_id != current_user.id:
        raise HTTPException(status_code=404, detail="Request not found")
    
    supply_data["event_request_id"] = request_id
    supply = event_request_flow_service.add_event_supply(db, supply_data)
    return {"message": "Supply added successfully", "supply": supply}

@router.get("/supplies/products")
def search_supply_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(require_event_organizer_role),
    db: Session = Depends(get_db)
):
    """Cerca prodotti per forniture eventi"""
    if category:
        products = product_service.get_products_by_category(db, category)
    elif search:
        products = product_service.search_products(db, search)
    else:
        products = product_service.get_all(db, 0, 50)
    
    return {"products": products}

# === DASHBOARD E STATISTICHE ===
@router.get("/dashboard")
def get_event_organizer_dashboard(
    current_user: User = Depends(require_event_organizer_role),
    db: Session = Depends(get_db)
):
    """Dashboard event organizer"""
    # Statistiche richieste
    my_requests = event_request_flow_service.get_requests_by_organizer(
        db, current_user.id
    )
    
    requests_by_status = {}
    for request in my_requests:
        status = request.status
        requests_by_status[status] = requests_by_status.get(status, 0) + 1
    
    # Prossimi eventi
    upcoming_events = event_request_flow_service.get_upcoming_events_for_organizer(
        db, current_user.id, 5
    )
    
    # Eventi recenti
    recent_events = event_request_flow_service.get_recent_events_for_organizer(
        db, current_user.id, 5
    )
    
    return {
        "requests": {
            "total": len(my_requests),
            "by_status": requests_by_status
        },
        "upcoming_events": upcoming_events,
        "recent_events": recent_events
    }

@router.get("/analytics/events")
def get_event_analytics(
    period: str = Query("month", regex="^(week|month|quarter|year)$"),
    current_user: User = Depends(require_event_organizer_role),
    db: Session = Depends(get_db)
):
    """Analytics sugli eventi organizzati"""
    analytics = event_request_flow_service.get_event_analytics_for_organizer(
        db, current_user.id, period
    )
    
    return {"analytics": analytics, "period": period}

@router.get("/analytics/locations")
def get_location_usage_analytics(
    current_user: User = Depends(require_event_organizer_role),
    db: Session = Depends(get_db)
):
    """Analytics sull'utilizzo delle location"""
    location_stats = event_request_flow_service.get_location_usage_for_organizer(
        db, current_user.id
    )
    
    return {"location_analytics": location_stats}

# === COMUNICAZIONE ===
@router.post("/requests/{request_id}/notify-participants")
def notify_event_participants(
    request_id: int,
    message: str,
    current_user: User = Depends(require_event_organizer_role),
    db: Session = Depends(get_db)
):
    """Invia notifica ai partecipanti dell'evento"""
    # Verifica proprietà
    request = event_request_flow_service.get(db, request_id)
    if not request or request.organizer_id != current_user.id:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # In un'implementazione reale, questo invierebbe notifiche effettive
    participants = event_request_flow_service.get_event_participants(db, request_id)
    
    return {
        "message": "Notifications sent successfully",
        "participants_notified": len(participants)
    }

@router.post("/requests/{request_id}/announcements")
def create_event_announcement(
    request_id: int,
    announcement_data: dict,
    current_user: User = Depends(require_event_organizer_role),
    db: Session = Depends(get_db)
):
    """Crea un annuncio per l'evento"""
    # Verifica proprietà
    request = event_request_flow_service.get(db, request_id)
    if not request or request.organizer_id != current_user.id:
        raise HTTPException(status_code=404, detail="Request not found")
    
    announcement_data["event_request_id"] = request_id
    announcement_data["organizer_id"] = current_user.id
    
    announcement = event_request_flow_service.create_event_announcement(
        db, announcement_data
    )
    
    return {"message": "Announcement created successfully", "announcement": announcement}
