from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, time
from app.db.session import get_db
from app.api.controllers.base_controller import get_current_user, require_role
from app.services import (
    vendor_service, restaurant_service, restaurant_table_service, 
    restaurant_seat_service, menu_item_service, restaurant_booking_service
)
from app.models.user import User

router = APIRouter(prefix="/restaurant-owner", tags=["Restaurant Owner"])

# Dipendenza per verificare che l'utente sia un restaurant owner
require_restaurant_owner_role = require_role("restaurant_owner")

# === GESTIONE RISTORANTI ===
@router.get("/my-restaurants")
def get_my_restaurants(
    current_user: User = Depends(require_restaurant_owner_role),
    db: Session = Depends(get_db)
):
    """I miei ristoranti"""
    vendors = vendor_service.get_vendors_by_owner(db, current_user.id)
    restaurants = [v for v in vendors if hasattr(v, 'restaurant') and v.restaurant]
    return {"restaurants": restaurants}

# === GESTIONE TAVOLI ===
@router.get("/restaurants/{restaurant_id}/tables")
def get_restaurant_tables(
    restaurant_id: int,
    current_user: User = Depends(require_restaurant_owner_role),
    db: Session = Depends(get_db)
):
    """Tavoli del ristorante"""
    # Verifica proprietà
    restaurant = restaurant_service.get_by_id(db, restaurant_id)
    if not restaurant or restaurant.vendor.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied to this restaurant")
    
    tables = restaurant_table_service.get_restaurant_tables(db, restaurant_id)
    return {"tables": tables}

@router.post("/restaurants/{restaurant_id}/tables")
def create_table(
    restaurant_id: int,
    name: str,
    seats_count: int,
    current_user: User = Depends(require_restaurant_owner_role),
    db: Session = Depends(get_db)
):
    """Crea un nuovo tavolo"""
    # Verifica proprietà
    restaurant = restaurant_service.get_by_id(db, restaurant_id)
    if not restaurant or restaurant.vendor.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied to this restaurant")
    
    # Crea il tavolo
    table = restaurant_table_service.create_table(db, name, restaurant_id)
    
    # Crea i posti per il tavolo
    for _ in range(seats_count):
        restaurant_seat_service.create_seat(db, table.id)
    
    return {"message": "Table created successfully", "table": table}

@router.delete("/tables/{table_id}")
def delete_table(
    table_id: int,
    current_user: User = Depends(require_restaurant_owner_role),
    db: Session = Depends(get_db)
):
    """Elimina un tavolo"""
    table = restaurant_table_service.get_by_id(db, table_id)
    if not table or table.restaurant.vendor.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied to this table")
    
    success = restaurant_table_service.delete(db, table_id)
    if success:
        return {"message": "Table deleted successfully"}
    else:
        raise HTTPException(status_code=400, detail="Cannot delete table")

# === GESTIONE MENU ===
@router.get("/restaurants/{restaurant_id}/menu")
def get_restaurant_menu(
    restaurant_id: int,
    category: Optional[str] = None,
    current_user: User = Depends(require_restaurant_owner_role),
    db: Session = Depends(get_db)
):
    """Menu del ristorante"""
    # Verifica proprietà
    restaurant = restaurant_service.get_by_id(db, restaurant_id)
    if not restaurant or restaurant.vendor.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied to this restaurant")
    
    if category:
        menu_items = menu_item_service.get_menu_by_category(db, restaurant_id, category)
    else:
        menu_items = menu_item_service.get_restaurant_menu(db, restaurant_id)
    
    return {"menu_items": menu_items}

@router.post("/restaurants/{restaurant_id}/menu")
def create_menu_item(
    restaurant_id: int,
    name: str,
    price: float,
    menu_category_id: int,
    description: str,
    current_user: User = Depends(require_restaurant_owner_role),
    db: Session = Depends(get_db)
):
    """Crea una nuova voce di menu"""
    # Verifica proprietà
    restaurant = restaurant_service.get_by_id(db, restaurant_id)
    if not restaurant or restaurant.vendor.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied to this restaurant")
    
    menu_item = menu_item_service.create_menu_item(
        db, name, price, menu_category_id, description, restaurant_id
    )
    
    return {"message": "Menu item created successfully", "menu_item": menu_item}

@router.put("/menu-items/{item_id}")
def update_menu_item(
    item_id: int,
    name: Optional[str] = None,
    price: Optional[float] = None,
    description: Optional[str] = None,
    current_user: User = Depends(require_restaurant_owner_role),
    db: Session = Depends(get_db)
):
    """Aggiorna una voce di menu"""
    menu_item = menu_item_service.get_by_id(db, item_id)
    if not menu_item or menu_item.restaurant.vendor.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied to this menu item")
    
    update_data = {}
    if name is not None:
        update_data["name"] = name
    if price is not None:
        update_data["price"] = price
    if description is not None:
        update_data["description"] = description
    
    updated_item = menu_item_service.update(db, item_id, **update_data)
    return {"message": "Menu item updated successfully", "menu_item": updated_item}

@router.delete("/menu-items/{item_id}")
def delete_menu_item(
    item_id: int,
    current_user: User = Depends(require_restaurant_owner_role),
    db: Session = Depends(get_db)
):
    """Elimina una voce di menu"""
    menu_item = menu_item_service.get_by_id(db, item_id)
    if not menu_item or menu_item.restaurant.vendor.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied to this menu item")
    
    success = menu_item_service.delete(db, item_id)
    if success:
        return {"message": "Menu item deleted successfully"}
    else:
        raise HTTPException(status_code=400, detail="Cannot delete menu item")

