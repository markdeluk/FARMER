from typing import List, Optional
from datetime import date, time
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, func
from app.models.restaurant import RestaurantTable, RestaurantSeat, MenuItem, RestaurantBooking
from app.models.enums import MenuCategory
from app.services.base_service import BaseService

class RestaurantTableService(BaseService[RestaurantTable]):
    """Servizio per operazioni CRUD su RestaurantTable"""
    
    def __init__(self):
        super().__init__(RestaurantTable)
    
    def create_table(self, db: Session, name: str, restaurant_id: int) -> RestaurantTable:
        """Crea un nuovo tavolo"""
        return self.create(db, name=name, restaurant_id=restaurant_id)
    
    def get_restaurant_tables(self, db: Session, restaurant_id: int) -> List[RestaurantTable]:
        """Recupera tutti i tavoli di un ristorante"""
        return db.query(RestaurantTable).options(
            joinedload(RestaurantTable.seats)
        ).filter(RestaurantTable.restaurant_id == restaurant_id).all()
    
    def get_table_with_seats(self, db: Session, table_id: int) -> Optional[RestaurantTable]:
        """Recupera un tavolo con i suoi posti"""
        return db.query(RestaurantTable).options(
            joinedload(RestaurantTable.seats)
        ).filter(RestaurantTable.id == table_id).first()

class RestaurantSeatService(BaseService[RestaurantSeat]):
    """Servizio per operazioni CRUD su RestaurantSeat"""
    
    def __init__(self):
        super().__init__(RestaurantSeat)
    
    def create_seat(self, db: Session, restaurant_table_id: int) -> RestaurantSeat:
        """Crea un nuovo posto"""
        return self.create(db, restaurant_table_id=restaurant_table_id)
    
    def get_table_seats(self, db: Session, table_id: int) -> List[RestaurantSeat]:
        """Recupera tutti i posti di un tavolo"""
        return self.filter_by(db, restaurant_table_id=table_id)
    
    def get_available_seats(self, db: Session, restaurant_id: int, date: date, time_slot: time) -> List[RestaurantSeat]:
        """Recupera i posti disponibili per una data e orario"""
        # Posti già prenotati
        booked_seats = db.query(RestaurantBooking.restaurant_seat_id).filter(
            and_(
                RestaurantBooking.date == date,
                RestaurantBooking.time_slot == time_slot
            )
        ).subquery()
        
        # Tutti i posti del ristorante non prenotati
        return db.query(RestaurantSeat).join(RestaurantTable).filter(
            and_(
                RestaurantTable.restaurant_id == restaurant_id,
                ~RestaurantSeat.id.in_(booked_seats)
            )
        ).all()
    
    def get_restaurant_total_seats(self, db: Session, restaurant_id: int) -> int:
        """Conta il numero totale di posti in un ristorante"""
        return db.query(RestaurantSeat).join(RestaurantTable).filter(
            RestaurantTable.restaurant_id == restaurant_id
        ).count()

class MenuItemService(BaseService[MenuItem]):
    """Servizio per operazioni CRUD su MenuItem"""
    
    def __init__(self):
        super().__init__(MenuItem)
    
    def create_menu_item(self, db: Session, name: str, price: float, menu_category_id: int, 
                        description: str, restaurant_id: int) -> MenuItem:
        """Crea una nuova voce di menu"""
        return self.create(
            db,
            name=name,
            price=price,
            menu_category_id=menu_category_id,
            description=description,
            restaurant_id=restaurant_id
        )
    
    def get_restaurant_menu(self, db: Session, restaurant_id: int) -> List[MenuItem]:
        """Recupera tutto il menu di un ristorante"""
        return db.query(MenuItem).options(
            joinedload(MenuItem.menu_category)
        ).filter(MenuItem.restaurant_id == restaurant_id).all()
    
    def get_menu_by_category(self, db: Session, restaurant_id: int, category_name: str) -> List[MenuItem]:
        """Recupera le voci di menu per categoria"""
        return db.query(MenuItem).join(MenuCategory).filter(
            and_(
                MenuItem.restaurant_id == restaurant_id,
                MenuCategory.name == category_name
            )
        ).all()
    
    def get_menu_items_by_price_range(self, db: Session, restaurant_id: int, 
                                    min_price: float, max_price: float) -> List[MenuItem]:
        """Recupera voci di menu per fascia di prezzo"""
        return db.query(MenuItem).filter(
            and_(
                MenuItem.restaurant_id == restaurant_id,
                MenuItem.price.between(min_price, max_price)
            )
        ).all()
    
    def search_menu_items(self, db: Session, restaurant_id: int, search_term: str) -> List[MenuItem]:
        """Cerca voci di menu per nome o descrizione"""
        return db.query(MenuItem).filter(
            and_(
                MenuItem.restaurant_id == restaurant_id,
                (MenuItem.name.ilike(f"%{search_term}%") | 
                 MenuItem.description.ilike(f"%{search_term}%"))
            )
        ).all()
    
    def update_menu_item_price(self, db: Session, item_id: int, new_price: float) -> Optional[MenuItem]:
        """Aggiorna il prezzo di una voce di menu"""
        return self.update(db, item_id, price=new_price)

