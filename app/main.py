from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.releases import (
    Release,
    ReleaseDB,
    DeploymentDB,
    ReleaseResponse,
    DeploymentResponse,
    create_release,
    get_releases,
    get_release,
    get_deployment_stats,
    delete_release,
    update_release,
    get_release_stats,
    search_releases,
    deploy_release
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

@app.post("/releases/{release_id}/deploy", response_model=ReleaseResponse)
def deploy_release_by_id(
    release_id: int,
    db: Session = Depends(get_db)
):
    release = deploy_release(db, release_id)

    if release is None:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404,
            detail="Release not found"
        )

    if release is False:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=409,
            detail="Release cannot be deployed from its current status"
        )

    return release

@app.get("/releases/{release_id}/deployments", response_model=list[DeploymentResponse])
def get_release_deployments(release_id: int, db: Session = Depends(get_db)):
    release = db.query(ReleaseDB).filter(ReleaseDB.id == release_id).first()

    if not release:
        raise HTTPException(status_code=404, detail="Release not found")

    return (
        db.query(DeploymentDB)
        .filter(DeploymentDB.release_id == release_id)
        .order_by(DeploymentDB.created_at.desc())
        .all()
    )
    
@app.get("/deployments/stats")
def deployment_stats(
    db: Session = Depends(get_db)
):
    return get_deployment_stats(db)