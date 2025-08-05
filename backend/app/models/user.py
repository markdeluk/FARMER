from sqlalchemy import Column, Integer, LargeBinary, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    profile_picture = Column(LargeBinary, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    language = Column(String, default="it", nullable=False)  # Lingua preferita: 'it' o 'en'
    role_type_id = Column(Integer, ForeignKey("role_types.id"), nullable=False)
    
    # Relationships
    role_type = relationship("RoleType", back_populates="users")
    contacts = relationship("Contact", back_populates="user")
    vendors = relationship("Vendor", back_populates="owner")
    product_reservations = relationship("ProductReservation", back_populates="user")
    restaurant_bookings = relationship("RestaurantBooking", back_populates="user")
    vendor_reviews = relationship("VendorReview", back_populates="user")
    product_reviews = relationship("ProductReview", back_populates="user")
    workshop_seats = relationship("WorkshopSeat", back_populates="user")
    event_seats = relationship("EventSeat", back_populates="user")
    workshop_enrollments = relationship("WorkshopEnrollment", back_populates="user")
    event_enrollments = relationship("EventEnrollment", back_populates="user")
    station_bookings = relationship("StationBooking", back_populates="user")
