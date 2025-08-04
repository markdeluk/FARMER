from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Time, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base


class RestaurantTable(Base):
    __tablename__ = "restaurant_tables"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    
    # Relationships
    restaurant = relationship("Restaurant", back_populates="tables")
    seats = relationship("RestaurantSeat", back_populates="table")


class RestaurantSeat(Base):
    __tablename__ = "restaurant_seats"
    
    id = Column(Integer, primary_key=True, index=True)
    restaurant_table_id = Column(Integer, ForeignKey("restaurant_tables.id"), nullable=False)
    
    # Relationships
    table = relationship("RestaurantTable", back_populates="seats")
    bookings = relationship("RestaurantBooking", back_populates="restaurant_seat")


class MenuItem(Base):
    __tablename__ = "menu_items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    menu_category_id = Column(Integer, ForeignKey("menu_categories.id"), nullable=False)
    description = Column(String, nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    
    # Relationships
    menu_category = relationship("MenuCategory", back_populates="menu_items")
    restaurant = relationship("Restaurant", back_populates="menu_items")


class RestaurantBooking(Base):
    __tablename__ = "restaurant_bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    restaurant_seat_id = Column(Integer, ForeignKey("restaurant_seats.id"), nullable=False)
    date = Column(Date, nullable=False)
    time_slot = Column(Time, nullable=False)
    
    __table_args__ = (
        UniqueConstraint('user_id', 'restaurant_seat_id', 'date', 'time_slot', name='unique_restaurant_booking'),
    )
    
    # Relationships
    user = relationship("User", back_populates="restaurant_bookings")
    restaurant_seat = relationship("RestaurantSeat", back_populates="bookings")
