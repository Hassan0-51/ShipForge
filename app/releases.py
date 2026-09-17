from datetime import datetime

from pydantic import BaseModel


class Release(BaseModel):
    id: int
    version: str
    environment: str
    status: str
    created_at: datetime