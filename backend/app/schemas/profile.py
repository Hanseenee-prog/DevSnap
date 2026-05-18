from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Pydantic model for the user profile
class ProfileCreate(BaseModel):
    username: int
    bio: str
    gender: str
    avatar_url: Optional[str]

class ProfileResponse(BaseModel):
    id: int
    username: int
    bio: str
    gender: str
    avatar_url: str
    created_at: datetime