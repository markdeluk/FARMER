from fastapi import APIRouter
from app.api.controllers import (
    auth_controller,
    base_controller,
    consumer_controller, 
    farmer_controller,
    restaurant_owner_controller,
    admin_controller,
    workshop_host_controller,
    event_organizer_controller
)

# Costante per il prefisso API
API_V1_PREFIX = "/api/v1"

# Router principale che include tutti i controller
api_router = APIRouter()

# Include il controller di autenticazione (senza prefisso stakeholder)
api_router.include_router(
    auth_controller.router,
    prefix=API_V1_PREFIX,
    tags=["Authentication"]
)

# Include tutti i router dei controller stakeholder
api_router.include_router(
    consumer_controller.router,
    prefix=API_V1_PREFIX,
    tags=["Consumer"]
)

api_router.include_router(
    farmer_controller.router,
    prefix=API_V1_PREFIX, 
    tags=["Farmer"]
)

api_router.include_router(
    restaurant_owner_controller.router,
    prefix=API_V1_PREFIX,
    tags=["Restaurant Owner"] 
)

api_router.include_router(
    admin_controller.router,
    prefix=API_V1_PREFIX,
    tags=["Admin"]
)

api_router.include_router(
    workshop_host_controller.router,
    prefix=API_V1_PREFIX,
    tags=["Workshop Host"]
)

api_router.include_router(
    event_organizer_controller.router,
    prefix=API_V1_PREFIX,
    tags=["Event Organizer"]
)
