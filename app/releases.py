from pydantic import BaseModel, ConfigDict
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
    version: str
    environment: str
    status: str


class ReleaseResponse(BaseModel):
    id: int
    version: str
    environment: str
    status: str

    model_config = ConfigDict(from_attributes=True)

def get_releases(db: Session):
    return db.query(ReleaseDB).all()


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