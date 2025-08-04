from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from app.models.request_flow import RequestFlow, EventRequestFlow, StationRequestFlow
from app.models.enums import RequestStatus
from app.services.base_service import BaseService

class RequestFlowService(BaseService[RequestFlow]):
    """Servizio per operazioni CRUD su RequestFlow"""
    
    def __init__(self):
        super().__init__(RequestFlow)
    
    def create_request_flow(self, db: Session, request_status_id: int, date_time: datetime) -> RequestFlow:
        """Crea un nuovo flusso di richiesta"""
        return self.create(
            db,
            request_status_id=request_status_id,
            date_time=date_time
        )
    
    def get_request_flow_with_status(self, db: Session, flow_id: int) -> Optional[RequestFlow]:
        """Recupera un flusso con il suo stato"""
        return db.query(RequestFlow).options(
            joinedload(RequestFlow.request_status)
        ).filter(RequestFlow.id == flow_id).first()
    
    def get_flows_by_status(self, db: Session, status_name: str) -> List[RequestFlow]:
        """Recupera flussi per stato"""
        return db.query(RequestFlow).join(RequestStatus).filter(
            RequestStatus.name == status_name
        ).all()
    
    def get_pending_requests(self, db: Session) -> List[RequestFlow]:
        """Recupera tutte le richieste in sospeso"""
        return self.get_flows_by_status(db, "pending")
    
    def get_approved_requests(self, db: Session) -> List[RequestFlow]:
        """Recupera tutte le richieste approvate"""
        return self.get_flows_by_status(db, "approved")
    
    def get_rejected_requests(self, db: Session) -> List[RequestFlow]:
        """Recupera tutte le richieste rifiutate"""
        return self.get_flows_by_status(db, "rejected")
    
    def update_request_status(self, db: Session, flow_id: int, new_status_id: int) -> Optional[RequestFlow]:
        """Aggiorna lo stato di una richiesta"""
        return self.update(db, flow_id, request_status_id=new_status_id)

class EventRequestFlowService(BaseService[EventRequestFlow]):
    """Servizio per operazioni CRUD su EventRequestFlow"""
    
    def __init__(self):
        super().__init__(EventRequestFlow)
    
    def create_event_request(self, db: Session, request_flow_id: int, event_id: int) -> EventRequestFlow:
        """Crea una nuova richiesta evento"""
        return self.create(db, id=request_flow_id, event_id=event_id)
    
    def get_event_request_with_details(self, db: Session, request_id: int) -> Optional[EventRequestFlow]:
        """Recupera una richiesta evento con tutti i dettagli"""
        return db.query(EventRequestFlow).options(
            joinedload(EventRequestFlow.request_flow).joinedload(RequestFlow.request_status),
            joinedload(EventRequestFlow.event)
        ).filter(EventRequestFlow.id == request_id).first()
    
    def get_event_requests(self, db: Session, event_id: int) -> List[EventRequestFlow]:
        """Recupera tutte le richieste per un evento"""
        return db.query(EventRequestFlow).options(
            joinedload(EventRequestFlow.request_flow).joinedload(RequestFlow.request_status)
        ).filter(EventRequestFlow.event_id == event_id).all()
    
    def get_pending_event_requests(self, db: Session) -> List[EventRequestFlow]:
        """Recupera richieste evento in sospeso"""
        return db.query(EventRequestFlow).join(RequestFlow).join(RequestStatus).filter(
            RequestStatus.name == "pending"
        ).all()
    
    def approve_event_request(self, db: Session, request_id: int) -> Optional[EventRequestFlow]:
        """Approva una richiesta evento"""
        request = self.get_by_id(db, request_id)
        if not request:
            return None
        
        # Trova l'ID del status "approved"
        approved_status = db.query(RequestStatus).filter(RequestStatus.name == "approved").first()
        if not approved_status:
            return None
        
        # Aggiorna il request flow
        request_flow_service = RequestFlowService()
        request_flow_service.update_request_status(db, request.id, approved_status.id)
        
        return self.get_by_id(db, request_id)
    
    def reject_event_request(self, db: Session, request_id: int) -> Optional[EventRequestFlow]:
        """Rifiuta una richiesta evento"""
        request = self.get_by_id(db, request_id)
        if not request:
            return None
        
        # Trova l'ID del status "rejected"
        rejected_status = db.query(RequestStatus).filter(RequestStatus.name == "rejected").first()
        if not rejected_status:
            return None
        
        # Aggiorna il request flow
        request_flow_service = RequestFlowService()
        request_flow_service.update_request_status(db, request.id, rejected_status.id)
        
        return self.get_by_id(db, request_id)

class StationRequestFlowService(BaseService[StationRequestFlow]):
    """Servizio per operazioni CRUD su StationRequestFlow"""
    
    def __init__(self):
        super().__init__(StationRequestFlow)
    
    def create_station_request(self, db: Session, request_flow_id: int, station_booking_id: int) -> StationRequestFlow:
        """Crea una nuova richiesta stazione"""
        return self.create(db, id=request_flow_id, station_booking_id=station_booking_id)
    
    def get_station_request_with_details(self, db: Session, request_id: int) -> Optional[StationRequestFlow]:
        """Recupera una richiesta stazione con tutti i dettagli"""
        return db.query(StationRequestFlow).options(
            joinedload(StationRequestFlow.request_flow).joinedload(RequestFlow.request_status),
            joinedload(StationRequestFlow.station_booking)
        ).filter(StationRequestFlow.id == request_id).first()
    
    def get_station_requests(self, db: Session, station_booking_id: int) -> List[StationRequestFlow]:
        """Recupera tutte le richieste per una prenotazione stazione"""
        return db.query(StationRequestFlow).options(
            joinedload(StationRequestFlow.request_flow).joinedload(RequestFlow.request_status)
        ).filter(StationRequestFlow.station_booking_id == station_booking_id).all()
    
    def get_pending_station_requests(self, db: Session) -> List[StationRequestFlow]:
        """Recupera richieste stazione in sospeso"""
        return db.query(StationRequestFlow).join(RequestFlow).join(RequestStatus).filter(
            RequestStatus.name == "pending"
        ).all()
    
    def approve_station_request(self, db: Session, request_id: int) -> Optional[StationRequestFlow]:
        """Approva una richiesta stazione"""
        request = self.get_by_id(db, request_id)
        if not request:
            return None
        
        # Trova l'ID del status "approved"
        approved_status = db.query(RequestStatus).filter(RequestStatus.name == "approved").first()
        if not approved_status:
            return None
        
        # Aggiorna il request flow
        request_flow_service = RequestFlowService()
        request_flow_service.update_request_status(db, request.id, approved_status.id)
        
        return self.get_by_id(db, request_id)
    
    def reject_station_request(self, db: Session, request_id: int) -> Optional[StationRequestFlow]:
        """Rifiuta una richiesta stazione"""
        request = self.get_by_id(db, request_id)
        if not request:
            return None
        
        # Trova l'ID del status "rejected"
        rejected_status = db.query(RequestStatus).filter(RequestStatus.name == "rejected").first()
        if not rejected_status:
            return None
        
        # Aggiorna il request flow
        request_flow_service = RequestFlowService()
        request_flow_service.update_request_status(db, request.id, rejected_status.id)
        
        return self.get_by_id(db, request_id)

# Istanze globali dei servizi
request_flow_service = RequestFlowService()
event_request_flow_service = EventRequestFlowService()
station_request_flow_service = StationRequestFlowService()
