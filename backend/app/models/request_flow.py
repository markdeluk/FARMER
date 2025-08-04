from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base


class RequestFlow(Base):
    __tablename__ = "request_flows"
    
    id = Column(Integer, primary_key=True, index=True)
    request_status_id = Column(Integer, ForeignKey("request_statuses.id"), nullable=False)
    date_time = Column(DateTime, nullable=False)
    
    # Relationships
    request_status = relationship("RequestStatus", back_populates="request_flows")
    event_request_flow = relationship("EventRequestFlow", back_populates="request_flow", uselist=False)
    station_request_flow = relationship("StationRequestFlow", back_populates="request_flow", uselist=False)


class EventRequestFlow(Base):
    __tablename__ = "event_request_flows"
    
    id = Column(Integer, ForeignKey("request_flows.id"), primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    
    # Relationships
    request_flow = relationship("RequestFlow", back_populates="event_request_flow")
    event = relationship("Event", back_populates="request_flows")


class StationRequestFlow(Base):
    __tablename__ = "station_request_flows"
    
    id = Column(Integer, ForeignKey("request_flows.id"), primary_key=True)
    station_booking_id = Column(Integer, ForeignKey("station_bookings.id"), nullable=False)
    
    # Relationships
    request_flow = relationship("RequestFlow", back_populates="station_request_flow")
    station_booking = relationship("StationBooking", back_populates="request_flows")
