from itertools import count
from typing import Union
from fastapi import Depends, FastAPI, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.exc import ProgrammingError

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


@app.get("/test/")
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

@app.get("/department/", response_model=list[schemas.Department])
def read_all_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        department = crud.select_departments(db, skip=skip, limit=limit)
    except ProgrammingError as e:       # table been dropped
        raise HTTPException(status_code=500, detail="Department table been dropped")
    return department

@app.get("/department/{dept_id}", response_model=schemas.Department)
def read_department_by_id(dept_id: int, db: Session = Depends(get_db)):
    try:
        department = crud.select_department_by_id(db, dept_id)
        if department is None:            # rise exception
            raise HTTPException(status_code=404, detail="Department not found")
    except ProgrammingError as e:       # table been dropped
        raise HTTPException(status_code=500, detail="Department table been dropped")
    return department


@app.get("/manager/", response_model=list[schemas.Manager])
def read_all_managers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        managers = crud.select_managers(db, skip=skip, limit=limit)
    except ProgrammingError as e:       # table been dropped
        raise HTTPException(status_code=500, detail="Manager table been dropped")
    return managers


@app.get("/manager/{dept_id}", response_model=list[schemas.Manager])
def read_managers_by_department(dept_id: int, db: Session = Depends(get_db)):
    try:
        manager = crud.select_manager_by_dept(db, dept_id)
        if manager is None:            # rise exception
            raise HTTPException(status_code=404, detail="Manager not found")
    except ProgrammingError as e:       # table been dropped
        raise HTTPException(status_code=500, detail="Manager table been dropped")
    return manager


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

'''
# option1: specify all the parameters
# con: don't have validation and can be problematic if data is complicated
# @app.post("/test/")
# def test_add_record_1(newUser: str):
#     index = len(testDatabase.keys()) + 1      # get the next index
#     testDatabase[index] = {"User": newUser}      # add new record to the test db
#     return testDatabase

# option2: pass in object
# use pydantic to design data schema and here is when to use 'schemas.py'
# @app.post("/test/")
# def test_add_record_2(newUser: schemas.TestRecord):
#     index = len(testDatabase.keys()) + 1      # get the next index
#     testDatabase[index] = {"User": newUser.user}      # get the schema's 'user' attribute
#     return testDatabase

# option3: access request body as a dictionary
# scenarios: not know what data to send over right away, 
#            or want to access the entire request body sent over and extract each item as required
# @app.post("/test/")
# def test_add_record_3(body = Body()):
#     index = len(testDatabase.keys()) + 1      # get the next index
#     testDatabase[index] = {"User": body['user']}      # extract the value of the 'user'
#     return testDatabase
'''
# option4: use response_model
@app.post("/test/", response_model= list[schemas.TestRecord])
def test_add_records(users: list[schemas.TestRecord]):
    for user in users:
        index = len(testDatabase.keys()) + 1
        testDatabase[index] = {"User": user.user}
    return testDatabase


@app.post("/department/", response_model=list[schemas.Department])
def add_departments(departments: list[schemas.DepartmentCreate], db: Session = Depends(get_db)):
    succ_add: list[schemas.Department] = []
    skip: list[schemas.Department] = []
    try:
        for department in departments:
            db_department = crud.select_department_by_name(db, department.name)
            if db_department:       # check if department exists
                skip.append(db_department)
                continue
                # raise HTTPException(status_code=400, detail="Department already registered")
            else:
                succ_add.append(crud.insert_department(db, department))
    except ProgrammingError as e:       # table been dropped
        raise HTTPException(status_code=500, detail="Department table been dropped")
    finally:
        print("******** Success add " + str(len(succ_add)) + " record(s).  \n******** Skip " + str(len(skip)) + " record(s).  \n")
    return succ_add

# Discarded
""" @app.post("/department/{dept_id}/manager/", response_model=list[schemas.Manager])
def add_managers_in_department(dept_id: int, managers: list[schemas.ManagerCreate], db: Session = Depends(get_db)):
    succ_add: list[schemas.Manager] = []
    skip: list[schemas.Manager] = []
    try:
        for manager in managers:
            db_manager = crud.select_department_by_name(db, manager.name)
            if db_manager:       # check if manager exists, even if two people have same name.
                skip.append(db_manager)
                continue
                # raise HTTPException(status_code=400, detail="Manager already registered")
            else:
                succ_add.append(crud.insert_manager(db, manager, dept_id))
    except ProgrammingError as e:       # table been dropped
        raise HTTPException(status_code=500, detail="Manager table been dropped")
    finally:
        print("Success add " + str(len(succ_add)) + " record(s).\nSkip " + str(len(skip)) + " record(s).\n")
        if len(skip) > 0:
            print("For people have same name, try nickname such as: Mike & Mike Junior.")
    return succ_add """

