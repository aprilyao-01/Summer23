from typing import Union

from pydantic import BaseModel

#Create Pydantic models/schemas

class TestRecord(BaseModel):
    user: str

class EmployeeBase(BaseModel):
    name: str


class EmployeeCreate(EmployeeBase):      # attributes that needed when create this record
    salary: Union[int, None] = None
    dept_id: Union[int, None] = None
    manager_id: Union[int, None] = None
    

class EmployeeNameList(EmployeeBase):       # orm mode to used under related table query
    pass

    class Config:
        orm_mode = True

class Employee(EmployeeBase):           # attributes that needed to become a ORM objects, should be same as model table
    id: int                             # if has 'top-secret' attribute like password, should NOT include
    dept_id: int
    manager_id: int

    class Config:       #internal Config class to turn pydantic model into ORM mode (aka arbitrary class instances)
        orm_mode = True      # to support models that map to ORM objects


class ManagerBase(BaseModel):          #seems useless?
    name: str

class ManagerCreate(ManagerBase):      # attributes that needed when create this record
    dept_id: int
   

class ManagerNameList(ManagerBase):       # orm mode to used under related table query
    pass

    class Config:
        orm_mode = True

class Manager(ManagerBase):           # attributes that needed to become a ORM objects, should be same as model table
    id: int
    dept_id: int
    monitor_employee: list[EmployeeNameList] = []

    class Config:       #internal Config class to turn pydantic model into ORM mode (aka arbitrary class instances)
        orm_mode = True      # to support models that map to ORM objects


class DepartmentBase(BaseModel):          #seems useless?
    name: str

class DepartmentCreate(DepartmentBase):      # attributes that needed when create this record
    pass
   

class Department(DepartmentBase):           # attributes that needed to become a ORM objects, should be same as model table
    id: int
    has_managers: list[ManagerNameList] = []
    has_employees: list[EmployeeNameList] = []

    class Config:       #internal Config class to turn pydantic model into ORM mode (aka arbitrary class instances)
        orm_mode = True      # to support models that map to ORM objects



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