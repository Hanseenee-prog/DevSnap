from pydantic import BaseModel

# Pydantic model for the user
class User(BaseModel):
    id: int
    email: str
    full_name: str