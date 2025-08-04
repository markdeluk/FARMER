from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, time
from app.db.session import get_db
from app.api.controllers.base_controller import get_current_user, require_role
from app.services import (
    product_service, product_availability_service, product_reservation_service,
    vendor_service, market_service, warehouse_service, station_booking_service,
    warehouse_spot_service
)
from app.models.user import User

router = APIRouter(prefix="/farmer", tags=["Farmer"])

# Dipendenza per verificare che l'utente sia un farmer
require_farmer_role = require_role("farmer")

# === GESTIONE PRODOTTI ===
@router.get("/my-markets")
def get_my_markets(
    current_user: User = Depends(require_farmer_role),
    db: Session = Depends(get_db)
):
    """I miei mercati"""
    vendors = vendor_service.get_vendors_by_owner(db, current_user.id)
    markets = [v for v in vendors if hasattr(v, 'market') and v.market]
    return {"markets": markets}

@router.get("/my-products")
def get_my_products(
    market_id: Optional[int] = None,
    current_user: User = Depends(require_farmer_role),
    db: Session = Depends(get_db)
):
    """I miei prodotti"""
    if market_id:
        # Verifica che il mercato appartenga all'utente
        market = market_service.get_by_id(db, market_id)
        if not market or market.vendor.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied to this market")
        
        products = product_service.get_market_products(db, market_id)
    else:
        # Tutti i prodotti di tutti i mercati dell'utente
        my_vendors = vendor_service.get_vendors_by_owner(db, current_user.id)
        my_markets = [v for v in my_vendors if hasattr(v, 'market') and v.market]
        products = []
        for market in my_markets:
            products.extend(product_service.get_market_products(db, market.id))
    
    return {"products": products}

@router.post("/products")
def create_product(
    market_id: int,
    name: str,
    description: Optional[str],
    category_id: int,
    unit_weight: float,
    unit_measure_id: int,
    current_user: User = Depends(require_farmer_role),
    db: Session = Depends(get_db)
):
    """Crea un nuovo prodotto"""
    # Verifica che il mercato appartenga all'utente
    market = market_service.get_by_id(db, market_id)
    if not market or market.vendor.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied to this market")
    
    product = product_service.create_product(
        db, market_id, name, description, category_id, unit_weight, unit_measure_id
    )
    
    return {"message": "Product created successfully", "product": product}

@router.put("/products/{product_id}")
def update_product(
    product_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    unit_weight: Optional[float] = None,
    current_user: User = Depends(require_farmer_role),
    db: Session = Depends(get_db)
):
    """Aggiorna un prodotto"""
    # Verifica proprietà
    product = product_service.get_by_id(db, product_id)
    if not product or product.market.vendor.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied to this product")
    
    update_data = {}
    if name is not None:
        update_data["name"] = name
    if description is not None:
        update_data["description"] = description
    if unit_weight is not None:
        update_data["unit_weight"] = unit_weight
    
    updated_product = product_service.update(db, product_id, **update_data)
    return {"message": "Product updated successfully", "product": updated_product}

# === GESTIONE DISPONIBILITÀ E PREZZI ===
@router.get("/products/{product_id}/availability")
def get_product_availability(
    product_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(require_farmer_role),
    db: Session = Depends(get_db)
):
    """Disponibilità di un prodotto"""
    # Verifica proprietà
    product = product_service.get_by_id(db, product_id)
    if not product or product.market.vendor.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied to this product")
    
    if start_date and end_date:
        availabilities = product_availability_service.get_product_availabilities_range(
            db, product_id, start_date, end_date
        )
    else:
        # Disponibilità di oggi
        availabilities = [product_availability_service.get_product_availability(
            db, product_id, date.today()
        )]
    
    return {"availabilities": availabilities}

@router.post("/products/{product_id}/availability")
def set_product_availability(
    product_id: int,
    availability_date: date,
    available_quantity: int,
    daily_price: float,
    discounted_price: Optional[float] = None,
    start_time_discount: Optional[time] = None,
    end_time_discount: Optional[time] = None,
    current_user: User = Depends(require_farmer_role),
    db: Session = Depends(get_db)
):
    """Imposta disponibilità e prezzo per una data"""
    # Verifica proprietà
    product = product_service.get_by_id(db, product_id)
    if not product or product.market.vendor.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied to this product")
    
    availability = product_availability_service.create_availability(
        db, product_id, availability_date, available_quantity, daily_price,
        discounted_price, start_time_discount, end_time_discount
    )
    
    if not availability:
        raise HTTPException(status_code=400, detail="Availability already exists for this date")
    
    return {"message": "Availability set successfully", "availability": availability}

@router.put("/products/{product_id}/availability/{availability_date}")
def update_product_availability(
    product_id: int,
    availability_date: date,
    available_quantity: Optional[int] = None,
    daily_price: Optional[float] = None,
    discounted_price: Optional[float] = None,
    current_user: User = Depends(require_farmer_role),
    db: Session = Depends(get_db)
):
    """Aggiorna disponibilità esistente"""
    # Verifica proprietà
    product = product_service.get_by_id(db, product_id)
    if not product or product.market.vendor.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied to this product")
    
    availability = product_availability_service.get_product_availability(db, product_id, availability_date)
    if not availability:
        raise HTTPException(status_code=404, detail="Availability not found for this date")
    
    update_data = {}
    if available_quantity is not None:
        update_data["available_quantity"] = available_quantity
    if daily_price is not None:
        update_data["daily_price"] = daily_price
    if discounted_price is not None:
        update_data["discounted_price"] = discounted_price
    
    updated_availability = product_availability_service.update(db, availability.id, **update_data)
    return {"message": "Availability updated successfully", "availability": updated_availability}

