from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.location import Contact
from app.models.enums import ContactInfoType
from app.services.base_service import BaseService

class ContactService(BaseService[Contact]):
    """Servizio per operazioni CRUD su Contact"""
    
    def __init__(self):
        super().__init__(Contact)
    
    def create_contact(self, db: Session, user_id: int, contact_info_type_id: int, contact_info: str) -> Optional[Contact]:
        """Crea un nuovo contatto per un utente"""
        try:
            return self.create(
                db, 
                user_id=user_id, 
                contact_info_type_id=contact_info_type_id, 
                contact_info=contact_info
            )
        except IntegrityError:
            db.rollback()
            return None  # Violazione del constraint unique
    
    def get_user_contacts(self, db: Session, user_id: int) -> List[Contact]:
        """Recupera tutti i contatti di un utente"""
        return self.filter_by(db, user_id=user_id)
    
    def get_user_contact_by_type(self, db: Session, user_id: int, contact_type_name: str) -> Optional[Contact]:
        """Recupera il contatto di un utente per tipo (email/telephone)"""
        return db.query(Contact).join(ContactInfoType).filter(
            Contact.user_id == user_id,
            ContactInfoType.name == contact_type_name
        ).first()
    
    def get_user_email(self, db: Session, user_id: int) -> Optional[str]:
        """Recupera l'email di un utente"""
        contact = self.get_user_contact_by_type(db, user_id, "email")
        return contact.contact_info if contact else None
    
    def get_user_phone(self, db: Session, user_id: int) -> Optional[str]:
        """Recupera il telefono di un utente"""
        contact = self.get_user_contact_by_type(db, user_id, "telephone")
        return contact.contact_info if contact else None
    
    def update_user_email(self, db: Session, user_id: int, new_email: str) -> Optional[Contact]:
        """Aggiorna l'email di un utente"""
        contact = self.get_user_contact_by_type(db, user_id, "email")
        if contact:
            return self.update(db, contact.id, contact_info=new_email)
        return None
    
    def update_user_phone(self, db: Session, user_id: int, new_phone: str) -> Optional[Contact]:
        """Aggiorna il telefono di un utente"""
        contact = self.get_user_contact_by_type(db, user_id, "telephone")
        if contact:
            return self.update(db, contact.id, contact_info=new_phone)
        return None
    
    def search_by_email(self, db: Session, email: str) -> Optional[Contact]:
        """Cerca un contatto per email"""
        return db.query(Contact).join(ContactInfoType).filter(
            ContactInfoType.name == "email",
            Contact.contact_info == email
        ).first()
    
    def search_by_phone(self, db: Session, phone: str) -> Optional[Contact]:
        """Cerca un contatto per telefono"""
        return db.query(Contact).join(ContactInfoType).filter(
            ContactInfoType.name == "telephone",
            Contact.contact_info == phone
        ).first()

# Istanza globale del servizio
contact_service = ContactService()
