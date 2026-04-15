from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional

class UserCreate(BaseModel):
    name:str = Field(..., min_length=2, max_length=100)
    email : EmailStr= Field(...)
    password: str = Field(..., min_length =4, max_length=64)

    @field_validator("email")
    @classmethod
    def check_length(cls, v):
        v= v.strip().lower()
        if len(v) > 52:
            raise ValueError("Email too long")
        return v

class UserResponse(BaseModel):
    id: int
    name : str
    email : EmailStr

    class Config:
        from_attributes= True