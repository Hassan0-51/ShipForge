from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from app.database import Base


class ReleaseDB(Base):
    __tablename__ = "releases"

    id = Column(Integer, primary_key=True, index=True)
    version = Column(String, nullable=False)
    environment = Column(String, nullable=False)
    status = Column(String, nullable=False)


class Release(BaseModel):
    version: str = Field(min_length=1)
    environment: str = Field(pattern="^(development|staging|production)$")
    status: str = Field(pattern="^(pending|deployed|failed)$")

class ReleaseResponse(BaseModel):
    id: int
    version: str
    environment: str
    status: str

    model_config = ConfigDict(from_attributes=True)

def get_releases(db: Session, environment: str = None):
    query = db.query(ReleaseDB)

    if environment:
        query = query.filter(ReleaseDB.environment == environment)

    return query.all()

def create_release(db: Session, release: Release):
    new_release = ReleaseDB(
        version=release.version,
        environment=release.environment,
        status=release.status
    )

    db.add(new_release)
    db.commit()
    db.refresh(new_release)

    return new_release

def get_release(db: Session, release_id: int):
    return db.query(ReleaseDB).filter(ReleaseDB.id == release_id).first()

def delete_release(db: Session, release_id: int):
    release = get_release(db, release_id)

    if release is None:
        return None

    db.delete(release)
    db.commit()

    return release

def update_release(db: Session, release_id: int, release: Release):
    existing_release = get_release(db, release_id)

    if existing_release is None:
        return None

    existing_release.version = release.version
    existing_release.environment = release.environment
    existing_release.status = release.status

    db.commit()
    db.refresh(existing_release)

    return existing_release