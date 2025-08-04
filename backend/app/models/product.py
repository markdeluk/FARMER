from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Time, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    market_id = Column(Integer, ForeignKey("markets.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey("product_categories.id"), nullable=False)
    unit_weight = Column(Float, nullable=False)
    unit_measure_id = Column(Integer, ForeignKey("unit_measures.id"), nullable=False)
    
    # Relationships
    market = relationship("Market", back_populates="products")
    category = relationship("ProductCategory", back_populates="products")
    unit_measure = relationship("UnitMeasure", back_populates="products")
    daily_availabilities = relationship("ProductDailyAvailability", back_populates="product")
    reservations = relationship("ProductReservation", back_populates="product")
    product_reviews = relationship("ProductReview", back_populates="product")


class ProductDailyAvailability(Base):
    __tablename__ = "product_daily_availabilities"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    date = Column(Date, nullable=False)
    available_quantity = Column(Integer, nullable=False)
    daily_price = Column(Float, nullable=False)
    discounted_price = Column(Float, nullable=True)
    start_time_discount = Column(Time, nullable=True)
    end_time_discount = Column(Time, nullable=True)
    
    __table_args__ = (
        UniqueConstraint('product_id', 'date', name='unique_product_date'),
    )
    
    # Relationships
    product = relationship("Product", back_populates="daily_availabilities")


class ProductReservation(Base):
    __tablename__ = "product_reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    date = Column(Date, nullable=False)
    time_slot = Column(Time, nullable=False)
    desired_quantity = Column(Integer, nullable=False)
    
    __table_args__ = (
        UniqueConstraint('user_id', 'product_id', 'date', 'time_slot', name='unique_user_product_reservation'),
    )
    
    # Relationships
    user = relationship("User", back_populates="product_reservations")
    product = relationship("Product", back_populates="reservations")
