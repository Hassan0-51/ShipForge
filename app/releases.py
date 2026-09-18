
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

from app.database import Base

class Release(BaseModel):
    version: str
    environment: str
    status: str


releases = []


def get_releases():
    return releases


def create_release(release: Release):
    releases.append(release)
    return release




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