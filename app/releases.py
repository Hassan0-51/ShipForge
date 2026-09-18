from pydantic import BaseModel


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