from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class RoleTypeEnum(PyEnum):
    CONSUMER = "consumer"
    FARMER = "farmer"
    PRODUCER = "producer"
    RESTAURANT_OWNER = "restaurant_owner"
    WORKSHOP_HOST = "workshop_host"
    EVENT_ORGANIZER = "event_organizer"
    ADMIN = "admin"


class ContactInfoTypeEnum(PyEnum):
    TELEPHONE = "telephone"
    EMAIL = "email"


class DayWeekEnum(PyEnum):
    MONDAY = "mon"
    TUESDAY = "tue"
    WEDNESDAY = "wed"
    THURSDAY = "thu"
    FRIDAY = "fri"
    SATURDAY = "sat"
    SUNDAY = "sun"


class ProductCategoryEnum(PyEnum):
    FRUIT = "fruit"
    VEGETABLE = "vegetable"
    SPICE = "spice"


class UnitMeasureEnum(PyEnum):
    KILOGRAM = "kg"
    LITER = "lt"
    GRAM = "g"
    MILLILITER = "ml"


class RatingEnum(PyEnum):
    VERY_BAD = "very bad"
    BAD = "bad"
    AVERAGE = "average"
    GOOD = "good"
    VERY_GOOD = "very good"


class RequestStatusEnum(PyEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class CropTypeEnum(PyEnum):
    BASIL = "basil"
    MINT = "mint"
    STRAWBERRIES = "strawberries"
    CHERRY_TOMATOES = "cherry tomatoes"


# Database tables for enums
class RoleType(Base):
    __tablename__ = "role_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    
    # Relationships
    users = relationship("User", back_populates="role_type")


class ContactInfoType(Base):
    __tablename__ = "contact_info_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    # Relationships
    contacts = relationship("Contact", back_populates="contact_info_type")


class DayWeek(Base):
    __tablename__ = "day_weeks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    # Relationships
    opening_hours = relationship("OpeningHour", back_populates="day_week")
    workshops = relationship("Workshop", back_populates="day_week")


class ProductCategory(Base):
    __tablename__ = "product_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    # Relationships
    products = relationship("Product", back_populates="category")


class UnitMeasure(Base):
    __tablename__ = "unit_measures"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    # Relationships
    products = relationship("Product", back_populates="unit_measure")


class Rating(Base):
    __tablename__ = "ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    # Relationships
    reviews = relationship("Review", back_populates="rating")


class RequestStatus(Base):
    __tablename__ = "request_statuses"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    # Relationships
    request_flows = relationship("RequestFlow", back_populates="request_status")


class CropType(Base):
    __tablename__ = "crop_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    # Relationships
    station_bookings = relationship("StationBooking", back_populates="crop_type")


class MenuCategory(Base):
    __tablename__ = "menu_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    # Relationships
    menu_items = relationship("MenuItem", back_populates="menu_category")
