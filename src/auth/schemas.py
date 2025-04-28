import re
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ValidationError, field_validator


class UserBase(BaseModel):
    email: EmailStr

    

class UserLogin(UserBase):
    password: str = Field(max_length=20, min_length=4)
        
    
class UserCreate(UserBase):
    name: str = Field(max_length=20)



class UserRead(UserCreate):
    id: int


class ResponceCreate(BaseModel):
    user_id: int


class UserPassSchema(BaseModel):
    user_id: int
    hash_pass: str = Field(min_length=60)
    date_pass: datetime = datetime.now()


class EditPass(BaseModel):
    new_pass: str = Field(max_length=20, min_length=4)

class ConfirmCode(BaseModel):
    input_code: str = Field(max_length=6, min_length=6)
