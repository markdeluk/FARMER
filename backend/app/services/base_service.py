from typing import TypeVar, Generic, Type, Optional, List, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.db.base import Base

T = TypeVar('T', bound=Base)

class BaseService(Generic[T]):
    """Servizio CRUD base generico per tutti i modelli"""
    
    def __init__(self, model: Type[T]):
        self.model = model
    
    def create(self, db: Session, **kwargs) -> T:
        """Crea una nuova istanza del modello"""
        db_obj = self.model(**kwargs)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_by_id(self, db: Session, id: int) -> Optional[T]:
        """Recupera un'istanza per ID"""
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[T]:
        """Recupera tutte le istanze con paginazione"""
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def update(self, db: Session, id: int, **kwargs) -> Optional[T]:
        """Aggiorna un'istanza esistente"""
        db_obj = self.get_by_id(db, id)
        if not db_obj:
            return None
        
        for field, value in kwargs.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, id: int) -> bool:
        """Elimina un'istanza per ID"""
        db_obj = self.get_by_id(db, id)
        if not db_obj:
            return False
        
        db.delete(db_obj)
        db.commit()
        return True
    
    def exists(self, db: Session, id: int) -> bool:
        """Verifica se un'istanza esiste"""
        return db.query(self.model).filter(self.model.id == id).first() is not None
    
    def count(self, db: Session) -> int:
        """Conta il numero totale di istanze"""
        return db.query(self.model).count()
    
    def filter_by(self, db: Session, **kwargs) -> List[T]:
        """Filtra le istanze per attributi specifici"""
        query = db.query(self.model)
        for field, value in kwargs.items():
            if hasattr(self.model, field):
                query = query.filter(getattr(self.model, field) == value)
        return query.all()
    
    def bulk_create(self, db: Session, objects_data: List[Dict[str, Any]]) -> List[T]:
        """Crea multiple istanze in una singola transazione"""
        db_objects = [self.model(**data) for data in objects_data]
        db.add_all(db_objects)
        db.commit()
        for obj in db_objects:
            db.refresh(obj)
        return db_objects
