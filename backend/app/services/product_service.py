from typing import List, Optional
from datetime import date, time
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, func
from app.models.product import Product, ProductDailyAvailability, ProductReservation
from app.models.enums import ProductCategory, UnitMeasure
from app.services.base_service import BaseService

class ProductService(BaseService[Product]):
    """Servizio per operazioni CRUD su Product"""
    
    def __init__(self):
        super().__init__(Product)
    
    def create_product(self, db: Session, market_id: int, name: str, description: Optional[str], 
                      category_id: int, unit_weight: float, unit_measure_id: int) -> Product:
        """Crea un nuovo prodotto"""
        return self.create(
            db,
            market_id=market_id,
            name=name,
            description=description,
            category_id=category_id,
            unit_weight=unit_weight,
            unit_measure_id=unit_measure_id
        )
    
    def get_product_with_details(self, db: Session, product_id: int) -> Optional[Product]:
        """Recupera un prodotto con tutti i dettagli"""
        return db.query(Product).options(
            joinedload(Product.market),
            joinedload(Product.category),
            joinedload(Product.unit_measure)
        ).filter(Product.id == product_id).first()
    
    def get_market_products(self, db: Session, market_id: int) -> List[Product]:
        """Recupera tutti i prodotti di un mercato"""
        return self.filter_by(db, market_id=market_id)
    
    def get_products_by_category(self, db: Session, category_name: str) -> List[Product]:
        """Recupera prodotti per categoria"""
        return db.query(Product).join(ProductCategory).filter(
            ProductCategory.name == category_name
        ).all()
    
    def search_products_by_name(self, db: Session, search_term: str) -> List[Product]:
        """Cerca prodotti per nome"""
        return db.query(Product).filter(
            Product.name.ilike(f"%{search_term}%")
        ).all()
    
    def get_available_products_today(self, db: Session, market_id: Optional[int] = None) -> List[Product]:
        """Recupera prodotti disponibili oggi"""
        query = db.query(Product).join(ProductDailyAvailability).filter(
            ProductDailyAvailability.date == date.today(),
            ProductDailyAvailability.available_quantity > 0
        )
        
        if market_id:
            query = query.filter(Product.market_id == market_id)
        
        return query.all()

class ProductDailyAvailabilityService(BaseService[ProductDailyAvailability]):
    """Servizio per operazioni CRUD su ProductDailyAvailability"""
    
    def __init__(self):
        super().__init__(ProductDailyAvailability)
    
    def create_availability(self, db: Session, product_id: int, date: date, 
                          available_quantity: int, daily_price: float,
                          discounted_price: Optional[float] = None,
                          start_time_discount: Optional[time] = None,
                          end_time_discount: Optional[time] = None) -> Optional[ProductDailyAvailability]:
        """Crea una nuova disponibilità giornaliera"""
        try:
            return self.create(
                db,
                product_id=product_id,
                date=date,
                available_quantity=available_quantity,
                daily_price=daily_price,
                discounted_price=discounted_price,
                start_time_discount=start_time_discount,
                end_time_discount=end_time_discount
            )
        except IntegrityError:
            db.rollback()
            return None  # Violazione constraint unique
    
    def get_product_availability(self, db: Session, product_id: int, date: date) -> Optional[ProductDailyAvailability]:
        """Recupera la disponibilità di un prodotto per una data"""
        return db.query(ProductDailyAvailability).filter(
            and_(
                ProductDailyAvailability.product_id == product_id,
                ProductDailyAvailability.date == date
            )
        ).first()
    
    def get_product_availabilities_range(self, db: Session, product_id: int, 
                                       start_date: date, end_date: date) -> List[ProductDailyAvailability]:
        """Recupera le disponibilità di un prodotto in un range di date"""
        return db.query(ProductDailyAvailability).filter(
            and_(
                ProductDailyAvailability.product_id == product_id,
                ProductDailyAvailability.date.between(start_date, end_date)
            )
        ).all()
    
    def update_quantity(self, db: Session, product_id: int, date: date, new_quantity: int) -> Optional[ProductDailyAvailability]:
        """Aggiorna la quantità disponibile"""
        availability = self.get_product_availability(db, product_id, date)
        if availability:
            return self.update(db, availability.id, available_quantity=new_quantity)
        return None
    
    def get_discounted_products(self, db: Session, current_time: time, current_date: date) -> List[ProductDailyAvailability]:
        """Recupera prodotti in sconto al momento attuale"""
        return db.query(ProductDailyAvailability).filter(
            and_(
                ProductDailyAvailability.date == current_date,
                ProductDailyAvailability.discounted_price.isnot(None),
                ProductDailyAvailability.start_time_discount <= current_time,
                ProductDailyAvailability.end_time_discount >= current_time
            )
        ).all()