@app.post("/manager/", response_model=list[schemas.Manager])
def add_managers(managers: list[schemas.ManagerCreate], db: Session = Depends(get_db)):
    succ_add: list[schemas.Manager] = []
    skip: list[schemas.Manager] = []
    try:
        for manager in managers:
            db_manager = crud.select_manager_by_dept_and_name(db, manager.name, manager.dept_id)
            if db_manager:       # check if manager exists, even if two people have same name.
                skip.append(manager)
                print("******** Insert skipped. Manager " + manager.name + " already exists in this department." 
                        +" For people have same name, try nickname such as: Mike & Mike Junior. ")
                continue
                # raise HTTPException(status_code=400, detail="Manager already registered")
            elif crud.select_department_by_id(db, dept_id=manager.dept_id) is None:
                skip.append(manager)
                print("******** Insert skipped. Department " + str(manager.dept_id) + " no exists!")
                continue
            else:
                succ_add.append(crud.insert_manager(db, manager))
    except ProgrammingError as e:       # table been dropped
        raise HTTPException(status_code=500, detail="Manager table been dropped")
    finally:
        print("******** Success add " + str(len(succ_add)) + " record(s).  \n******** Skip " + str(len(skip)) + " record(s).  ")
    return succ_add

#  TODO: insert employee under the relation department and manager
@app.post("/employee/", response_model=schemas.Employee)
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

# update department by id
@app.put("/department/{dept_id}", response_model=schemas.Department)
def update_department_by_id(dept_id: int, modi_dept: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    try:
        db_dept = crud.select_department_by_id(db, dept_id=dept_id)
        if db_dept is None:            # rise exception
            raise HTTPException(status_code=404, detail="Department not found")
        elif crud.select_department_by_name(db, dept_name=modi_dept.name):
            raise HTTPException(status_code=400, detail="Department already exists")
        else:
            crud.update_department_by_id(db, dept_id=dept_id, modi_name=modi_dept.name)
    except ProgrammingError as e:       # table been dropped
        raise HTTPException(status_code=500, detail="Department table been dropped")
    return db_dept

#update manager by mng_id
@app.put("/manager/{mng_id}", response_model=schemas.Manager)
def update_manager_by_id(mng_id: int, modi_mng: schemas.ManagerCreate, db: Session = Depends(get_db)):
    try:
        db_mng = crud.select_manager_by_id(db, mng_id= mng_id)
        if db_mng is None:            # rise exception
            raise HTTPException(status_code=404, detail="Manager not found")
        elif crud.select_manager_by_dept_and_name(db, name=modi_mng.name, dept_id=modi_mng.dept_id):
            raise HTTPException(status_code=400, 
                detail="Manager already exists in department.For people have same name, try nickname such as: Mike & Mike Junior.")
        elif crud.select_department_by_id(db, dept_id=modi_mng.dept_id) is None:
            raise HTTPException(status_code=500, detail="Department not exits.")
        else:
            crud.update_manager_by_id(db, id=mng_id, modi_manager=modi_mng)
    except ProgrammingError as e:       # table been dropped
        raise HTTPException(status_code=500, detail="Manager table been dropped.")
    return db_mng

#deleting data
@app.delete("/test/{id}")
def test_delete(id: int):
    del testDatabase[id]
    return testDatabase


@app.delete("/department/")
def drop_departments(db: Session = Depends(get_db)):
    try:
        response = crud.drop_department_table(db)
        # print(type(response))
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    return response

@app.delete("/department/{dept_id}", response_model=list[schemas.Department])
def delete_department_by_id(dept_id: int, db: Session = Depends(get_db)):
    try:
        department = crud.select_department_by_id(db, dept_id)
        if department is None:            # rise exception
            raise HTTPException(status_code=404, detail="Department not exists")
        else:
            crud.delete_department(db, department)
    except ProgrammingError as e:       # table been dropped
        raise HTTPException(status_code=500, detail="Department table been dropped")
    return crud.select_departments(db, None, None)


@app.delete("/manager/")
def drop_managers(db: Session = Depends(get_db)):
    try:
        response = crud.drop_manager_table(db)
        # print(type(response))
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    return response

@app.delete("/manager/{mng_id}", response_model=list[schemas.Manager])
def delete_manager_by_id(mng_id: int, db: Session = Depends(get_db)):
    try:
        manager = crud.select_manager_by_id(db, mng_id)
        if manager is None:            # rise exception
            raise HTTPException(status_code=404, detail="Manager not exists")
        else:
            crud.delete_manager(db, manager)
    except ProgrammingError as e:       # table been dropped
        raise HTTPException(status_code=500, detail="Manager table been dropped")
    return crud.select_managers(db, None, None)