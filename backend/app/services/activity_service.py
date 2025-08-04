from typing import List, Optional
from datetime import date, time
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, func
from app.models.activity import Workshop, WorkshopSeat, Event, EventSeat, WorkshopEnrollment, EventEnrollment
from app.models.vendor import Activity
from app.models.enums import DayWeek
from app.services.base_service import BaseService

class WorkshopService(BaseService[Workshop]):
    """Servizio per operazioni CRUD su Workshop"""
    
    def __init__(self):
        super().__init__(Workshop)
    
    def create_workshop(self, db: Session, activity_id: int, day_week_id: int) -> Workshop:
        """Crea un nuovo workshop"""
        return self.create(db, id=activity_id, day_week_id=day_week_id)
    
    def get_workshop_with_details(self, db: Session, workshop_id: int) -> Optional[Workshop]:
        """Recupera un workshop con tutti i dettagli"""
        return db.query(Workshop).options(
            joinedload(Workshop.activity).joinedload(Activity.vendor),
            joinedload(Workshop.day_week),
            joinedload(Workshop.seats)
        ).filter(Workshop.id == workshop_id).first()
    
    def get_workshops_by_day(self, db: Session, day_name: str) -> List[Workshop]:
        """Recupera workshop per giorno della settimana"""
        return db.query(Workshop).join(DayWeek).filter(
            DayWeek.name == day_name
        ).all()
    
    def get_available_workshops(self, db: Session, day_name: Optional[str] = None) -> List[Workshop]:
        """Recupera workshop con posti disponibili"""
        query = db.query(Workshop).join(Activity)
        
        if day_name:
            query = query.join(DayWeek).filter(DayWeek.name == day_name)
        
        # Filtra workshop con posti disponibili
        workshops = query.all()
        available_workshops = []
        
        for workshop in workshops:
            occupied_seats = db.query(WorkshopSeat).filter(
                WorkshopSeat.workshop_id == workshop.id
            ).count()
            
            if occupied_seats < workshop.activity.capacity:
                available_workshops.append(workshop)
        
        return available_workshops

class WorkshopSeatService(BaseService[WorkshopSeat]):
    """Servizio per operazioni CRUD su WorkshopSeat"""
    
    def __init__(self):
        super().__init__(WorkshopSeat)
    
    def create_seat(self, db: Session, workshop_id: int, user_id: int) -> Optional[WorkshopSeat]:
        """Crea un nuovo posto workshop"""
        # Verifica capacità
        workshop = db.query(Workshop).join(Activity).filter(Workshop.id == workshop_id).first()
        if not workshop:
            return None
        
        current_seats = self.count_workshop_seats(db, workshop_id)
        if current_seats >= workshop.activity.capacity:
            return None  # Workshop pieno
        
        return self.create(db, workshop_id=workshop_id, user_id=user_id)
    
    def get_workshop_seats(self, db: Session, workshop_id: int) -> List[WorkshopSeat]:
        """Recupera tutti i posti di un workshop"""
        return db.query(WorkshopSeat).options(
            joinedload(WorkshopSeat.user)
        ).filter(WorkshopSeat.workshop_id == workshop_id).all()
    
    def get_user_workshop_seats(self, db: Session, user_id: int) -> List[WorkshopSeat]:
        """Recupera tutti i posti workshop di un utente"""
        return db.query(WorkshopSeat).options(
            joinedload(WorkshopSeat.workshop)
        ).filter(WorkshopSeat.user_id == user_id).all()
    
    def count_workshop_seats(self, db: Session, workshop_id: int) -> int:
        """Conta i posti occupati in un workshop"""
        return db.query(WorkshopSeat).filter(
            WorkshopSeat.workshop_id == workshop_id
        ).count()
    
    def is_workshop_full(self, db: Session, workshop_id: int) -> bool:
        """Verifica se un workshop è pieno"""
        workshop = db.query(Workshop).join(Activity).filter(Workshop.id == workshop_id).first()
        if not workshop:
            return True
        
        current_seats = self.count_workshop_seats(db, workshop_id)
        return current_seats >= workshop.activity.capacity

class EventService(BaseService[Event]):
    """Servizio per operazioni CRUD su Event"""
    
    def __init__(self):
        super().__init__(Event)
    
    def create_event(self, db: Session, activity_id: int, date: date, organizer_fee: float) -> Event:
        """Crea un nuovo evento"""
        return self.create(db, id=activity_id, date=date, organizer_fee=organizer_fee)
    
    def get_event_with_details(self, db: Session, event_id: int) -> Optional[Event]:
        """Recupera un evento con tutti i dettagli"""
        return db.query(Event).options(
            joinedload(Event.activity).joinedload(Activity.vendor),
            joinedload(Event.seats)
        ).filter(Event.id == event_id).first()
    
    def get_events_by_date_range(self, db: Session, start_date: date, end_date: date) -> List[Event]:
        """Recupera eventi in un range di date"""
        return db.query(Event).filter(
            Event.date.between(start_date, end_date)
        ).all()
    
    def get_upcoming_events(self, db: Session, limit: int = 10) -> List[Event]:
        """Recupera i prossimi eventi"""
        return db.query(Event).filter(
            Event.date >= date.today()
        ).order_by(Event.date).limit(limit).all()
    
    def get_available_events(self, db: Session, from_date: Optional[date] = None) -> List[Event]:
        """Recupera eventi con posti disponibili"""
        query = db.query(Event).join(Activity)
        
        if from_date:
            query = query.filter(Event.date >= from_date)
        else:
            query = query.filter(Event.date >= date.today())
        
        events = query.all()
        available_events = []
        
        for event in events:
            occupied_seats = db.query(EventSeat).filter(
                EventSeat.event_id == event.id
            ).count()
            
            if occupied_seats < event.activity.capacity:
                available_events.append(event)
        
        return available_events

