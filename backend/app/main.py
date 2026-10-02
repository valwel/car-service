from fastapi import FastAPI
from app.db.database import Base, engine
from app.db import models
from app.services import router as services_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(services_router)

@app.get("/")
def root():
    return {"message": "Car service API"}