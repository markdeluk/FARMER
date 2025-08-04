from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.db.base import Base


class WarehouseRow(Base):
    __tablename__ = "warehouse_rows"
    
    id = Column(Integer, primary_key=True, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    
    # Relationships
    warehouse = relationship("Warehouse", back_populates="warehouse_rows")
    shelves = relationship("WarehouseShelf", back_populates="warehouse_row")


class WarehouseShelf(Base):
    __tablename__ = "warehouse_shelves"
    
    id = Column(Integer, primary_key=True, index=True)
    warehouse_row_id = Column(Integer, ForeignKey("warehouse_rows.id"), nullable=False)
    
    # Relationships
    warehouse_row = relationship("WarehouseRow", back_populates="shelves")
    spots = relationship("WarehouseSpot", back_populates="warehouse_shelf")


class WarehouseSpot(Base):
    __tablename__ = "warehouse_spots"
    
    id = Column(Integer, primary_key=True, index=True)
    equipment_details = Column(String, nullable=False)
    farmer_fee = Column(Float, nullable=False)
    warehouse_shelf_id = Column(Integer, ForeignKey("warehouse_shelves.id"), nullable=False)
    
    # Relationships
    warehouse_shelf = relationship("WarehouseShelf", back_populates="spots")
    station_bookings = relationship("StationBooking", back_populates="warehouse_spot")


class StationBooking(Base):
    __tablename__ = "station_bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    warehouse_spot_id = Column(Integer, ForeignKey("warehouse_spots.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    crop_type_id = Column(Integer, ForeignKey("crop_types.id"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="station_bookings")
    warehouse_spot = relationship("WarehouseSpot", back_populates="station_bookings")
    crop_type = relationship("CropType", back_populates="station_bookings")
    request_flows = relationship("StationRequestFlow", back_populates="station_booking")