class EventSeatService(BaseService[EventSeat]):
    """Servizio per operazioni CRUD su EventSeat"""
    
    def __init__(self):
        super().__init__(EventSeat)
    
    def create_seat(self, db: Session, event_id: int, user_id: int) -> Optional[EventSeat]:
        """Crea un nuovo posto evento"""
        # Verifica capacità
        event = db.query(Event).join(Activity).filter(Event.id == event_id).first()
        if not event:
            return None
        
        current_seats = self.count_event_seats(db, event_id)
        if current_seats >= event.activity.capacity:
            return None  # Evento pieno
        
        return self.create(db, event_id=event_id, user_id=user_id)
    
    def get_event_seats(self, db: Session, event_id: int) -> List[EventSeat]:
        """Recupera tutti i posti di un evento"""
        return db.query(EventSeat).options(
            joinedload(EventSeat.user)
        ).filter(EventSeat.event_id == event_id).all()
    
    def get_user_event_seats(self, db: Session, user_id: int) -> List[EventSeat]:
        """Recupera tutti i posti evento di un utente"""
        return db.query(EventSeat).options(
            joinedload(EventSeat.event)
        ).filter(EventSeat.user_id == user_id).all()
    
    def count_event_seats(self, db: Session, event_id: int) -> int:
        """Conta i posti occupati in un evento"""
        return db.query(EventSeat).filter(
            EventSeat.event_id == event_id
        ).count()
    
    def is_event_full(self, db: Session, event_id: int) -> bool:
        """Verifica se un evento è pieno"""
        event = db.query(Event).join(Activity).filter(Event.id == event_id).first()
        if not event:
            return True
        
        current_seats = self.count_event_seats(db, event_id)
        return current_seats >= event.activity.capacity

class WorkshopEnrollmentService(BaseService[WorkshopEnrollment]):
    """Servizio per operazioni CRUD su WorkshopEnrollment"""
    
    def __init__(self):
        super().__init__(WorkshopEnrollment)
    
    def create_enrollment(self, db: Session, user_id: int, workshop_seat_id: int, date: date) -> Optional[WorkshopEnrollment]:
        """Crea una nuova iscrizione workshop"""
        try:
            return self.create(
                db,
                user_id=user_id,
                workshop_seat_id=workshop_seat_id,
                date=date
            )
        except IntegrityError:
            db.rollback()
            return None  # Utente già iscritto per quella data
    
    def get_user_workshop_enrollments(self, db: Session, user_id: int) -> List[WorkshopEnrollment]:
        """Recupera tutte le iscrizioni workshop di un utente"""
        return db.query(WorkshopEnrollment).options(
            joinedload(WorkshopEnrollment.workshop_seat).joinedload(WorkshopSeat.workshop)
        ).filter(WorkshopEnrollment.user_id == user_id).all()
    
    def get_workshop_enrollments_by_date(self, db: Session, workshop_id: int, date: date) -> List[WorkshopEnrollment]:
        """Recupera iscrizioni workshop per una data"""
        return db.query(WorkshopEnrollment).join(WorkshopSeat).filter(
            and_(
                WorkshopSeat.workshop_id == workshop_id,
                WorkshopEnrollment.date == date
            )
        ).all()

class EventEnrollmentService(BaseService[EventEnrollment]):
    """Servizio per operazioni CRUD su EventEnrollment"""
    
    def __init__(self):
        super().__init__(EventEnrollment)
    
    def create_enrollment(self, db: Session, user_id: int, event_seat_id: int) -> Optional[EventEnrollment]:
        """Crea una nuova iscrizione evento"""
        try:
            return self.create(
                db,
                user_id=user_id,
                event_seat_id=event_seat_id
            )
        except IntegrityError:
            db.rollback()
            return None  # Utente già iscritto
    
    def get_user_event_enrollments(self, db: Session, user_id: int) -> List[EventEnrollment]:
        """Recupera tutte le iscrizioni evento di un utente"""
        return db.query(EventEnrollment).options(
            joinedload(EventEnrollment.event_seat).joinedload(EventSeat.event)
        ).filter(EventEnrollment.user_id == user_id).all()
    
    def get_event_enrollments(self, db: Session, event_id: int) -> List[EventEnrollment]:
        """Recupera tutte le iscrizioni per un evento"""
        return db.query(EventEnrollment).join(EventSeat).filter(
            EventSeat.event_id == event_id
        ).all()

# Istanze globali dei servizi
workshop_service = WorkshopService()
workshop_seat_service = WorkshopSeatService()
event_service = EventService()
event_seat_service = EventSeatService()
workshop_enrollment_service = WorkshopEnrollmentService()
event_enrollment_service = EventEnrollmentService()
