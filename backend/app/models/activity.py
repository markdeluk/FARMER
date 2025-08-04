from sqlalchemy import Column, Integer, Float, ForeignKey, Date, Time, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base


class Workshop(Base):
    __tablename__ = "workshops"
    
    id = Column(Integer, ForeignKey("activities.id"), primary_key=True)
    day_week_id = Column(Integer, ForeignKey("day_weeks.id"), nullable=False)
    
    # Relationships
    activity = relationship("Activity", back_populates="workshop")
    day_week = relationship("DayWeek", back_populates="workshops")
    seats = relationship("WorkshopSeat", back_populates="workshop")


class WorkshopSeat(Base):
    __tablename__ = "workshop_seats"
    
    id = Column(Integer, primary_key=True, index=True)
    workshop_id = Column(Integer, ForeignKey("workshops.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    workshop = relationship("Workshop", back_populates="seats")
    user = relationship("User", back_populates="workshop_seats")
    enrollments = relationship("WorkshopEnrollment", back_populates="workshop_seat")


class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, ForeignKey("activities.id"), primary_key=True)
    date = Column(Date, nullable=False)
    organizer_fee = Column(Float, nullable=False)
    
    # Relationships
    activity = relationship("Activity", back_populates="event")
    seats = relationship("EventSeat", back_populates="event")
    request_flows = relationship("EventRequestFlow", back_populates="event")


class EventSeat(Base):
    __tablename__ = "event_seats"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    event = relationship("Event", back_populates="seats")
    user = relationship("User", back_populates="event_seats")
    enrollments = relationship("EventEnrollment", back_populates="event_seat")


class WorkshopEnrollment(Base):
    __tablename__ = "workshop_enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    workshop_seat_id = Column(Integer, ForeignKey("workshop_seats.id"), nullable=False)
    date = Column(Date, nullable=False)
    
    __table_args__ = (
        UniqueConstraint('user_id', 'workshop_seat_id', 'date', name='unique_workshop_enrollment'),
    )
    
    # Relationships
    user = relationship("User", back_populates="workshop_enrollments")
    workshop_seat = relationship("WorkshopSeat", back_populates="enrollments")


class EventEnrollment(Base):
    __tablename__ = "event_enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_seat_id = Column(Integer, ForeignKey("event_seats.id"), nullable=False)
    
    __table_args__ = (
        UniqueConstraint('user_id', 'event_seat_id', name='unique_event_enrollment'),
    )
    
    # Relationships
    user = relationship("User", back_populates="event_enrollments")
    event_seat = relationship("EventSeat", back_populates="enrollments")
