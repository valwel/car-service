from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100)
    )

    price: Mapped[int]

    appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="service"
    )


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    car = Column(String, nullable=False)
    service_id = Column(
        Integer,
        ForeignKey("services.id"),
        nullable=False
    )
    appointment_date = Column(DateTime, nullable=False)
    comment = Column(String, nullable=True)

    service: Mapped["Service"] = relationship(
        back_populates="appointments"
    )