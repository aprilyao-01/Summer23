from typing import Any, Union

import peewee
from pydantic import BaseModel
from pydantic.utils import GetterDict

# to convert the peewee object by dict and inform pydantic schemas
class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):      # checking if the attribute that is being accessed is an instance of peewee.ModelSelect
            return list(res)        # if is, return a list with it
        return res

#Create Pydantic models/schemas
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
        getter_dic = PeeweeGetterDict   # inform pydantic schemas

class Employee(EmployeeBase):
    id: int             #creating the models with an id, which didn't explicitly specified in models, but Peewee adds one automatically.
    dept_id: Union[int, None] = None      # also adding the magic dept_id and manager_id attributes to Employee, which are Peewee adds automatically.
    manager_id: Union[int, None] = None

    class Config:
        orm_mode = True
        getter_dic = PeeweeGetterDict   # inform pydantic schemas


class ManagerBase(BaseModel): 
    name: str

class ManagerCreate(ManagerBase):      # attributes that needed when create this record
    dept_id: int
   

class ManagerNameList(ManagerBase):       # orm mode to used under related table query
    pass

    class Config:
        orm_mode = True
        getter_dic = PeeweeGetterDict   # inform pydantic schemas


class Manager(ManagerBase):           # attributes that needed to become a ORM objects, should be same as model table
    id: int
    dept_id: int
    with_employee: list[EmployeeNameList] = []

    class Config:
        orm_mode = True
        getter_dic = PeeweeGetterDict   # inform pydantic schemas



class DepartmentBase(BaseModel):
    name: str

class DepartmentCreate(DepartmentBase):      # attributes that needed when create this record
    pass
   

class Department(DepartmentBase):           # attributes that needed to become a ORM objects, should be same as model table
    id: int
    has_managers: list[ManagerNameList] = []
    has_employees: list[EmployeeNameList] = []

    class Config:
        orm_mode = True
        getter_dic = PeeweeGetterDict   # inform pydantic schemas