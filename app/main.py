from fastapi import FastAPI

app = FastAPI(
    title="ShipForge",
    description="A DevOps learning project for managing software releases.",
    version="1.0.0"
)


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