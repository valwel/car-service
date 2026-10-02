from pydantic import BaseModel


class ServiceCreate(BaseModel):
    name: str
    price: int


class Service(BaseModel):
    id: int
    name: str
    price: int