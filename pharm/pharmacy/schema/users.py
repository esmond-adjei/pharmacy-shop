from pydantic import BaseModel
from datetime import date


class UserBase(BaseModel):
    username: str
    address: str | None
    email: str | None
    date_of_birth: date | None


class UserCreate(UserBase):
    password: str


class UserSchema(UserBase):
    id: int

    class Config:
        orm_mode = True
