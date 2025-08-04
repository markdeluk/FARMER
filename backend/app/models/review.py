from sqlalchemy import Column, Integer, String, ForeignKey, Date, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base


class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    rating_id = Column(Integer, ForeignKey("ratings.id"), nullable=False)
    comment = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    
    # Relationships
    rating = relationship("Rating", back_populates="reviews")
    vendor_review = relationship("VendorReview", back_populates="review", uselist=False)
    product_review = relationship("ProductReview", back_populates="review", uselist=False)


class VendorReview(Base):
    __tablename__ = "vendor_reviews"
    
    id = Column(Integer, ForeignKey("reviews.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    
    __table_args__ = (
        UniqueConstraint('user_id', 'vendor_id', name='unique_user_vendor_review'),
    )
    
    # Relationships
    review = relationship("Review", back_populates="vendor_review")
    user = relationship("User", back_populates="vendor_reviews")
    vendor = relationship("Vendor", back_populates="vendor_reviews")


class ProductReview(Base):
    __tablename__ = "product_reviews"
    
    id = Column(Integer, ForeignKey("reviews.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    __table_args__ = (
        UniqueConstraint('user_id', 'product_id', name='unique_user_product_review'),
    )
    
    # Relationships
    review = relationship("Review", back_populates="product_review")
    user = relationship("User", back_populates="product_reviews")
    product = relationship("Product", back_populates="product_reviews")
