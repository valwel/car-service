from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Service, Appointment
from app.schemas import (
    Service as ServiceSchema,
    ServiceCreate,
    Appointment as AppointmentSchema,
    AppointmentCreate,
)

router = APIRouter()


@router.get("/api/services", response_model=list[ServiceSchema])
def get_services(db: Session = Depends(get_db)):
    return db.query(Service).all()


@router.get("/api/services/{service_id}", response_model=ServiceSchema)
def get_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id). first()

    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    return service


@router.post("/api/services", response_model=ServiceSchema)
def create_service(
    service: ServiceCreate,
    db: Session = Depends(get_db)
):
    new_service = Service(
        name=service.name,
        price=service.price
    )

    db.add(new_service)
    db.commit()
    db.refresh(new_service)

    return new_service


@router.put("/api/services/{service_id}", response_model=ServiceSchema)
def update_service(
    service_id: int,
    service: ServiceCreate,
    db: Session = Depends(get_db)
):
    existing_service = (db.query(Service).filter(Service.id == service_id).first())

    if existing_service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    existing_service.name = service.name
    existing_service.price = service.price

    db.commit()
    db.refresh(existing_service)

    return existing_service


@router.delete("/api/services/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id). first()

    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    db.delete(service)
    db.commit()

    return {"message": "Service deleted"}


@router.post("/api/appointments", response_model=AppointmentSchema)
def create_appointment( appointment: AppointmentCreate, db: Session = Depends(get_db)):
    service = (db.query(Service).filter(Service.id == appointment.service_id).first())

    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    new_appointment = Appointment(
        client_name=appointment.client_name,
        phone=appointment.phone,
        car=appointment.car,
        service_id=appointment.service_id,
        appointment_date=appointment.appointment_date,
        comment=appointment.comment
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return new_appointment


@router.get("/api/appointments", response_model=list[AppointmentSchema])
def get_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).all()


@router.get("/api/appointments/{appointment_id}", response_model=AppointmentSchema)
def get_appointments(appointment_id: int, db: Session = Depends(get_db)):
    appointment = (db.query(Appointment).filter(Appointment.id == appointment_id).first())

    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return appointment


@router.put(
    "/api/appointments/{appointment_id}",
    response_model=AppointmentSchema
)
def update_appointment(
    appointment_id: int,
    appointment: AppointmentCreate,
    db: Session = Depends(get_db)
):
    existing_appointment = (
        db.query(Appointment)
        .filter(Appointment.id == appointment_id)
        .first()
    )

    if existing_appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    service = (
        db.query(Service)
        .filter(Service.id == appointment.service_id)
        .first()
    )

    if service is None:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    existing_appointment.client_name = appointment.client_name
    existing_appointment.phone = appointment.phone
    existing_appointment.car = appointment.car
    existing_appointment.service_id = appointment.service_id
    existing_appointment.appointment_date = appointment.appointment_date
    existing_appointment.comment = appointment.comment

    db.commit()
    db.refresh(existing_appointment)

    return existing_appointment


@router.delete("/api/appointments/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    appointment = (
        db.query(Appointment)
        .filter(Appointment.id == appointment_id)
        .first()
    )

    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    db.delete(appointment)
    db.commit()

    return {"message": "Appointment deleted"}