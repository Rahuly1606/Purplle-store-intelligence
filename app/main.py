from fastapi import FastAPI

from app.api.ingestion import router as ingestion_router
from app.api.metrics import router as metrics_router
from app.api.funnel import router as funnel_router
from app.api.heatmap import router as heatmap_router

from app.database.database import engine
from app.database.database import Base

app = FastAPI(
    title="Store Intelligence API",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(ingestion_router)
app.include_router(metrics_router)
app.include_router(funnel_router)
app.include_router(heatmap_router)


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