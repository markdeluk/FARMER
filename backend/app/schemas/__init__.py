"""
Modelli Pydantic per la documentazione API e validazione dati
Questi modelli vengono usati per generare automaticamente la documentazione Swagger
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime, date
from enum import Enum

# =================== AUTH MODELS ===================
class UserRole(str, Enum):
    ADMIN = "admin"
    FARMER = "farmer"
    CONSUMER = "consumer"
    RESTAURANT_OWNER = "restaurant_owner"
    WORKSHOP_HOST = "workshop_host"
    EVENT_ORGANIZER = "event_organizer"

class RoleInfo(BaseModel):
    """Informazioni complete su un ruolo"""
    id: int
    name: str
    description: Optional[str] = None
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Email dell'utente")
    password: str = Field(..., min_length=6, description="Password (minimo 6 caratteri)")
    
    class Config:
        schema_extra = {
            "example": {
                "email": "mario.rossi@email.com",
                "password": "password123"
            }
        }

class UserRegister(BaseModel):
    email: EmailStr = Field(..., description="Email dell'utente")
    password: str = Field(..., min_length=6, description="Password (minimo 6 caratteri)")
    first_name: str = Field(..., min_length=2, max_length=50, description="Nome")
    last_name: str = Field(..., min_length=2, max_length=50, description="Cognome")
    phone: str = Field(..., description="Numero di telefono")
    role_id: int = Field(..., description="ID del ruolo (1=admin, 2=farmer, 3=consumer, etc.)")
    language: str = Field(default="it", description="Lingua preferita (it/en)")
    profile_picture: Optional[bytes] = Field(None, description="Foto profilo dell'utente (opzionale)")
    
    class Config:
        schema_extra = {
            "example": {
                "email": "mario.rossi@email.com",
                "password": "password123",
                "first_name": "Mario",
                "last_name": "Rossi",
                "phone": "+39 123 456 7890",
                "role_id": 2
            }
        }

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    phone: str
    is_active: bool
    language: str = Field(default="it", description="Lingua preferita dell'utente (it/en)")
    role_id: int = Field(..., description="ID del ruolo utente")
    role_name: str = Field(..., description="Nome del ruolo utente") 
    role_description: Optional[str] = Field(None, description="Descrizione del ruolo utente")
    profile_picture: Optional[bytes] = Field(None, description="Foto profilo dell'utente")
    
    class Config:
        from_attributes = True

class ProfilePictureUpdate(BaseModel):
    profile_picture: bytes = Field(..., description="Nuova foto profilo dell'utente")
    
class ProfilePictureResponse(BaseModel):
    profile_picture: Optional[bytes] = Field(None, description="Foto profilo dell'utente")
    
    class Config:
        from_attributes = True

class LanguageUpdate(BaseModel):
    language: str = Field(..., description="Nuova lingua preferita (it/en)")
    
    class Config:
        schema_extra = {
            "example": {
                "language": "en"
            }
        }

class Token(BaseModel):
    access_token: str = Field(..., description="Token JWT per l'autenticazione")
    token_type: str = Field(default="bearer", description="Tipo di token")
    expires_in: int = Field(..., description="Durata token in secondi")
    user: UserResponse = Field(..., description="Informazioni utente")

# =================== PRODUCT MODELS ===================
class ProductBase(BaseModel):
    name: str = Field(..., max_length=100, description="Nome del prodotto")
    description: Optional[str] = Field(None, description="Descrizione del prodotto")
    category: str = Field(..., description="Categoria del prodotto")
    origin: Optional[str] = Field(None, description="Origine del prodotto")

class ProductCreate(ProductBase):
    class Config:
        schema_extra = {
            "example": {
                "name": "Pomodori San Marzano",
                "description": "Pomodori biologici coltivati in Campania",
                "category": "Ortaggi",
                "origin": "Campania, Italia"
            }
        }

class ProductResponse(ProductBase):
    id: int
    farmer_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# =================== VENDOR MODELS ===================
class VendorType(str, Enum):
    MARKET = "market"
    RESTAURANT = "restaurant"
    ACTIVITY = "activity"
    WAREHOUSE = "warehouse"

class VendorBase(BaseModel):
    name: str = Field(..., max_length=100, description="Nome del vendor")
    description: Optional[str] = Field(None, description="Descrizione del vendor")
    type: VendorType = Field(..., description="Tipo di vendor")

class VendorResponse(VendorBase):
    id: int
    owner_id: int
    location_id: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True

# =================== BOOKING MODELS ===================
class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class BookingCreate(BaseModel):
    restaurant_id: int = Field(..., description="ID del ristorante")
    booking_date: date = Field(..., description="Data della prenotazione")
    booking_time: str = Field(..., description="Ora della prenotazione (HH:MM)")
    party_size: int = Field(..., ge=1, le=20, description="Numero di persone (1-20)")
    special_requests: Optional[str] = Field(None, description="Richieste speciali")
    
    class Config:
        schema_extra = {
            "example": {
                "restaurant_id": 1,
                "booking_date": "2025-08-15",
                "booking_time": "19:30",
                "party_size": 4,
                "special_requests": "Tavolo vicino alla finestra"
            }
        }

class BookingResponse(BaseModel):
    id: int
    user_id: int
    restaurant_id: int
    booking_date: date
    booking_time: str
    party_size: int
    status: BookingStatus
    special_requests: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# =================== REVIEW MODELS ===================
class ReviewRating(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    POOR = "poor"

class ReviewCreate(BaseModel):
    rating: ReviewRating = Field(..., description="Valutazione")
    comment: Optional[str] = Field(None, max_length=500, description="Commento (max 500 caratteri)")
    
    class Config:
        schema_extra = {
            "example": {
                "rating": "excellent",
                "comment": "Prodotti freschi e di alta qualità, servizio eccellente!"
            }
        }

class ReviewResponse(BaseModel):
    id: int
    user_id: int
    vendor_id: int
    rating: ReviewRating
    comment: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# =================== LOCATION MODELS ===================
class LocationCreate(BaseModel):
    name: str = Field(..., max_length=100, description="Nome della location")
    address: str = Field(..., description="Indirizzo completo")
    city: str = Field(..., max_length=50, description="Città")
    postal_code: str = Field(..., max_length=10, description="Codice postale")
    latitude: Optional[float] = Field(None, description="Latitudine")
    longitude: Optional[float] = Field(None, description="Longitudine")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Mercato Centrale",
                "address": "Via Roma 123",
                "city": "Milano",
                "postal_code": "20100",
                "latitude": 45.4642,
                "longitude": 9.1900
            }
        }

class LocationResponse(LocationCreate):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# =================== ERROR MODELS ===================
class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Descrizione dell'errore")
    
    class Config:
        schema_extra = {
            "example": {
                "detail": "User not found"
            }
        }

class ValidationErrorResponse(BaseModel):
    detail: List[dict] = Field(..., description="Lista degli errori di validazione")

# =================== COMMON MODELS ===================
class PaginationParams(BaseModel):
    skip: int = Field(0, ge=0, description="Numero di elementi da saltare")
    limit: int = Field(100, ge=1, le=1000, description="Numero massimo di elementi da restituire")

class PaginatedResponse(BaseModel):
    total: int = Field(..., description="Numero totale di elementi")
    skip: int = Field(..., description="Elementi saltati")
    limit: int = Field(..., description="Limite applicato")

class SuccessResponse(BaseModel):
    message: str = Field(..., description="Messaggio di successo")
    
    class Config:
        schema_extra = {
            "example": {
                "message": "Operation completed successfully"
            }
        }

# =================== DASHBOARD MODELS ===================
class DashboardStats(BaseModel):
    total_products: int = Field(..., description="Numero totale prodotti")
    total_orders: int = Field(..., description="Numero totale ordini")
    total_revenue: float = Field(..., description="Ricavi totali")
    active_bookings: int = Field(..., description="Prenotazioni attive")

class AnalyticsResponse(BaseModel):
    period: str = Field(..., description="Periodo dell'analisi")
    data: dict = Field(..., description="Dati dell'analisi")
    
    class Config:
        schema_extra = {
            "example": {
                "period": "month",
                "data": {
                    "sales": 1500.00,
                    "orders": 45,
                    "customers": 23
                }
            }
        }
