from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, func, desc
from app.models.review import Review, VendorReview, ProductReview
from app.models.enums import Rating
from app.services.base_service import BaseService

class ReviewService(BaseService[Review]):
    """Servizio per operazioni CRUD su Review"""
    
    def __init__(self):
        super().__init__(Review)
    
    def create_review(self, db: Session, rating_id: int, comment: str, date: date) -> Review:
        """Crea una nuova recensione"""
        return self.create(
            db,
            rating_id=rating_id,
            comment=comment,
            date=date
        )
    
    def get_review_with_rating(self, db: Session, review_id: int) -> Optional[Review]:
        """Recupera una recensione con il rating"""
        return db.query(Review).options(
            joinedload(Review.rating)
        ).filter(Review.id == review_id).first()
    
    def get_reviews_by_rating(self, db: Session, rating_name: str) -> List[Review]:
        """Recupera recensioni per valore di rating"""
        return db.query(Review).join(Rating).filter(
            Rating.name == rating_name
        ).all()
    
    def get_recent_reviews(self, db: Session, limit: int = 10) -> List[Review]:
        """Recupera le recensioni più recenti"""
        return db.query(Review).order_by(desc(Review.date)).limit(limit).all()

class VendorReviewService(BaseService[VendorReview]):
    """Servizio per operazioni CRUD su VendorReview"""
    
    def __init__(self):
        super().__init__(VendorReview)
    
    def create_vendor_review(self, db: Session, user_id: int, vendor_id: int, 
                           rating_id: int, comment: str) -> Optional[VendorReview]:
        """Crea una nuova recensione per un vendor"""
        try:
            # Prima crea la review base
            review = Review(
                rating_id=rating_id,
                comment=comment,
                date=date.today()
            )
            db.add(review)
            db.flush()  # Per ottenere l'ID
            
            # Poi crea la vendor review
            vendor_review = VendorReview(
                id=review.id,
                user_id=user_id,
                vendor_id=vendor_id
            )
            db.add(vendor_review)
            db.commit()
            db.refresh(vendor_review)
            
            return vendor_review
            
        except IntegrityError:
            db.rollback()
            return None  # Utente ha già recensito questo vendor
    
    def get_vendor_reviews(self, db: Session, vendor_id: int) -> List[VendorReview]:
        """Recupera tutte le recensioni di un vendor"""
        return db.query(VendorReview).options(
            joinedload(VendorReview.review).joinedload(Review.rating),
            joinedload(VendorReview.user)
        ).filter(VendorReview.vendor_id == vendor_id).all()
    
    def get_user_vendor_reviews(self, db: Session, user_id: int) -> List[VendorReview]:
        """Recupera tutte le recensioni fatte da un utente ai vendor"""
        return db.query(VendorReview).options(
            joinedload(VendorReview.review).joinedload(Review.rating),
            joinedload(VendorReview.vendor)
        ).filter(VendorReview.user_id == user_id).all()
    
    def get_vendor_average_rating(self, db: Session, vendor_id: int) -> Optional[float]:
        """Calcola il rating medio di un vendor"""
        # Assumendo che i rating abbiano valori numerici: 1=very bad, 2=bad, 3=average, 4=good, 5=very good
        rating_values = {
            "very bad": 1,
            "bad": 2,
            "average": 3,
            "good": 4,
            "very good": 5
        }
        
        reviews = self.get_vendor_reviews(db, vendor_id)
        if not reviews:
            return None
        
        total_rating = sum(rating_values.get(review.review.rating.name, 3) for review in reviews)
        return total_rating / len(reviews)
    
    def get_vendor_rating_distribution(self, db: Session, vendor_id: int) -> dict:
        """Ottiene la distribuzione dei rating per un vendor"""
        reviews = db.query(VendorReview).join(Review).join(Rating).filter(
            VendorReview.vendor_id == vendor_id
        ).all()
        
        distribution = {
            "very bad": 0,
            "bad": 0,
            "average": 0,
            "good": 0,
            "very good": 0
        }
        
        for review in reviews:
            rating_name = review.review.rating.name
            if rating_name in distribution:
                distribution[rating_name] += 1
        
        return distribution
    
    def user_has_reviewed_vendor(self, db: Session, user_id: int, vendor_id: int) -> bool:
        """Verifica se un utente ha già recensito un vendor"""
        review = db.query(VendorReview).filter(
            and_(
                VendorReview.user_id == user_id,
                VendorReview.vendor_id == vendor_id
            )
        ).first()
        
        return review is not None

