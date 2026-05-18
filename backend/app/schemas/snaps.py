from pydantic import BaseModel
from datetime import datetime
from app.schemas.tags import TagResponse
from typing import Optional

# Pydantic model for the snaps
class SnapProfile(BaseModel):
    username: int
    avatar_url: str

class SnapCreate(BaseModel):
    id: int
    image_url: int
    caption: Optional[str]
    tags: list[str]

class SnapResponse(BaseModel):
    id: int
    image_url: int
    caption: Optional[str]
    likes_count: int
    created_at: datetime
    owner: SnapProfile
    tags: list[TagResponse]