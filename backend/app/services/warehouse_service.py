from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_, func
from app.models.warehouse import WarehouseRow, WarehouseShelf, WarehouseSpot, StationBooking
from app.models.enums import CropType
from app.services.base_service import BaseService

class WarehouseRowService(BaseService[WarehouseRow]):
    """Servizio per operazioni CRUD su WarehouseRow"""
    
    def __init__(self):
        super().__init__(WarehouseRow)
    
    def create_row(self, db: Session, warehouse_id: int) -> WarehouseRow:
        """Crea una nuova fila del magazzino"""
        return self.create(db, warehouse_id=warehouse_id)
    
    def get_warehouse_rows(self, db: Session, warehouse_id: int) -> List[WarehouseRow]:
        """Recupera tutte le file di un magazzino"""
        return db.query(WarehouseRow).options(
            joinedload(WarehouseRow.shelves)
        ).filter(WarehouseRow.warehouse_id == warehouse_id).all()

class WarehouseShelfService(BaseService[WarehouseShelf]):
    """Servizio per operazioni CRUD su WarehouseShelf"""
    
    def __init__(self):
        super().__init__(WarehouseShelf)
    
    def create_shelf(self, db: Session, warehouse_row_id: int) -> WarehouseShelf:
        """Crea una nuova scaffalatura"""
        return self.create(db, warehouse_row_id=warehouse_row_id)
    
    def get_row_shelves(self, db: Session, warehouse_row_id: int) -> List[WarehouseShelf]:
        """Recupera tutte le scaffalature di una fila"""
        return db.query(WarehouseShelf).options(
            joinedload(WarehouseShelf.spots)
        ).filter(WarehouseShelf.warehouse_row_id == warehouse_row_id).all()

class WarehouseSpotService(BaseService[WarehouseSpot]):
    """Servizio per operazioni CRUD su WarehouseSpot"""
    
    def __init__(self):
        super().__init__(WarehouseSpot)
    
    def create_spot(self, db: Session, warehouse_shelf_id: int, equipment_details: str, farmer_fee: float) -> WarehouseSpot:
        """Crea un nuovo spot nel magazzino"""
        return self.create(
            db,
            warehouse_shelf_id=warehouse_shelf_id,
            equipment_details=equipment_details,
            farmer_fee=farmer_fee
        )
    
    def get_shelf_spots(self, db: Session, warehouse_shelf_id: int) -> List[WarehouseSpot]:
        """Recupera tutti gli spot di una scaffalatura"""
        return self.filter_by(db, warehouse_shelf_id=warehouse_shelf_id)
    
    def get_warehouse_spots(self, db: Session, warehouse_id: int) -> List[WarehouseSpot]:
        """Recupera tutti gli spot di un magazzino"""
        return db.query(WarehouseSpot).join(WarehouseShelf).join(WarehouseRow).filter(
            WarehouseRow.warehouse_id == warehouse_id
        ).all()
    
    def get_available_spots(self, db: Session, warehouse_id: int, start_date: date, end_date: date) -> List[WarehouseSpot]:
        """Recupera spot disponibili per un periodo"""
        # Spot già prenotati nel periodo
        booked_spots = db.query(StationBooking.warehouse_spot_id).filter(
            or_(
                and_(StationBooking.start_date <= start_date, StationBooking.end_date >= start_date),
                and_(StationBooking.start_date <= end_date, StationBooking.end_date >= end_date),
                and_(StationBooking.start_date >= start_date, StationBooking.end_date <= end_date)
            )
        ).subquery()
        
        # Tutti gli spot del magazzino non prenotati
        return db.query(WarehouseSpot).join(WarehouseShelf).join(WarehouseRow).filter(
            and_(
                WarehouseRow.warehouse_id == warehouse_id,
                ~WarehouseSpot.id.in_(booked_spots)
            )
        ).all()
    
    def get_spots_by_fee_range(self, db: Session, warehouse_id: int, min_fee: float, max_fee: float) -> List[WarehouseSpot]:
        """Recupera spot per fascia di prezzo"""
        return db.query(WarehouseSpot).join(WarehouseShelf).join(WarehouseRow).filter(
            and_(
                WarehouseRow.warehouse_id == warehouse_id,
                WarehouseSpot.farmer_fee.between(min_fee, max_fee)
            )
        ).all()
    
    def update_spot_fee(self, db: Session, spot_id: int, new_fee: float) -> Optional[WarehouseSpot]:
        """Aggiorna la tariffa di uno spot"""
        return self.update(db, spot_id, farmer_fee=new_fee)