class ProductReviewService(BaseService[ProductReview]):
    """Servizio per operazioni CRUD su ProductReview"""
    
    def __init__(self):
        super().__init__(ProductReview)
    
    def create_product_review(self, db: Session, user_id: int, product_id: int, 
                            rating_id: int, comment: str) -> Optional[ProductReview]:
        """Crea una nuova recensione per un prodotto"""
        try:
            # Prima crea la review base
            review = Review(
                rating_id=rating_id,
                comment=comment,
                date=date.today()
            )
            db.add(review)
            db.flush()  # Per ottenere l'ID
            
            # Poi crea la product review
            product_review = ProductReview(
                id=review.id,
                user_id=user_id,
                product_id=product_id
            )
            db.add(product_review)
            db.commit()
            db.refresh(product_review)
            
            return product_review
            
        except IntegrityError:
            db.rollback()
            return None  # Utente ha già recensito questo prodotto
    
    def get_product_reviews(self, db: Session, product_id: int) -> List[ProductReview]:
        """Recupera tutte le recensioni di un prodotto"""
        return db.query(ProductReview).options(
            joinedload(ProductReview.review).joinedload(Review.rating),
            joinedload(ProductReview.user)
        ).filter(ProductReview.product_id == product_id).all()
    
    def get_user_product_reviews(self, db: Session, user_id: int) -> List[ProductReview]:
        """Recupera tutte le recensioni fatte da un utente ai prodotti"""
        return db.query(ProductReview).options(
            joinedload(ProductReview.review).joinedload(Review.rating),
            joinedload(ProductReview.product)
        ).filter(ProductReview.user_id == user_id).all()
    
    def get_product_average_rating(self, db: Session, product_id: int) -> Optional[float]:
        """Calcola il rating medio di un prodotto"""
        rating_values = {
            "very bad": 1,
            "bad": 2,
            "average": 3,
            "good": 4,
            "very good": 5
        }
        
        reviews = self.get_product_reviews(db, product_id)
        if not reviews:
            return None
        
        total_rating = sum(rating_values.get(review.review.rating.name, 3) for review in reviews)
        return total_rating / len(reviews)
    
    def get_top_rated_products(self, db: Session, limit: int = 10) -> List[dict]:
        """Recupera i prodotti con il rating più alto"""
        # Query complessa che calcola il rating medio per prodotto
        # Questo è un esempio semplificato
        product_reviews = db.query(ProductReview).options(
            joinedload(ProductReview.product),
            joinedload(ProductReview.review).joinedload(Review.rating)
        ).all()
        
        # Raggruppa per prodotto e calcola rating medio
        product_ratings = {}
        for review in product_reviews:
            product_id = review.product_id
            rating_value = {
                "very bad": 1, "bad": 2, "average": 3, "good": 4, "very good": 5
            }.get(review.review.rating.name, 3)
            
            if product_id not in product_ratings:
                product_ratings[product_id] = {"ratings": [], "product": review.product}
            
            product_ratings[product_id]["ratings"].append(rating_value)
        
        # Calcola medie e ordina
        products_with_avg = []
        for product_id, data in product_ratings.items():
            avg_rating = sum(data["ratings"]) / len(data["ratings"])
            products_with_avg.append({
                "product": data["product"],
                "average_rating": avg_rating,
                "review_count": len(data["ratings"])
            })
        
        # Ordina per rating medio decrescente
        products_with_avg.sort(key=lambda x: x["average_rating"], reverse=True)
        
        return products_with_avg[:limit]
    
    def user_has_reviewed_product(self, db: Session, user_id: int, product_id: int) -> bool:
        """Verifica se un utente ha già recensito un prodotto"""
        review = db.query(ProductReview).filter(
            and_(
                ProductReview.user_id == user_id,
                ProductReview.product_id == product_id
            )
        ).first()
        
        return review is not None

# Istanze globali dei servizi
review_service = ReviewService()
vendor_review_service = VendorReviewService()
product_review_service = ProductReviewService()