class RestaurantBookingService(BaseService[RestaurantBooking]):
    """Servizio per operazioni CRUD su RestaurantBooking"""
    
    def __init__(self):
        super().__init__(RestaurantBooking)
    
    def create_booking(self, db: Session, user_id: int, restaurant_seat_id: int, 
                      date: date, time_slot: time) -> Optional[RestaurantBooking]:
        """Crea una nuova prenotazione"""
        try:
            return self.create(
                db,
                user_id=user_id,
                restaurant_seat_id=restaurant_seat_id,
                date=date,
                time_slot=time_slot
            )
        except IntegrityError:
            db.rollback()
            return None  # Posto già prenotato
    
    def get_user_bookings(self, db: Session, user_id: int) -> List[RestaurantBooking]:
        """Recupera tutte le prenotazioni di un utente"""
        return db.query(RestaurantBooking).options(
            joinedload(RestaurantBooking.restaurant_seat).joinedload(RestaurantSeat.table)
        ).filter(RestaurantBooking.user_id == user_id).all()
    
    def get_restaurant_bookings_by_date(self, db: Session, restaurant_id: int, date: date) -> List[RestaurantBooking]:
        """Recupera tutte le prenotazioni di un ristorante per una data"""
        return db.query(RestaurantBooking).join(RestaurantSeat).join(RestaurantTable).filter(
            and_(
                RestaurantTable.restaurant_id == restaurant_id,
                RestaurantBooking.date == date
            )
        ).all()
    
    def get_bookings_by_time_slot(self, db: Session, restaurant_id: int, 
                                 date: date, time_slot: time) -> List[RestaurantBooking]:
        """Recupera prenotazioni per un orario specifico"""
        return db.query(RestaurantBooking).join(RestaurantSeat).join(RestaurantTable).filter(
            and_(
                RestaurantTable.restaurant_id == restaurant_id,
                RestaurantBooking.date == date,
                RestaurantBooking.time_slot == time_slot
            )
        ).all()
    
    def is_seat_available(self, db: Session, seat_id: int, date: date, time_slot: time) -> bool:
        """Verifica se un posto è disponibile"""
        booking = db.query(RestaurantBooking).filter(
            and_(
                RestaurantBooking.restaurant_seat_id == seat_id,
                RestaurantBooking.date == date,
                RestaurantBooking.time_slot == time_slot
            )
        ).first()
        
        return booking is None
    
    def cancel_booking(self, db: Session, booking_id: int) -> bool:
        """Cancella una prenotazione"""
        return self.delete(db, booking_id)
    
    def get_restaurant_occupancy_rate(self, db: Session, restaurant_id: int, date: date) -> float:
        """Calcola il tasso di occupazione di un ristorante per una data"""
        total_seats = db.query(RestaurantSeat).join(RestaurantTable).filter(
            RestaurantTable.restaurant_id == restaurant_id
        ).count()
        
        if total_seats == 0:
            return 0.0
        
        booked_seats = db.query(RestaurantBooking).join(RestaurantSeat).join(RestaurantTable).filter(
            and_(
                RestaurantTable.restaurant_id == restaurant_id,
                RestaurantBooking.date == date
            )
        ).count()
        
        return (booked_seats / total_seats) * 100

# Istanze globali dei servizi
restaurant_table_service = RestaurantTableService()
restaurant_seat_service = RestaurantSeatService()
menu_item_service = MenuItemService()
restaurant_booking_service = RestaurantBookingService()
