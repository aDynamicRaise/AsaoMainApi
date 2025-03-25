import re
from fastapi import status
from datetime import datetime
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field, ValidationError, field_validator


class UserBase(BaseModel):
    email: str

    @field_validator('email')
    def validate_email(cls, value):
        # Используем регулярное выражение, чтобы проверить формат email 
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        
        if not re.match(email_regex, value):
            raise ValueError("Неверный формат адреса электронной почты. Адрес должен быть по типу: user@example.com")
        return value

class UserLogin(UserBase):
    password: str = Field(max_length=20)
        
    @field_validator('password')
    def validate_password(cls, value):
        value = str(value) 
        if len(value) < 4:
            raise ValueError("Пароль должен содержать не менее 4 символов")
        if len(value) > 20:
            raise ValueError("Пароль должен содержать не более 20 символов")
        return value


class UserCreate(UserBase):
    name: str = Field(max_length=20)



class UserRead(UserCreate):
    id: int


class ResponceCreate(BaseModel):
    user_id: int


class UserPassSchema(BaseModel):
    user_id: int
    hash_pass: str = Field(min_length=60)
    date_pass: datetime