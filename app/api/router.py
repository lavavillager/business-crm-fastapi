from fastapi import APIRouter

from app.api.v1 import (
    activity,
    appointments,
    auth,
    clients,
    employees,
    services,
)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(clients.router)
api_router.include_router(employees.router)
api_router.include_router(services.router)
api_router.include_router(appointments.router)
api_router.include_router(activity.router)
