from pydantic import BaseModel, EmailStr

# Pydantic model for the user
class SignUp(BaseModel):
    email: EmailStr
    name: str
    password: str

class SignIn(BaseModel):
    email: EmailStr
    password: str