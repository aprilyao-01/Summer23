# In this file we will have reusable functions to interact with the data in the database.
# CRUD: Create, Read, Update, and Delete
# ...although in this example we are only creating and reading

from unittest import mock
from sqlalchemy.orm import Session
# allow to declare the type of the db parameters and have better type checks and completion in functions

from . import models, schemas


'''
# Read a single user by ID
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Read a single user by email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Read multiple users
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# Create a SQLAlchemy model instance with data
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"        # example is not secure, the password is not hashed. In a real life application you would need to hash the password and never save them in plaintext.
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)     # add instance object to database session
    db.commit()         # commit the changes to the database (so that they are saved)
    db.refresh(db_user) # refresh instance (so that it contains any new data from the database, like the generated ID)
    return db_user

# Read multiple items
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

# Create a SQLAlchemy model instance with your data.
def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
'''

# Create a department record
def insert_department(db: Session, department: schemas.DepartmentCreate):
    new_department = models.Department(**department.dict())
    db.add(new_department)        # add instance object to database session
    db.commit()                 # commit the changes to the database (so that they are saved)
    db.refresh(new_department)    # refresh instance (so that it contains any new data from the database, like the generated ID)
    return new_department

# Read multiple departments
def select_departments(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.Department).offset(skip).limit(limit).all()

# Read department by id
def select_department_by_id(db: Session, dept_id: int):
    return db.query(models.Department).get(dept_id)
    # return db.query(models.Department).filter(models.Department.id == dept_id).first()

# Read department by name
def select_department_by_name(db: Session, dept_name: str):
    return db.query(models.Department).filter(models.Department.name == dept_name).first()

# Update department by id
def update_department_by_id(db: Session, dept_id: int, modi_name:str):
    db_dept = db.query(models.Department).get(dept_id)
    db_dept.name = modi_name
    db.commit()
    return db_dept

# delete department record
def delete_department(db: Session, department: schemas.Department):
    db.delete(department)
    db.commit()
    return

# drop department table
def drop_department_table(db: Session):
    db.execute("DROP TABLE IF EXISTS department CASCADE;")
    db.commit()
    return {"Drop table department": "True"}



# Create a manager record
def insert_manager(db: Session, manager: schemas.ManagerCreate):
    new_manager = models.Manager(**manager.dict())
    db.add(new_manager)         # add instance object to database session
    db.commit()                 # commit the changes to the database (so that they are saved)
    db.refresh(new_manager)     # refresh instance (so that it contains any new data from the database, like the generated ID)
    return new_manager

# Read multiple managers
def select_managers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Manager).offset(skip).limit(limit).all()

# Read manager by id
def select_manager_by_id(db: Session, mng_id: int):
    return db.query(models.Manager).get(mng_id)

# Read manager by department and name
def select_manager_by_dept_and_name(db: Session, name: str, dept_id:int):
    return db.query(models.Manager).filter(models.Manager.name == name, models.Manager.dept_id == dept_id).first()

# Read managers by department
def select_manager_by_dept(db: Session, dept_id: int):
    return db.query(models.Manager).filter(models.Manager.dept_id == dept_id).all()


# Update manager by id
def update_manager_by_id(db: Session, id:int, modi_manager: schemas.ManagerCreate):
    db_mng = db.query(models.Manager).get(id)
    db_mng.name = modi_manager.name
    db_mng.dept_id = modi_manager.dept_id
    db.commit()
    return db_mng

# delete manager record
def delete_manager(db: Session, manager: schemas.Manager):
    db.delete(manager)
    db.commit()
    return

# drop manager table
def drop_manager_table(db: Session):
    db.execute("DROP TABLE IF EXISTS manager CASCADE;")
    db.commit()
    return {"Drop table manager": "True"}


# Create a employee record
def insert_employee(db: Session, employee: schemas.EmployeeCreate):
    new_employee = models.Employee(**employee.dict())
    db.add(new_employee)         # add instance object to database session
    db.commit()                  # commit the changes to the database (so that they are saved)
    db.refresh(new_employee)     # refresh instance (so that it contains any new data from the database, like the generated ID)
    return new_employee


# Read multiple employees
def select_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Employee).offset(skip).limit(limit).all()

# Read employee by id
def select_employee_by_id(db: Session, emp_id: int):
    return db.query(models.Employee).get(emp_id)

# Read employee by department
def select_employee_by_dept(db: Session, dept_id: int):
    return db.query(models.Employee).filter(models.Employee.dept_id == dept_id).all()

# Read employee check if exist
def select_employee_by_all(db: Session, check: schemas.EmployeeCreate):
    return db.query(models.Employee).filter(models.Employee.name == check.name,
                                    models.Employee.salary == check.salary,
                                    models.Employee.dept_id == check.dept_id,
                                    models.Employee.manager_id == check.manager_id).first()

# Update employee by id
def update_employee_by_id(db: Session, id:int, modi_employee: schemas.EmployeeCreate):
    db_emp = db.query(models.Employee).get(id)
    db_emp.name = modi_employee.name
    db_emp.salary = modi_employee.salary
    db_emp.manager_id = modi_employee.manager_id
    db_emp.dept_id = modi_employee.dept_id
    db.commit()
    return db_emp

# delete employee record
def delete_employee(db: Session, employee: schemas.Employee):
    db.delete(employee)
    db.commit()
    return

# drop employee table
def drop_employee_table(db: Session):
    db.execute("DROP TABLE IF EXISTS employee;")
    db.commit()
    return {"Drop table employee": "True"}