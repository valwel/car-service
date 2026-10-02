from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Service
from app.schemas import Service as ServiceSchema, ServiceCreate

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