# === GESTIONE PRENOTAZIONI ===
@router.get("/restaurants/{restaurant_id}/bookings")
def get_restaurant_bookings(
    restaurant_id: int,
    booking_date: Optional[date] = None,
    current_user: User = Depends(require_restaurant_owner_role),
    db: Session = Depends(get_db)
):
    """Prenotazioni del ristorante"""
    # Verifica proprietà
    restaurant = restaurant_service.get_by_id(db, restaurant_id)
    if not restaurant or restaurant.vendor.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied to this restaurant")
    
    if booking_date:
        bookings = restaurant_booking_service.get_restaurant_bookings_by_date(db, restaurant_id, booking_date)
    else:
        # Prenotazioni di oggi per default
        bookings = restaurant_booking_service.get_restaurant_bookings_by_date(db, restaurant_id, date.today())
    
    return {"bookings": bookings}

@router.get("/restaurants/{restaurant_id}/bookings/{booking_date}/{time_slot}")
def get_bookings_by_time_slot(
    restaurant_id: int,
    booking_date: date,
    time_slot: time,
    current_user: User = Depends(require_restaurant_owner_role),
    db: Session = Depends(get_db)
):
    """Prenotazioni per un orario specifico"""
    # Verifica proprietà
    restaurant = restaurant_service.get_by_id(db, restaurant_id)
    if not restaurant or restaurant.vendor.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied to this restaurant")
    
    bookings = restaurant_booking_service.get_bookings_by_time_slot(db, restaurant_id, booking_date, time_slot)
    return {"bookings": bookings}

@router.get("/restaurants/{restaurant_id}/availability/{booking_date}")
def get_daily_availability(
    restaurant_id: int,
    booking_date: date,
    current_user: User = Depends(require_restaurant_owner_role),
    db: Session = Depends(get_db)
):
    """Disponibilità del ristorante per una data"""
    # Verifica proprietà
    restaurant = restaurant_service.get_by_id(db, restaurant_id)
    if not restaurant or restaurant.vendor.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied to this restaurant")
    
    total_seats = restaurant_seat_service.get_restaurant_total_seats(db, restaurant_id)
    occupancy_rate = restaurant_booking_service.get_restaurant_occupancy_rate(db, restaurant_id, booking_date)
    
    # Prenotazioni per orari specifici (esempio: 19:00, 20:00, 21:00)
    time_slots = [time(19, 0), time(20, 0), time(21, 0)]
    availability_by_time = {}
    
    for slot in time_slots:
        available_seats = restaurant_seat_service.get_available_seats(db, restaurant_id, booking_date, slot)
        availability_by_time[str(slot)] = {
            "available_seats": len(available_seats),
            "booked_seats": total_seats - len(available_seats)
        }
    
    return {
        "date": booking_date,
        "total_seats": total_seats,
        "occupancy_rate": occupancy_rate,
        "availability_by_time": availability_by_time
    }

# === DASHBOARD E STATISTICHE ===
@router.get("/dashboard")
def get_restaurant_owner_dashboard(
    current_user: User = Depends(require_restaurant_owner_role),
    db: Session = Depends(get_db)
):
    """Dashboard del proprietario di ristorante"""
    # I miei ristoranti
    vendors = vendor_service.get_vendors_by_owner(db, current_user.id)
    restaurants = [v for v in vendors if hasattr(v, 'restaurant') and v.restaurant]
    
    # Statistiche aggregate
    total_tables = 0
    total_seats = 0
    today_bookings = 0
    total_menu_items = 0
    
    for restaurant_vendor in restaurants:
        restaurant = restaurant_vendor.restaurant
        
        # Tavoli e posti
        tables = restaurant_table_service.get_restaurant_tables(db, restaurant.id)
        total_tables += len(tables)
        total_seats += restaurant_seat_service.get_restaurant_total_seats(db, restaurant.id)
        
        # Prenotazioni oggi
        today_bookings += len(restaurant_booking_service.get_restaurant_bookings_by_date(
            db, restaurant.id, date.today()
        ))
        
        # Voci di menu
        menu_items = menu_item_service.get_restaurant_menu(db, restaurant.id)
        total_menu_items += len(menu_items)
    
    return {
        "total_restaurants": len(restaurants),
        "total_tables": total_tables,
        "total_seats": total_seats,
        "today_bookings": today_bookings,
        "total_menu_items": total_menu_items,
        "restaurants": restaurants
    }

# === ORARI DI APERTURA ===
@router.get("/restaurants/{restaurant_id}/opening-hours")
def get_opening_hours(
    restaurant_id: int,
    current_user: User = Depends(require_restaurant_owner_role),
    db: Session = Depends(get_db)
):
    """Orari di apertura del ristorante"""
    # Verifica proprietà
    restaurant = restaurant_service.get_by_id(db, restaurant_id)
    if not restaurant or restaurant.vendor.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied to this restaurant")
    
    # Gli orari sono gestiti tramite vendor
    from app.services import opening_hour_service
    opening_hours = opening_hour_service.get_vendor_opening_hours(db, restaurant_id)
    
    return {"opening_hours": opening_hours}
