from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.releases import (
    Release,
    ReleaseDB,
    ReleaseResponse,
    create_release,
    get_releases,
    get_release
)


Base.metadata.create_all(bind=engine)

app = FastAPI(title="ShipForge")


@app.get("/")
def root():
    return {
        "application": "ShipForge",
        "version": "0.1.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/releases", response_model=list[ReleaseResponse])
def releases(db: Session = Depends(get_db)):
    return get_releases(db)


@app.post("/releases", response_model=ReleaseResponse)
def add_release(
    release: Release,
    db: Session = Depends(get_db)
):
    return create_release(db, release)