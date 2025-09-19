from pydantic import BaseModel, EmailStr
from typing import Optional

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class ItemOut(ItemBase):
    id: int
    owner_id: int
    class Config:
        from_attributes = True  # instead of orm_mode
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    class Config:
        from_attributes = True  # instead of orm_mode

class Token(BaseModel):
    access_token: str
    token_type: str
