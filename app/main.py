from fastapi import FastAPI

from app.releases import Release, create_release, get_releases


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


@app.get("/releases")
def releases():
    return get_releases()


@app.post("/releases")
def add_release(release: Release):
    return create_release(release)