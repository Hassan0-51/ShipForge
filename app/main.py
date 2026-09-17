from datetime import datetime

from fastapi import FastAPI

from app.releases import Release


app = FastAPI(
    title="ShipForge",
    description="A DevOps learning project for managing software releases.",
    version="1.0.0"
)


releases = [
    Release(
        id=1,
        version="v1.0.0",
        environment="development",
        status="deployed",
        created_at=datetime.now(),
    )
]


@app.get("/")
def root():
    return {
        "application": "ShipForge",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/releases")
def get_releases():
    return releases