from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
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
