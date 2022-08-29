from typing import Union

from pydantic import BaseModel

#Create Pydantic models/schemas
class ItemBase(BaseModel):      # pydantic schemas
    title: str
    description : Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):       # pydantic schemas for reading/returning
    id: int
    owner_id: int

    # an internal Config class -> provide configurations to Pydantic, be able to return a database model and it will read the data from it
    class Config:
        orm_mode = True


class UserBase(BaseModel):          # pydantic schemas
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):           # pydantic schemas for reading/returning
    id: int
    is_active: bool
    items: list[Item] = []

    # an internal Config class -> provide configurations to Pydantic, be able to return a database model and it will read the data from it
    class Config:
        orm_mode = True