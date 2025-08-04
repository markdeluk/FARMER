from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
from app.db.session import get_db
from app.api.controllers.base_controller import get_current_user, require_role
from app.services import (
    user_service, vendor_service, product_service, restaurant_booking_service,
    event_request_flow_service, station_request_flow_service, request_flow_service,
    location_service, review_service
)
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["Admin"])

# Dipendenza per verificare che l'utente sia un admin
require_admin_role = require_role("admin")

# === GESTIONE UTENTI ===
@router.get("/users")
def get_all_users(
    role: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=500),
    current_user: User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    """Lista tutti gli utenti con filtri"""
    if search:
        users = user_service.search_users_by_name(db, search)
    elif role:
        users = user_service.get_users_by_role(db, role)
    else:
        users = user_service.get_all(db, skip, limit)
    
    return {"users": users, "total": user_service.count(db)}

@router.get("/users/{user_id}")
def get_user_details(
    user_id: int,
    current_user: User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    """Dettagli completi di un utente"""
    user = user_service.get_user_with_relations(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"user": user}

@router.put("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    new_role_id: int,
    current_user: User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    """Cambia il ruolo di un utente"""
    updated_user = user_service.update_user_role(db, user_id, new_role_id)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User role updated successfully", "user": updated_user}

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    """Elimina un utente"""
    success = user_service.delete(db, user_id)
    if success:
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

# === GESTIONE VENDOR ===
@router.get("/vendors")
def get_all_vendors(
    search: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=500),
    current_user: User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    """Lista tutti i vendor"""
    if search:
        vendors = vendor_service.search_vendors_by_name(db, search)
    else:
        vendors = vendor_service.get_all(db, skip, limit)
    
    return {"vendors": vendors, "total": vendor_service.count(db)}

@router.get("/vendors/{vendor_id}")
def get_vendor_details(
    vendor_id: int,
    current_user: User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    """Dettagli completi di un vendor"""
    vendor = vendor_service.get_vendor_with_location(db, vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    
    return {"vendor": vendor}

@router.delete("/vendors/{vendor_id}")
def delete_vendor(
    vendor_id: int,
    current_user: User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    """Elimina un vendor"""
    success = vendor_service.delete(db, vendor_id)
    if success:
        return {"message": "Vendor deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Vendor not found")

# === APPROVAZIONE RICHIESTE ===
@router.get("/requests/events/pending")
def get_pending_event_requests(
    current_user: User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    """Richieste eventi in sospeso"""
    requests = event_request_flow_service.get_pending_event_requests(db)
    return {"pending_requests": requests}

@router.post("/requests/events/{request_id}/approve")
def approve_event_request(
    request_id: int,
    current_user: User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    """Approva una richiesta evento"""
    approved_request = event_request_flow_service.approve_event_request(db, request_id)
    if not approved_request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    return {"message": "Event request approved successfully", "request": approved_request}

@router.post("/requests/events/{request_id}/reject")
def reject_event_request(
    request_id: int,
    current_user: User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    """Rifiuta una richiesta evento"""
    rejected_request = event_request_flow_service.reject_event_request(db, request_id)
    if not rejected_request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    return {"message": "Event request rejected successfully", "request": rejected_request}

@router.get("/requests/stations/pending")
def get_pending_station_requests(
    current_user: User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    """Richieste stazioni in sospeso"""
    requests = station_request_flow_service.get_pending_station_requests(db)
    return {"pending_requests": requests}

@router.post("/requests/stations/{request_id}/approve")
def approve_station_request(
    request_id: int,
    current_user: User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    """Approva una richiesta stazione"""
    approved_request = station_request_flow_service.approve_station_request(db, request_id)
    if not approved_request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    return {"message": "Station request approved successfully", "request": approved_request}

@router.post("/requests/stations/{request_id}/reject")
def reject_station_request(
    request_id: int,
    current_user: User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    """Rifiuta una richiesta stazione"""
    rejected_request = station_request_flow_service.reject_station_request(db, request_id)
    if not rejected_request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    return {"message": "Station request rejected successfully", "request": rejected_request}

# === MONITORING E STATISTICHE ===
@router.get("/dashboard")
def get_admin_dashboard(
    current_user: User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    """Dashboard amministratore con statistiche generali"""
    # Statistiche utenti
    total_users = user_service.count(db)
    farmers = len(user_service.get_farmers(db))
    consumers = len(user_service.get_consumers(db))
    restaurant_owners = len(user_service.get_restaurant_owners(db))
    
    # Statistiche vendor
    total_vendors = vendor_service.count(db)
    
    # Statistiche prodotti
    total_products = product_service.count(db)
    
    # Richieste in sospeso
    pending_event_requests = len(event_request_flow_service.get_pending_event_requests(db))
    pending_station_requests = len(station_request_flow_service.get_pending_station_requests(db))
    
    # Statistiche location
    location_stats = location_service.get_location_statistics(db)
    
    return {
        "users": {
            "total": total_users,
            "farmers": farmers,
            "consumers": consumers,
            "restaurant_owners": restaurant_owners
        },
        "vendors": {
            "total": total_vendors
        },
        "products": {
            "total": total_products
        },
        "pending_requests": {
            "events": pending_event_requests,
            "stations": pending_station_requests
        },
        "locations": location_stats
    }

@router.get("/analytics/users")
def get_user_analytics(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    """Analytics sugli utenti"""
    # Distribuzione per ruolo
    role_distribution = {
        "farmers": len(user_service.get_farmers(db)),
        "consumers": len(user_service.get_consumers(db)),
        "restaurant_owners": len(user_service.get_restaurant_owners(db))
    }
    
    return {"role_distribution": role_distribution}

@router.get("/analytics/reviews")
def get_review_analytics(
    current_user: User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    """Analytics sulle recensioni"""
    recent_reviews = review_service.get_recent_reviews(db, 20)
    
    # Distribuzione rating
    rating_distribution = {}
    for review in recent_reviews:
        rating = review.rating.name
        rating_distribution[rating] = rating_distribution.get(rating, 0) + 1
    
    return {
        "recent_reviews": recent_reviews,
        "rating_distribution": rating_distribution
    }

# === GESTIONE SISTEMA ===
@router.get("/logs")
def get_system_logs(
    level: Optional[str] = None,
    limit: int = Query(100, le=1000),
    current_user: User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    """Log di sistema (placeholder)"""
    # In un'implementazione reale, questo leggerebbe i log effettivi
    return {"message": "System logs endpoint - to be implemented"}

@router.post("/maintenance/mode")
def toggle_maintenance_mode(
    enabled: bool,
    current_user: User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    """Attiva/disattiva modalità manutenzione (placeholder)"""
    # In un'implementazione reale, questo gestirebbe uno stato globale
    return {"message": f"Maintenance mode {'enabled' if enabled else 'disabled'}"}

@router.get("/system/health")
def system_health_check(
    current_user: User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    """Controllo salute del sistema"""
    # Verifica connessione database
    try:
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"
    
    return {
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "database": db_status,
        "timestamp": datetime.utcnow()
    }
