from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.location import Location
from app.services.base_service import BaseService
import math

class LocationService(BaseService[Location]):
    """Servizio per operazioni CRUD su Location"""
    
    def __init__(self):
        super().__init__(Location)
    
    def create_location(self, db: Session, lat: float, lon: float, address: str, zip: str) -> Location:
        """Crea una nuova location"""
        return self.create(
            db,
            lat=lat,
            lon=lon,
            address=address,
            zip=zip
        )
    
    def search_by_address(self, db: Session, search_term: str) -> List[Location]:
        """Cerca location per indirizzo"""
        return db.query(Location).filter(
            Location.address.ilike(f"%{search_term}%")
        ).all()
    
    def search_by_zip(self, db: Session, zip_code: str) -> List[Location]:
        """Cerca location per CAP"""
        return self.filter_by(db, zip=zip_code)
    
    def get_locations_in_radius(self, db: Session, center_lat: float, center_lon: float, radius_km: float) -> List[Location]:
        """Recupera location entro un raggio specificato (usando formula haversine approssimata)"""
        # Formula semplificata per esempio (per produzione usare PostGIS o calcolo più preciso)
        lat_diff = radius_km / 111.0  # 1 grado di latitudine ≈ 111 km
        lon_diff = radius_km / (111.0 * abs(math.cos(math.radians(center_lat))))
        
        return db.query(Location).filter(
            Location.lat.between(center_lat - lat_diff, center_lat + lat_diff),
            Location.lon.between(center_lon - lon_diff, center_lon + lon_diff)
        ).all()
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calcola la distanza tra due punti usando la formula haversine (in km)"""
        # Converti gradi in radianti
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Formula haversine
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371  # Raggio della Terra in km
        
        return c * r
    
    def get_nearest_locations(self, db: Session, center_lat: float, center_lon: float, limit: int = 10) -> List[dict]:
        """Recupera le location più vicine a un punto specificato"""
        # Per un'implementazione più efficiente, usare database con supporto geospaziale
        all_locations = self.get_all(db)
        
        locations_with_distance = []
        for location in all_locations:
            distance = self.calculate_distance(center_lat, center_lon, location.lat, location.lon)
            locations_with_distance.append({
                "location": location,
                "distance_km": round(distance, 2)
            })
        
        # Ordina per distanza e limita risultati
        locations_with_distance.sort(key=lambda x: x["distance_km"])
        return locations_with_distance[:limit]
    
    def update_coordinates(self, db: Session, location_id: int, new_lat: float, new_lon: float) -> Optional[Location]:
        """Aggiorna le coordinate di una location"""
        return self.update(db, location_id, lat=new_lat, lon=new_lon)
    
    def update_address(self, db: Session, location_id: int, new_address: str, new_zip: str) -> Optional[Location]:
        """Aggiorna l'indirizzo di una location"""
        return self.update(db, location_id, address=new_address, zip=new_zip)
    
    def validate_coordinates(self, lat: float, lon: float) -> bool:
        """Valida che le coordinate siano nel range corretto"""
        return -90 <= lat <= 90 and -180 <= lon <= 180
    
    def get_locations_by_zip_range(self, db: Session, start_zip: str, end_zip: str) -> List[Location]:
        """Recupera location in un range di CAP"""
        return db.query(Location).filter(
            Location.zip.between(start_zip, end_zip)
        ).all()
    
    def get_unique_zip_codes(self, db: Session) -> List[str]:
        """Recupera tutti i CAP unici nel database"""
        return [zip_code[0] for zip_code in db.query(Location.zip).distinct().all()]
    
    def get_location_statistics(self, db: Session) -> dict:
        """Recupera statistiche sulle location"""
        total_locations = self.count(db)
        unique_zips = len(self.get_unique_zip_codes(db))
        
        # Calcola bounding box
        if total_locations > 0:
            locations = self.get_all(db)
            lats = [loc.lat for loc in locations]
            lons = [loc.lon for loc in locations]
            
            bounding_box = {
                "min_lat": min(lats),
                "max_lat": max(lats),
                "min_lon": min(lons),
                "max_lon": max(lons)
            }
        else:
            bounding_box = None
        
        return {
            "total_locations": total_locations,
            "unique_zip_codes": unique_zips,
            "bounding_box": bounding_box
        }

# Istanza globale del servizio
location_service = LocationService()
