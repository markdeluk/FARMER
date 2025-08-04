from sqlalchemy import Column, Integer, String, ForeignKey, Time
from sqlalchemy.orm import relationship
from app.db.base import Base


class Vendor(Base):
    __tablename__ = "vendors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    location = relationship("Location", back_populates="vendors")
    owner = relationship("User", back_populates="vendors")
    opening_hours = relationship("OpeningHour", back_populates="vendor")
    vendor_reviews = relationship("VendorReview", back_populates="vendor")
    
    # Polymorphic relationships
    market = relationship("Market", back_populates="vendor", uselist=False)
    restaurant = relationship("Restaurant", back_populates="vendor", uselist=False)
    activity = relationship("Activity", back_populates="vendor", uselist=False)
    warehouse = relationship("Warehouse", back_populates="vendor", uselist=False)


class OpeningHour(Base):
    __tablename__ = "opening_hours"
    
    id = Column(Integer, primary_key=True, index=True)
    day_week_id = Column(Integer, ForeignKey("day_weeks.id"), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    
    # Relationships
    day_week = relationship("DayWeek", back_populates="opening_hours")
    vendor = relationship("Vendor", back_populates="opening_hours")


class Market(Base):
    __tablename__ = "markets"
    
    id = Column(Integer, ForeignKey("vendors.id"), primary_key=True)
    
    # Relationships
    vendor = relationship("Vendor", back_populates="market")
    products = relationship("Product", back_populates="market")


class Restaurant(Base):
    __tablename__ = "restaurants"
    
    id = Column(Integer, ForeignKey("vendors.id"), primary_key=True)
    
    # Relationships
    vendor = relationship("Vendor", back_populates="restaurant")
    tables = relationship("RestaurantTable", back_populates="restaurant")
    menu_items = relationship("MenuItem", back_populates="restaurant")


class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, ForeignKey("vendors.id"), primary_key=True)
    capacity = Column(Integer, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    
    # Relationships
    vendor = relationship("Vendor", back_populates="activity")
    workshop = relationship("Workshop", back_populates="activity", uselist=False)
    event = relationship("Event", back_populates="activity", uselist=False)


class Warehouse(Base):
    __tablename__ = "warehouses"
    
    id = Column(Integer, ForeignKey("vendors.id"), primary_key=True)
    
    # Relationships
    vendor = relationship("Vendor", back_populates="warehouse")
    warehouse_rows = relationship("WarehouseRow", back_populates="warehouse")
