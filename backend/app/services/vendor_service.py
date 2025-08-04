from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.vendor import Vendor, OpeningHour, Market, Restaurant, Activity, Warehouse
from app.models.location import Location
from app.models.enums import DayWeek
from app.services.base_service import BaseService

class VendorService(BaseService[Vendor]):
    """Servizio per operazioni CRUD su Vendor"""
    
    def __init__(self):
        super().__init__(Vendor)
    
    def create_vendor(self, db: Session, name: str, description: str, location_id: int, owner_id: int) -> Vendor:
        """Crea un nuovo vendor"""
        return self.create(
            db, 
            name=name, 
            description=description, 
            location_id=location_id, 
            owner_id=owner_id
        )
    
    def get_vendor_with_location(self, db: Session, vendor_id: int) -> Optional[Vendor]:
        """Recupera un vendor con la sua location"""
        return db.query(Vendor).options(
            joinedload(Vendor.location),
            joinedload(Vendor.owner)
        ).filter(Vendor.id == vendor_id).first()
    
    def get_vendors_by_owner(self, db: Session, owner_id: int) -> List[Vendor]:
        """Recupera tutti i vendor di un proprietario"""
        return self.filter_by(db, owner_id=owner_id)
    
    def get_vendors_by_location(self, db: Session, location_id: int) -> List[Vendor]:
        """Recupera tutti i vendor in una location"""
        return self.filter_by(db, location_id=location_id)
    
    def search_vendors_by_name(self, db: Session, search_term: str) -> List[Vendor]:
        """Cerca vendor per nome"""
        return db.query(Vendor).filter(
            Vendor.name.ilike(f"%{search_term}%")
        ).all()
    
    def get_vendors_near_location(self, db: Session, lat: float, lon: float, radius_km: float = 10.0) -> List[Vendor]:
        """Recupera vendor vicini a una coordinata (semplificato)"""
        # Formula haversine semplificata per esempio
        lat_diff = radius_km / 111.0  # 1 grado ≈ 111 km
        lon_diff = radius_km / (111.0 * abs(lat))
        
        return db.query(Vendor).join(Location).filter(
            Location.lat.between(lat - lat_diff, lat + lat_diff),
            Location.lon.between(lon - lon_diff, lon + lon_diff)
        ).all()

class OpeningHourService(BaseService[OpeningHour]):
    """Servizio per operazioni CRUD su OpeningHour"""
    
    def __init__(self):
        super().__init__(OpeningHour)
    
    def create_opening_hour(self, db: Session, vendor_id: int, day_week_id: int, start_time, end_time) -> OpeningHour:
        """Crea un nuovo orario di apertura"""
        return self.create(
            db,
            vendor_id=vendor_id,
            day_week_id=day_week_id,
            start_time=start_time,
            end_time=end_time
        )
    
    def get_vendor_opening_hours(self, db: Session, vendor_id: int) -> List[OpeningHour]:
        """Recupera tutti gli orari di apertura di un vendor"""
        return db.query(OpeningHour).options(
            joinedload(OpeningHour.day_week)
        ).filter(OpeningHour.vendor_id == vendor_id).all()
    
    def get_opening_hours_by_day(self, db: Session, vendor_id: int, day_name: str) -> List[OpeningHour]:
        """Recupera gli orari di apertura per un giorno specifico"""
        return db.query(OpeningHour).join(DayWeek).filter(
            OpeningHour.vendor_id == vendor_id,
            DayWeek.name == day_name
        ).all()
    
    def is_vendor_open(self, db: Session, vendor_id: int, day_name: str, time) -> bool:
        """Verifica se un vendor è aperto in un momento specifico"""
        opening_hours = self.get_opening_hours_by_day(db, vendor_id, day_name)
        for oh in opening_hours:
            if oh.start_time <= time <= oh.end_time:
                return True
        return False

class MarketService(BaseService[Market]):
    """Servizio per operazioni CRUD su Market"""
    
    def __init__(self):
        super().__init__(Market)
    
    def create_market(self, db: Session, vendor_id: int) -> Market:
        """Crea un nuovo mercato"""
        return self.create(db, id=vendor_id)
    
    def get_market_with_products(self, db: Session, market_id: int) -> Optional[Market]:
        """Recupera un mercato con i suoi prodotti"""
        return db.query(Market).options(
            joinedload(Market.products)
        ).filter(Market.id == market_id).first()

class RestaurantService(BaseService[Restaurant]):
    """Servizio per operazioni CRUD su Restaurant"""
    
    def __init__(self):
        super().__init__(Restaurant)
    
    def create_restaurant(self, db: Session, vendor_id: int) -> Restaurant:
        """Crea un nuovo ristorante"""
        return self.create(db, id=vendor_id)
    
    def get_restaurant_with_tables(self, db: Session, restaurant_id: int) -> Optional[Restaurant]:
        """Recupera un ristorante con i suoi tavoli"""
        return db.query(Restaurant).options(
            joinedload(Restaurant.tables)
        ).filter(Restaurant.id == restaurant_id).first()

class ActivityService(BaseService[Activity]):
    """Servizio per operazioni CRUD su Activity"""
    
    def __init__(self):
        super().__init__(Activity)
    
    def create_activity(self, db: Session, vendor_id: int, capacity: int, start_time, end_time) -> Activity:
        """Crea una nuova attività"""
        return self.create(
            db,
            id=vendor_id,
            capacity=capacity,
            start_time=start_time,
            end_time=end_time
        )

class WarehouseService(BaseService[Warehouse]):
    """Servizio per operazioni CRUD su Warehouse"""
    
    def __init__(self):
        super().__init__(Warehouse)
    
    def create_warehouse(self, db: Session, vendor_id: int) -> Warehouse:
        """Crea un nuovo magazzino"""
        return self.create(db, id=vendor_id)
    
    def get_warehouse_with_structure(self, db: Session, warehouse_id: int) -> Optional[Warehouse]:
        """Recupera un magazzino con la sua struttura"""
        return db.query(Warehouse).options(
            joinedload(Warehouse.warehouse_rows)
        ).filter(Warehouse.id == warehouse_id).first()

# Istanze globali dei servizi
vendor_service = VendorService()
opening_hour_service = OpeningHourService()
market_service = MarketService()
restaurant_service = RestaurantService()
activity_service = ActivityService()
warehouse_service = WarehouseService()
