from pydantic import BaseModel
from datetime import datetime


class ServiceCreate(BaseModel):
    name: str
    price: int


class Service(BaseModel):
    id: int
    name: str
    price: int


class AppointmentCreate(BaseModel):
    client_name: str
    phone: str
    car: str
    service_id: int
    appointment_date: datetime
    comment: str | None = None


class Appointment(AppointmentCreate):
    id: int
    service: Service

    class Config:
        from_attributes = True