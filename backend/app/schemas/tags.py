from pydantic import BaseModel

# Pydantic model for the tags
class TagResponse(BaseModel):
    id: int
    name: str