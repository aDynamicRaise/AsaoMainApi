from pydantic import BaseModel, EmailStr, Field, field_validator


class UserLogin(BaseModel):
    login: str = Field(max_length=60)
    password: str = Field(max_length=20)

    @field_validator('password')
    def validate_password(cls, v):
        assert len(v) >= 4, 'password must be at least 4 characters'
        return v


class UserCreate(UserLogin):
    email: EmailStr


class UserRead(UserCreate):
    id: int

