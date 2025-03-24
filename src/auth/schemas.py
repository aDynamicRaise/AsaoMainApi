from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(max_length=20)

    @field_validator('password')
    def validate_password(cls, v):
        assert len(v) >= 4, 'password must be at least 4 characters'
        return v


class UserCreate(BaseModel):
    name: str = Field(max_length=20)
    email: EmailStr


class UserRead(UserCreate):
    id: int

