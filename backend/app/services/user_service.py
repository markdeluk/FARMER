from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.user import User
from app.models.enums import RoleType
from app.services.base_service import BaseService

class UserService(BaseService[User]):
    """Servizio per operazioni CRUD su User"""
    
    def __init__(self):
        super().__init__(User)
    
    def create_user(self, db: Session, name: str, surname: str, role_type_id: int) -> User:
        """Crea un nuovo utente"""
        return self.create(db, name=name, surname=surname, role_type_id=role_type_id)
    
    def get_user_with_relations(self, db: Session, user_id: int) -> Optional[User]:
        """Recupera un utente con tutte le sue relazioni caricate"""
        return db.query(User).options(
            joinedload(User.role_type),
            joinedload(User.contacts),
            joinedload(User.vendors)
        ).filter(User.id == user_id).first()
    
    def get_users_by_role(self, db: Session, role_name: str) -> List[User]:
        """Recupera tutti gli utenti con un ruolo specifico"""
        return db.query(User).join(RoleType).filter(
            RoleType.name == role_name
        ).all()
    
    def get_farmers(self, db: Session) -> List[User]:
        """Recupera tutti gli utenti con ruolo farmer"""
        return self.get_users_by_role(db, "farmer")
    
    def get_consumers(self, db: Session) -> List[User]:
        """Recupera tutti gli utenti con ruolo consumer"""
        return self.get_users_by_role(db, "consumer")
    
    def get_restaurant_owners(self, db: Session) -> List[User]:
        """Recupera tutti i proprietari di ristoranti"""
        return self.get_users_by_role(db, "restaurant_owner")
    
    def update_user_role(self, db: Session, user_id: int, new_role_id: int) -> Optional[User]:
        """Aggiorna il ruolo di un utente"""
        return self.update(db, user_id, role_type_id=new_role_id)
    
    def search_users_by_name(self, db: Session, search_term: str) -> List[User]:
        """Cerca utenti per nome o cognome"""
        return db.query(User).filter(
            (User.name.ilike(f"%{search_term}%")) |
            (User.surname.ilike(f"%{search_term}%"))
        ).all()

# Istanza globale del servizio
user_service = UserService()
