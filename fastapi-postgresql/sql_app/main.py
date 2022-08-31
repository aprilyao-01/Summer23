from fastapi import Depends, FastAPI, HTTPException, Body
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

#Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:            #make sure the db session is always closed after the request. Even if there was an exception while processing the request.
        db.close()

# fake db used for test
testDatabase = {
    1:{'User': 'U1'},
    2:{'User': 'U2'},
    3:{'User': 'U3'},
}


@app.get("/test")
def test_get():
    return testDatabase

#test get by id
@app.get("/test/{id}")
def test_get_by_id(id: int):
    return testDatabase[id]


# TODO: retest after add data, and join with department
@app.get("/")
def get_all(db: Session = Depends(get_db)):
    # query = """ SELECT e.id, e.name AS emp_name, e.salary, m.name, e.dept_id, d.name 
    #             FROM employee e
    #             LEFT JOIN manager m ON e.manager_id = m.id
    #             LEFT JOIN department d ON e.dept_id = d.id; """
    # records = db.execute(query)
    records = db.query(models.Employee.id, models.Employee.name,
                    models.Employee.salary, models.Manager.name,
                    models.Employee.dept_id #, models.Department.name
                    ).join((models.Manager, models.Employee.manager_id==models.Manager.id), isouter = True
                    # ).join(models.Department, models.Employee.dept_id == models.Department.id, isouter = True
                    ).all()
    
    return records  # return all the records as a JSON list

@app.get("/employee/", response_model=list[schemas.Employee])
def read_all_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    employees = crud.select_employees(db, skip=skip, limit=limit)
    return employees


@app.get("/employee/{emp_id}", response_model=schemas.Employee)
def read_employee_by_id(emp_id: int, db: Session = Depends(get_db)):
    employee = crud.select_employee_by_id(db, emp_id)
    if employee is None:            # rise exception
        raise HTTPException(status_code=404, detail="employee not found")
    return employee

# TODO: Read employees by salary range

@app.get("/manager/", response_model=list[schemas.Manager])
def read_all_managers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    managers = crud.select_managers(db, skip=skip, limit=limit)
    return managers

@app.get("/manager/{mng_id}", response_model=schemas.Manager)
def read_department_by_id(mng_id: int, db: Session = Depends(get_db)):
    manager = crud.select_manager_by_id(db, mng_id)
    if manager is None:            # rise exception
        raise HTTPException(status_code=404, detail="manager not found")
    return manager

@app.get("/department/", response_model=list[schemas.Department])
def read_all_department(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    departments = crud.select_departments(db, skip=skip, limit=limit)
    return departments

@app.get("/department/{dept_id}", response_model=schemas.Department)
def read_department_by_id(dept_id: int, db: Session = Depends(get_db)):
    department = crud.select_department_by_id(db, dept_id)
    if department is None:            # rise exception
        raise HTTPException(status_code=404, detail="department not found")
    return department

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


# option1: specify all the parameters
# con: don't have validation and can be problematic if data is complicated
# @app.post("/test/")
# def test_add_record_1(newUser: str):
#     index = len(testDatabase.keys()) + 1      # get the next index
#     testDatabase[index] = {"User": newUser}      # add new record to the test db
#     return testDatabase

# option2: pass in object
# use pydantic to design data schema and here is when to use 'schemas.py'
@app.post("/test/")
def test_add_record_2(newUser: schemas.TestRecord):
    index = len(testDatabase.keys()) + 1      # get the next index
    testDatabase[index] = {"User": newUser.user}      # get the schema's 'user' attribute
    return testDatabase

# option3: access request body as a dictionary
# scenarios: not know what data to send over right away, 
#            or want to access the entire request body sent over and extract each item as required
# @app.post("/test/")
# def test_add_record_3(body = Body()):
#     index = len(testDatabase.keys()) + 1      # get the next index
#     testDatabase[index] = {"User": body['user']}      # extract the value of the 'user'
#     return testDatabase


@app.post("/department/")
def add_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    return crud.insert_department(db, department)

@app.post("/department/{dept_id}/manager/", response_model=schemas.Manager)
def add_manager_in_department(dept_id: int, department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    return crud.insert_manager(db, department, dept_id)

#  TODO: insert employee under the relation department and manager
@app.post("/employee/")
def add_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.insert_employee(db, employee)

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):       # when using the dependency in a path operation function, declare it with the type Session that imported directly from SQLAlchemy
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


# updating data
@app.put("/test/{id}")
def test_update(id: int, modiUser:schemas.TestRecord):
    testDatabase[id]['User'] = modiUser.user
    return testDatabase


#deleting data
@app.delete("/test/{id}")
def test_delete(id: int):
    del testDatabase[id]
    return testDatabase