class StationBookingService(BaseService[StationBooking]):
    """Servizio per operazioni CRUD su StationBooking"""
    
    def __init__(self):
        super().__init__(StationBooking)
    
    def create_booking(self, db: Session, user_id: int, warehouse_spot_id: int, name: str, 
                      description: str, start_date: date, end_date: date, crop_type_id: int) -> Optional[StationBooking]:
        """Crea una nuova prenotazione stazione"""
        # Verifica disponibilità dello spot
        if not self.is_spot_available(db, warehouse_spot_id, start_date, end_date):
            return None
        
        return self.create(
            db,
            user_id=user_id,
            warehouse_spot_id=warehouse_spot_id,
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            crop_type_id=crop_type_id
        )
    
    def get_user_bookings(self, db: Session, user_id: int) -> List[StationBooking]:
        """Recupera tutte le prenotazioni di un utente"""
        return db.query(StationBooking).options(
            joinedload(StationBooking.warehouse_spot),
            joinedload(StationBooking.crop_type)
        ).filter(StationBooking.user_id == user_id).all()
    
    def get_warehouse_bookings(self, db: Session, warehouse_id: int) -> List[StationBooking]:
        """Recupera tutte le prenotazioni di un magazzino"""
        return db.query(StationBooking).join(WarehouseSpot).join(WarehouseShelf).join(WarehouseRow).filter(
            WarehouseRow.warehouse_id == warehouse_id
        ).all()
    
    def get_active_bookings(self, db: Session, user_id: Optional[int] = None) -> List[StationBooking]:
        """Recupera prenotazioni attive (che includono la data odierna)"""
        query = db.query(StationBooking).filter(
            and_(
                StationBooking.start_date <= date.today(),
                StationBooking.end_date >= date.today()
            )
        )
        
        if user_id:
            query = query.filter(StationBooking.user_id == user_id)
        
        return query.all()
    
    def get_upcoming_bookings(self, db: Session, user_id: Optional[int] = None, days_ahead: int = 30) -> List[StationBooking]:
        """Recupera prenotazioni future"""
        future_date = date.today()
        from datetime import timedelta
        end_date = future_date + timedelta(days=days_ahead)
        
        query = db.query(StationBooking).filter(
            and_(
                StationBooking.start_date >= future_date,
                StationBooking.start_date <= end_date
            )
        )
        
        if user_id:
            query = query.filter(StationBooking.user_id == user_id)
        
        return query.all()
    
    def get_bookings_by_crop_type(self, db: Session, crop_type_name: str) -> List[StationBooking]:
        """Recupera prenotazioni per tipo di coltivazione"""
        return db.query(StationBooking).join(CropType).filter(
            CropType.name == crop_type_name
        ).all()
    
    def is_spot_available(self, db: Session, spot_id: int, start_date: date, end_date: date) -> bool:
        """Verifica se uno spot è disponibile per un periodo"""
        conflicting_booking = db.query(StationBooking).filter(
            and_(
                StationBooking.warehouse_spot_id == spot_id,
                or_(
                    and_(StationBooking.start_date <= start_date, StationBooking.end_date >= start_date),
                    and_(StationBooking.start_date <= end_date, StationBooking.end_date >= end_date),
                    and_(StationBooking.start_date >= start_date, StationBooking.end_date <= end_date)
                )
            )
        ).first()
        
        return conflicting_booking is None
    
    def extend_booking(self, db: Session, booking_id: int, new_end_date: date) -> Optional[StationBooking]:
        """Estende una prenotazione"""
        booking = self.get_by_id(db, booking_id)
        if not booking:
            return None
        
        # Verifica che l'estensione sia possibile
        if self.is_spot_available(db, booking.warehouse_spot_id, booking.end_date, new_end_date):
            return self.update(db, booking_id, end_date=new_end_date)
        
        return None
    
    def cancel_booking(self, db: Session, booking_id: int) -> bool:
        """Cancella una prenotazione"""
        return self.delete(db, booking_id)
    
    def get_booking_duration(self, db: Session, booking_id: int) -> Optional[int]:
        """Calcola la durata di una prenotazione in giorni"""
        booking = self.get_by_id(db, booking_id)
        if not booking:
            return None
        
        return (booking.end_date - booking.start_date).days + 1
    
    def calculate_total_cost(self, db: Session, booking_id: int) -> Optional[float]:
        """Calcola il costo totale di una prenotazione"""
        booking = db.query(StationBooking).options(
            joinedload(StationBooking.warehouse_spot)
        ).filter(StationBooking.id == booking_id).first()
        
        if not booking:
            return None
        
        duration = self.get_booking_duration(db, booking_id)
        if duration is None:
            return None
        
        return booking.warehouse_spot.farmer_fee * duration
    
    def get_warehouse_revenue(self, db: Session, warehouse_id: int, start_date: date, end_date: date) -> float:
        """Calcola il fatturato di un magazzino per un periodo"""
        bookings = db.query(StationBooking).join(WarehouseSpot).join(WarehouseShelf).join(WarehouseRow).filter(
            and_(
                WarehouseRow.warehouse_id == warehouse_id,
                StationBooking.start_date <= end_date,
                StationBooking.end_date >= start_date
            )
        ).all()
        
        total_revenue = 0.0
        for booking in bookings:
            # Calcola i giorni di sovrapposizione con il periodo richiesto
            overlap_start = max(booking.start_date, start_date)
            overlap_end = min(booking.end_date, end_date)
            
            if overlap_start <= overlap_end:
                overlap_days = (overlap_end - overlap_start).days + 1
                daily_rate = booking.warehouse_spot.farmer_fee
                total_revenue += daily_rate * overlap_days
        
        return total_revenue

# Istanze globali dei servizi
warehouse_row_service = WarehouseRowService()
warehouse_shelf_service = WarehouseShelfService()
warehouse_spot_service = WarehouseSpotService()
station_booking_service = StationBookingService()
