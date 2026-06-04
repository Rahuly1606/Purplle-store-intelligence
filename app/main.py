from fastapi import FastAPI

from app.api.ingestion import router as ingestion_router

from app.database.database import engine
from app.database.database import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(ingestion_router)


@app.get("/")
def root():
    return {
        "message": "Store Intelligence Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }