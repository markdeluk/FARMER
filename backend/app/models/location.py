from sqlalchemy import Column, Integer, String, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base


class Location(Base):
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True, index=True)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    address = Column(String, nullable=False)
    zip = Column(String, nullable=False)
    
    # Relationships
    vendors = relationship("Vendor", back_populates="location")


class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    contact_info_type_id = Column(Integer, ForeignKey("contact_info_types.id"), nullable=False)
    contact_info = Column(String, nullable=False)
    
    __table_args__ = (
        UniqueConstraint('user_id', 'contact_info_type_id', name='unique_user_contact_type'),
    )
    
    # Relationships
    user = relationship("User", back_populates="contacts")
    contact_info_type = relationship("ContactInfoType", back_populates="contacts")
