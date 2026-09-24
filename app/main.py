from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.releases import (
    Release,
    ReleaseDB,
    ReleaseResponse,
    create_release,
    get_releases,
    get_release,
    delete_release,
    update_release,
    get_release_stats,
    search_releases
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
        "status": "ok",
        "service": "ShipForge"
    }
    
@app.get("/releases/stats")
def release_stats(
    db: Session = Depends(get_db)
):
    return get_release_stats(db)

@app.get("/releases", response_model=list[ReleaseResponse])
def releases(
    environment: str = None,
    status: str = None,
    skip: int = 0,
    limit: int = None,
    db: Session = Depends(get_db)
):
    return get_releases(db, environment, status, skip, limit)

@app.post("/releases", response_model=ReleaseResponse)
def add_release(
    release: Release,
    db: Session = Depends(get_db)
):
    return create_release(db, release)

@app.get("/releases/search", response_model=list[ReleaseResponse])
def search_release_versions(
    version: str,
    db: Session = Depends(get_db)
):
    return search_releases(db, version)

@app.get("/releases/{release_id}", response_model=ReleaseResponse)
def release_by_id(
    release_id: int,
    db: Session = Depends(get_db)
):
    release = get_release(db, release_id)

    if release is None:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=404,
            detail="Release not found"
        )

    return release

@app.delete("/releases/{release_id}")
def delete_release_by_id(
    release_id: int,
    db: Session = Depends(get_db)
):
    release = delete_release(db, release_id)

    if release is None:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=404,
            detail="Release not found"
        )

    return {
        "message": "Release deleted successfully",
        "id": release.id
    }
    
@app.put("/releases/{release_id}", response_model=ReleaseResponse)
def update_release_by_id(
    release_id: int,
    release: Release,
    db: Session = Depends(get_db)
):
    updated_release = update_release(db, release_id, release)

    if updated_release is None:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=404,
            detail="Release not found"
        )

    return updated_release