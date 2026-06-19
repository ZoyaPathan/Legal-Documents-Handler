from pydantic import BaseModel, Field, EmailStr
from typing import Literal

class UserAuth(BaseModel):
    """Schema that is used for user input during signup or login."""
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)
    role: Literal["client", "lawyer"] 

class UserOut(BaseModel):
    """"Schema that defines what is sent back to the client."""
    id: str
    username: str 
    email: str
    role: str

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class Document(BaseModel):
    title: str
    content: str