class ProductReservationService(BaseService[ProductReservation]):
    """Servizio per operazioni CRUD su ProductReservation"""
    
    def __init__(self):
        super().__init__(ProductReservation)
    
    def create_reservation(self, db: Session, user_id: int, product_id: int, 
                         date: date, time_slot: time, desired_quantity: int) -> Optional[ProductReservation]:
        """Crea una nuova prenotazione"""
        try:
            # Verifica disponibilità
            availability = db.query(ProductDailyAvailability).filter(
                and_(
                    ProductDailyAvailability.product_id == product_id,
                    ProductDailyAvailability.date == date
                )
            ).first()
            
            if not availability or availability.available_quantity < desired_quantity:
                return None  # Quantità non disponibile
            
            reservation = self.create(
                db,
                user_id=user_id,
                product_id=product_id,
                date=date,
                time_slot=time_slot,
                desired_quantity=desired_quantity
            )
            
            # Aggiorna la disponibilità
            availability.available_quantity -= desired_quantity
            db.commit()
            
            return reservation
            
        except IntegrityError:
            db.rollback()
            return None  # Violazione constraint unique
    
    def get_user_reservations(self, db: Session, user_id: int) -> List[ProductReservation]:
        """Recupera tutte le prenotazioni di un utente"""
        return db.query(ProductReservation).options(
            joinedload(ProductReservation.product)
        ).filter(ProductReservation.user_id == user_id).all()
    
    def get_product_reservations(self, db: Session, product_id: int, date: date) -> List[ProductReservation]:
        """Recupera tutte le prenotazioni per un prodotto in una data"""
        return db.query(ProductReservation).filter(
            and_(
                ProductReservation.product_id == product_id,
                ProductReservation.date == date
            )
        ).all()
    
    def get_user_reservations_by_date(self, db: Session, user_id: int, date: date) -> List[ProductReservation]:
        """Recupera le prenotazioni di un utente per una data specifica"""
        return db.query(ProductReservation).options(
            joinedload(ProductReservation.product)
        ).filter(
            and_(
                ProductReservation.user_id == user_id,
                ProductReservation.date == date
            )
        ).all()
    
    def cancel_reservation(self, db: Session, reservation_id: int) -> bool:
        """Cancella una prenotazione e ripristina la disponibilità"""
        reservation = self.get_by_id(db, reservation_id)
        if not reservation:
            return False
        
        # Ripristina la disponibilità
        availability = db.query(ProductDailyAvailability).filter(
            and_(
                ProductDailyAvailability.product_id == reservation.product_id,
                ProductDailyAvailability.date == reservation.date
            )
        ).first()
        
        if availability:
            availability.available_quantity += reservation.desired_quantity
        
        return self.delete(db, reservation_id)
    
    def get_total_reserved_quantity(self, db: Session, product_id: int, date: date) -> int:
        """Calcola la quantità totale prenotata per un prodotto in una data"""
        result = db.query(func.sum(ProductReservation.desired_quantity)).filter(
            and_(
                ProductReservation.product_id == product_id,
                ProductReservation.date == date
            )
        ).scalar()
        
        return result or 0

# Istanze globali dei servizi
product_service = ProductService()
product_availability_service = ProductDailyAvailabilityService()
product_reservation_service = ProductReservationService()