# === GESTIONE PRENOTAZIONI ===
@router.get("/reservations")
def get_product_reservations(
    product_id: Optional[int] = None,
    reservation_date: Optional[date] = None,
    current_user: User = Depends(require_farmer_role),
    db: Session = Depends(get_db)
):
    """Prenotazioni per i miei prodotti"""
    if product_id:
        # Verifica proprietà
        product = product_service.get_by_id(db, product_id)
        if not product or product.market.vendor.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied to this product")
        
        if reservation_date:
            reservations = product_reservation_service.get_product_reservations(db, product_id, reservation_date)
        else:
            # Tutte le prenotazioni per il prodotto
            reservations = product_reservation_service.filter_by(db, product_id=product_id)
    else:
        # Tutte le prenotazioni per tutti i miei prodotti
        my_products = self.get_my_products(None, current_user, db)["products"]
        reservations = []
        for product in my_products:
            reservations.extend(product_reservation_service.filter_by(db, product_id=product.id))
    
    return {"reservations": reservations}

# === GESTIONE MAGAZZINO ===
@router.get("/my-warehouses")
def get_my_warehouses(
    current_user: User = Depends(require_farmer_role),
    db: Session = Depends(get_db)
):
    """I miei magazzini"""
    vendors = vendor_service.get_vendors_by_owner(db, current_user.id)
    warehouses = [v for v in vendors if hasattr(v, 'warehouse') and v.warehouse]
    return {"warehouses": warehouses}

@router.get("/warehouse-bookings")
def get_warehouse_bookings(
    warehouse_id: Optional[int] = None,
    current_user: User = Depends(require_farmer_role),
    db: Session = Depends(get_db)
):
    """Prenotazioni nei miei magazzini"""
    if warehouse_id:
        # Verifica proprietà
        warehouse = warehouse_service.get_by_id(db, warehouse_id)
        if not warehouse or warehouse.vendor.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied to this warehouse")
        
        bookings = station_booking_service.get_warehouse_bookings(db, warehouse_id)
    else:
        # Tutti i magazzini
        my_warehouses = self.get_my_warehouses(current_user, db)["warehouses"]
        bookings = []
        for warehouse in my_warehouses:
            bookings.extend(station_booking_service.get_warehouse_bookings(db, warehouse.id))
    
    return {"bookings": bookings}

@router.get("/warehouse/{warehouse_id}/spots")
def get_warehouse_spots(
    warehouse_id: int,
    current_user: User = Depends(require_farmer_role),
    db: Session = Depends(get_db)
):
    """Spot del mio magazzino"""
    # Verifica proprietà
    warehouse = warehouse_service.get_by_id(db, warehouse_id)
    if not warehouse or warehouse.vendor.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied to this warehouse")
    
    spots = warehouse_spot_service.get_warehouse_spots(db, warehouse_id)
    return {"spots": spots}

@router.put("/warehouse/spots/{spot_id}/fee")
def update_spot_fee(
    spot_id: int,
    new_fee: float,
    current_user: User = Depends(require_farmer_role),
    db: Session = Depends(get_db)
):
    """Aggiorna la tariffa di uno spot"""
    # Verifica proprietà (attraverso warehouse)
    spot = warehouse_spot_service.get_by_id(db, spot_id)
    if not spot:
        raise HTTPException(status_code=404, detail="Spot not found")
    
    # Naviga fino al warehouse owner
    warehouse_owner_id = spot.warehouse_shelf.warehouse_row.warehouse.vendor.owner_id
    if warehouse_owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied to this spot")
    
    updated_spot = warehouse_spot_service.update_spot_fee(db, spot_id, new_fee)
    return {"message": "Spot fee updated successfully", "spot": updated_spot}

# === STATISTICS ===
@router.get("/dashboard")
def get_farmer_dashboard(
    current_user: User = Depends(require_farmer_role),
    db: Session = Depends(get_db)
):
    """Dashboard con statistiche del farmer"""
    # Prodotti totali
    my_products = self.get_my_products(None, current_user, db)["products"]
    total_products = len(my_products)
    
    # Prenotazioni oggi
    today_reservations = []
    for product in my_products:
        today_reservations.extend(
            product_reservation_service.get_product_reservations(db, product.id, date.today())
        )
    
    # Fatturato warehouse (esempio per questo mese)
    from datetime import datetime, timedelta
    start_of_month = date.today().replace(day=1)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    total_warehouse_revenue = 0.0
    my_warehouses = self.get_my_warehouses(current_user, db)["warehouses"]
    for warehouse in my_warehouses:
        revenue = station_booking_service.get_warehouse_revenue(
            db, warehouse.id, start_of_month, end_of_month
        )
        total_warehouse_revenue += revenue
    
    return {
        "total_products": total_products,
        "today_reservations": len(today_reservations),
        "monthly_warehouse_revenue": total_warehouse_revenue,
        "total_markets": len(self.get_my_markets(current_user, db)["markets"]),
        "total_warehouses": len(my_warehouses)
    }
