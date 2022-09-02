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


class ManagerBase(BaseModel): 
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
    with_employee: list[EmployeeNameList] = []

    class Config:       #internal Config class to turn pydantic model into ORM mode (aka arbitrary class instances)
        orm_mode = True      # to support models that map to ORM objects


class DepartmentBase(BaseModel):         
    name: str

class DepartmentCreate(DepartmentBase):      # attributes that needed when create this record
    pass
   

class Department(DepartmentBase):           # attributes that needed to become a ORM objects, should be same as model table
    id: int
    has_managers: list[ManagerNameList] = []
    has_employees: list[EmployeeNameList] = []

    class Config:       #internal Config class to turn pydantic model into ORM mode (aka arbitrary class instances)
        orm_mode = True      # to support models that map to ORM objects