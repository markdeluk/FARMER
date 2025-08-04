from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, time
from app.db.session import get_db
from app.api.controllers.base_controller import get_current_user, require_role
from app.services import (
    product_service, product_availability_service, product_reservation_service,
    vendor_service, restaurant_booking_service, restaurant_seat_service,
    vendor_review_service, product_review_service, event_service, event_seat_service
)
from app.models.user import User

router = APIRouter(prefix="/consumer", tags=["Consumer"])

# Dipendenza per verificare che l'utente sia un consumer
require_consumer_role = require_role("consumer")

# === PRODOTTI E MERCATI ===
@router.get("/products")
def get_available_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
    market_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Visualizza prodotti disponibili oggi"""
    if search:
        products = product_service.search_products_by_name(db, search)
    elif category:
        products = product_service.get_products_by_category(db, category)
    elif market_id:
        products = product_service.get_available_products_today(db, market_id)
    else:
        products = product_service.get_available_products_today(db)
    
    return {"products": products}

@router.get("/products/{product_id}")
def get_product_details(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Dettagli prodotto con disponibilità e recensioni"""
    product = product_service.get_product_with_details(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Disponibilità oggi
    availability = product_availability_service.get_product_availability(db, product_id, date.today())
    
    # Recensioni
    reviews = product_review_service.get_product_reviews(db, product_id)
    avg_rating = product_review_service.get_product_average_rating(db, product_id)
    
    return {
        "product": product,
        "availability": availability,
        "reviews": reviews,
        "average_rating": avg_rating
    }

@router.post("/products/{product_id}/reserve")
def reserve_product(
    product_id: int,
    desired_quantity: int,
    reservation_date: date,
    time_slot: time,
    current_user: User = Depends(require_consumer_role),
    db: Session = Depends(get_db)
):
    """Prenota un prodotto"""
    reservation = product_reservation_service.create_reservation(
        db, current_user.id, product_id, reservation_date, time_slot, desired_quantity
    )
    
    if not reservation:
        raise HTTPException(
            status_code=400, 
            detail="Cannot create reservation - insufficient quantity or duplicate booking"
        )
    
    return {"message": "Reservation created successfully", "reservation": reservation}

@router.get("/my-reservations")
def get_my_reservations(
    current_user: User = Depends(require_consumer_role),
    db: Session = Depends(get_db)
):
    """Le mie prenotazioni prodotti"""
    reservations = product_reservation_service.get_user_reservations(db, current_user.id)
    return {"reservations": reservations}

@router.delete("/reservations/{reservation_id}")
def cancel_reservation(
    reservation_id: int,
    current_user: User = Depends(require_consumer_role),
    db: Session = Depends(get_db)
):
    """Cancella una prenotazione"""
    # Verifica che la prenotazione appartenga all'utente
    reservation = product_reservation_service.get_by_id(db, reservation_id)
    if not reservation or reservation.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    success = product_reservation_service.cancel_reservation(db, reservation_id)
    if success:
        return {"message": "Reservation cancelled successfully"}
    else:
        raise HTTPException(status_code=400, detail="Cannot cancel reservation")

# === RISTORANTI ===
@router.get("/restaurants")
def get_restaurants(
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lista ristoranti disponibili"""
    if search:
        vendors = vendor_service.search_vendors_by_name(db, search)
        # Filtra solo i ristoranti
        restaurants = [v for v in vendors if hasattr(v, 'restaurant') and v.restaurant]
    else:
        # Implementare query specifica per ristoranti
        restaurants = []  # Placeholder
    
    return {"restaurants": restaurants}

@router.get("/restaurants/{restaurant_id}/availability")
def check_restaurant_availability(
    restaurant_id: int,
    booking_date: date,
    time_slot: time,
    db: Session = Depends(get_db)
):
    """Verifica disponibilità ristorante"""
    available_seats = restaurant_seat_service.get_available_seats(db, restaurant_id, booking_date, time_slot)
    total_seats = restaurant_seat_service.get_restaurant_total_seats(db, restaurant_id)
    
    return {
        "date": booking_date,
        "time_slot": time_slot,
        "available_seats": len(available_seats),
        "total_seats": total_seats,
        "seats": available_seats
    }

@router.post("/restaurants/{restaurant_id}/book")
def book_restaurant(
    restaurant_id: int,
    seat_id: int,
    booking_date: date,
    time_slot: time,
    current_user: User = Depends(require_consumer_role),
    db: Session = Depends(get_db)
):
    """Prenota un tavolo al ristorante"""
    booking = restaurant_booking_service.create_booking(
        db, current_user.id, seat_id, booking_date, time_slot
    )
    
    if not booking:
        raise HTTPException(status_code=400, detail="Cannot create booking - seat not available")
    
    return {"message": "Restaurant booking created successfully", "booking": booking}

# === EVENTI ===
@router.get("/events")
def get_upcoming_events(
    limit: int = Query(10, le=50),
    db: Session = Depends(get_db)
):
    """Eventi in programma"""
    events = event_service.get_upcoming_events(db, limit)
    return {"events": events}

@router.get("/events/available")
def get_available_events(
    from_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Eventi con posti disponibili"""
    events = event_service.get_available_events(db, from_date)
    return {"events": events}

@router.post("/events/{event_id}/join")
def join_event(
    event_id: int,
    current_user: User = Depends(require_consumer_role),
    db: Session = Depends(get_db)
):
    """Iscriviti a un evento"""
    # Prima crea un posto per l'evento
    seat = event_seat_service.create_seat(db, event_id, current_user.id)
    if not seat:
        raise HTTPException(status_code=400, detail="Event is full or you're already registered")
    
    return {"message": "Successfully joined event", "seat": seat}

# === RECENSIONI ===
@router.post("/vendors/{vendor_id}/review")
def create_vendor_review(
    vendor_id: int,
    rating_id: int,
    comment: str,
    current_user: User = Depends(require_consumer_role),
    db: Session = Depends(get_db)
):
    """Recensisci un vendor"""
    review = vendor_review_service.create_vendor_review(
        db, current_user.id, vendor_id, rating_id, comment
    )
    
    if not review:
        raise HTTPException(status_code=400, detail="You have already reviewed this vendor")
    
    return {"message": "Review created successfully", "review": review}

@router.post("/products/{product_id}/review")
def create_product_review(
    product_id: int,
    rating_id: int,
    comment: str,
    current_user: User = Depends(require_consumer_role),
    db: Session = Depends(get_db)
):
    """Recensisci un prodotto"""
    review = product_review_service.create_product_review(
        db, current_user.id, product_id, rating_id, comment
    )
    
    if not review:
        raise HTTPException(status_code=400, detail="You have already reviewed this product")
    
    return {"message": "Review created successfully", "review": review}

@router.get("/my-reviews")
def get_my_reviews(
    current_user: User = Depends(require_consumer_role),
    db: Session = Depends(get_db)
):
    """Le mie recensioni"""
    vendor_reviews = vendor_review_service.get_user_vendor_reviews(db, current_user.id)
    product_reviews = product_review_service.get_user_product_reviews(db, current_user.id)
    
    return {
        "vendor_reviews": vendor_reviews,
        "product_reviews": product_reviews
    }
