from typing import Union, Optional
from . import models, schemas

# Create a department record -> int, number of records been created
def insert_department(department: schemas.DepartmentCreate) -> int:
    new_department = models.Department.create(**department.dict())
    new_department.save()         # commit the changes to the database (so that they are saved)
    return new_department

#if error, no record will be insert. duplicate key value violates unique constraint "department_name"
# def insert_departments(departments: list):
#     new_departments = models.Department.insert_many(departments).execute()
#     print(new_departments)
#     return new_departments

# Read multiple departments -> [Model]|[]
def select_departments(skip: int = 0, limit: int = 50) -> Optional[list[schemas.Department]]:
    departments = list(models.Department.select().offset(skip).limit(limit))
    for department in departments:
        department = response_department(department)
    return departments

# Read department by id -> Model| raise DepartmentDoesNotExist if id does not exist
def select_department_get_by_id(dept_id: int) -> Union[schemas.Department,Exception]:
    department = models.Department.get_by_id(dept_id)
    department = response_department(department)
    return department

def select_department_by_id(dept_id: int) -> Optional[schemas.Department]:
    department = models.Department.filter(models.Department.id == dept_id).first()
    if department:
        department = response_department(department)
    return department

# Read department by name -> Model | None
def select_department_by_name(dept_name: str) -> Optional[schemas.Department]:
    department = models.Department.filter(models.Department.name == dept_name).first()
    if department:      # if department != None
        department = response_department(department)
    return department

# Update department by id -> Model| raise DepartmentDoesNotExist if id does not exist
def update_department_by_id(dept_id: int, modi_name:str) -> Union[schemas.Department,Exception]:
    db_dept = models.Department.get_by_id(dept_id)
    db_dept.name = modi_name
    db_dept.save()
    db_dept = response_department(db_dept)
    return db_dept

# delete department record by id -> int, number of records been deleted
def delete_department_by_id(dept_id: int) -> int:
    return models.Department.delete_by_id(dept_id)

# drop department table -> None
def drop_department_table() -> None:
    models.Department.drop_table(safe=True,cascade=True)
    return {"Drop table department": "True"}

# Create a manager record
def insert_manager(manager: schemas.ManagerCreate) -> int:
    new_manager = models.Manager.create(**manager.dict())
    new_manager.save()
    return new_manager

# Read multiple managers
def select_managers(skip: int = 0, limit: int = 100)-> list[schemas.Manager]:
    managers = list(models.Manager.select().offset(skip).limit(limit))
    for manager in managers:
        manager = response_manager(manager)
    return managers

# Read manager by id
def select_manager_get_by_id(mng_id: int)-> Union[schemas.Manager,Exception]:
    manager = models.Manager.get_by_id(mng_id)
    manager = response_manager(manager)
    return manager


def select_manager_by_id(mng_id: int)-> Optional[schemas.Manager]:
    manager = models.Manager.filter(models.Manager.id == mng_id).first()
    if manager:
        manager = response_manager(manager)
    return manager

# Read manager by department and name
def select_manager_by_dept_and_name(name: str, dept_id:int)-> Optional[schemas.Manager]:
    manager = models.Manager.filter(models.Manager.name == name, models.Manager.dept_id == dept_id).first()
    if manager:
        manager = response_manager(manager)
    return manager

# Read managers by department
def select_manager_by_dept(dept_id: int)-> list[schemas.Manager]:
    managers = list(models.Manager.select().filter(models.Manager.dept_id == dept_id))
    for manager in managers:
        manager = response_manager(manager)
    return managers

# Update manager by id
def update_manager_by_id(id:int, modi_manager: schemas.ManagerCreate)-> Union[schemas.Manager,Exception]:
    db_mng = models.Manager.get_by_id(id)
    db_mng.name = modi_manager.name
    db_mng.dept_id = modi_manager.dept_id
    db_mng.save()
    db_mng = response_manager(db_mng)
    return db_mng

# delete manager record
def delete_manager_by_id(id: int) -> int:
    return models.Manager.delete_by_id(id)

# drop manager table
def drop_manager_table()-> None:
    models.Manager.drop_table(safe=True,cascade=True)
    return {"Drop table manager": "True"}

# Create a employee record
def insert_employee(employee: schemas.EmployeeCreate)-> int:
    new_employee = models.Employee.create(**employee.dict())
    new_employee.save() 
    return new_employee

# Read multiple employees
def select_employees(skip: int = 0, limit: int = 100)-> Optional[list[models.Employee]]:
    return list(models.Employee.select().offset(skip).limit(limit))

# Read employee by id
def select_employee_by_id(emp_id: int)-> Union[schemas.Employee,Exception]:
    return models.Employee.get_by_id(emp_id)

# Read employees by department
def select_employee_by_dept(dept_id: int)-> list[models.Employee]:
    return list(models.Employee.select().filter(models.Employee.dept_id == dept_id))

# Read employee check if exist
def select_employee_by_all(check: schemas.EmployeeCreate) -> Optional[schemas.Employee]:
    return models.Employee.filter(models.Employee.name == check.name,
                                    models.Employee.salary == check.salary,
                                    models.Employee.dept_id == check.dept_id,
                                    models.Employee.manager_id == check.manager_id).first()

# Update employee by id
def update_employee_by_id(id:int, modi_employee: schemas.EmployeeCreate)-> Union[schemas.Employee,Exception]:
    db_emp = models.Employee.get_by_id(id)
    db_emp.name = modi_employee.name
    db_emp.salary = modi_employee.salary
    db_emp.manager_id = modi_employee.manager_id
    db_emp.dept_id = modi_employee.dept_id
    db_emp.save()
    return db_emp

# delete employee record
def delete_employee_by_id(id: int)-> int:
    return models.Employee.delete_by_id(id)

# drop employee table
def drop_employee_table()-> None:
    models.Employee.drop_table(safe=True,cascade=True)
    return {"Drop table employee": "True"}

# put query return into schemas format
def response_manager(manager: schemas.Manager) -> schemas.Manager:
    manager.with_employee = list(manager.with_employee)
    return manager

def response_department(department: schemas.Department) -> schemas.Department:
    department.has_managers = list(department.has_managers)
    department.has_employees = list(department.has_employees)
    return department

