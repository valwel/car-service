from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Service
from app.schemas import Service as ServiceSchema, ServiceCreate

router = APIRouter()


@router.get("/api/services", response_model=list[ServiceSchema])
def get_services(db: Session = Depends(get_db)):
    return db.query(Service).all()

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