
import time
from typing import List, Union

from fastapi import Depends, FastAPI, HTTPException

from . import crud, database, models, schemas
from .database import db_state_default
from pydantic import ValidationError

# create db tables
database.db.connect()
database.db.create_tables([models.Department, models.Manager, models.Employee])
database.db.close()

app = FastAPI()

sleep_time = 10


# Context variable sub-dependency
async def reset_db_state():
    database.db._state._state.set(db_state_default.copy())
    database.db._state.reset()


# Create a dependency that will connect the database right at the beginning of a request and disconnect it at the end
def get_db(db_state=Depends(reset_db_state)):
    try:
        database.db.connect()
        yield       # empty because not using the db object directly
    finally:
        if not database.db.is_closed():
            database.db.close()


# @app.get("/", response_model=list[schemas.Department], dependencies=[Depends(get_db)])
# def get_all():
#     try:
#         department = crud.select_departments(skip=None, limit=None)
        
#     except Exception as e:       # table been dropped
#         raise HTTPException(status_code=500, detail="Table been dropped")
#     return department
@app.get("/department/", response_model=list[schemas.Department], dependencies=[Depends(get_db)])
# @app.get("/department/", response_model=Union[list[schemas.Department], list[schemas.DepartmentCreate]], dependencies=[Depends(get_db)])
def read_all_departments(skip: int = 0, limit: int = 50):
    try:
        if not models.Department.table_exists():
            raise HTTPException(status_code=500, detail="Department table been dropped")
        department = crud.select_departments(skip=skip, limit=limit)
    except ValidationError:
        raise HTTPException(status_code=500, detail="response_model not match")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return department

@app.get("/department/{dept_id}", response_model=schemas.Department, dependencies=[Depends(get_db)])
def read_department_by_id(dept_id: int):
    try:
        if not models.Department.table_exists():
            raise HTTPException(status_code=500, detail="Department table been dropped")
        department = crud.select_department_by_id(dept_id)
    except models.Department.DoesNotExist:      #raise by select not found
        raise HTTPException(status_code=404, detail="Department not found")
    except ValidationError:
        raise HTTPException(status_code=500, detail="response_model not match")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return department


@app.get("/manager/", response_model=list[schemas.Manager], dependencies=[Depends(get_db)])
def read_all_managers(skip: int = 0, limit: int = 100):
    try:
        if not models.Manager.table_exists():
            raise HTTPException(status_code=500, detail="Manager table been dropped")
        managers = crud.select_managers(skip=skip, limit=limit)
    except ValidationError:
        raise HTTPException(status_code=500, detail="response_model not match")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return managers


@app.get("/manager/{dept_id}", response_model=list[schemas.Manager], dependencies=[Depends(get_db)])
def read_managers_by_department(dept_id: int):
    try:
        if not models.Manager.table_exists():
            raise HTTPException(status_code=500, detail="Manager table been dropped")
        managers = crud.select_manager_by_dept(dept_id=dept_id)
    except models.Manager.DoesNotExist:      #raise by select not found
        raise HTTPException(status_code=404, detail="Manager not found")
    except ValidationError:
        raise HTTPException(status_code=500, detail="response_model not match")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return managers


@app.get("/employee/", response_model=list[schemas.Employee], dependencies=[Depends(get_db)])
def read_all_employees(skip: int = 0, limit: int = 100):
    try:
        if not models.Employee.table_exists():
            raise HTTPException(status_code=500, detail="Employee table been dropped")
        employees = crud.select_employees(skip=skip, limit=limit)
    except ValidationError:
        raise HTTPException(status_code=500, detail="response_model not match")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return employees


@app.get("/employee/{emp_id}", response_model=schemas.Employee, dependencies=[Depends(get_db)])
def read_employee_by_id(emp_id: int):
    try:
        if not models.Employee.table_exists():
            raise HTTPException(status_code=500, detail="Employee table been dropped")
        employee = crud.select_employee_by_id(emp_id)
    except models.Employee.DoesNotExist:        #raise by select not found
            raise HTTPException(status_code=404, detail="Employee not found")
    except ValidationError:
        raise HTTPException(status_code=500, detail="response_model not match")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return employee


@app.post("/department/", response_model=Union[list[schemas.Department], list[schemas.DepartmentCreate]], dependencies=[Depends(get_db)])
def add_departments(departments: list[schemas.DepartmentCreate]):
    succ_add: list[schemas.Department] = []
    skip: list[schemas.Department] = []
    try:
        if not models.Department.table_exists():
            raise HTTPException(status_code=500, detail="Department table been dropped")
        for department in departments:
            db_department = crud.select_department_by_name(department.name)
            if db_department:       # check if department exist
                skip.append(db_department)
                print("******** Insert skipped. Department " + department.name + " already existed.")
                continue
                # raise HTTPException(status_code=400, detail="Department already registered")
            if crud.insert_department(department):  #return 1 for succ inset 1 record
                succ_add.append(crud.select_department_by_name(department.name))
    except ValidationError:
        raise HTTPException(status_code=500, detail="response_model not match")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        print("******** Success add " + str(len(succ_add)) + " record(s).  \n******** Skip " + str(len(skip)) + " record(s).  \n")
    return succ_add


@app.post("/manager/", response_model=list[schemas.Manager], dependencies=[Depends(get_db)])
def add_managers(managers: list[schemas.ManagerCreate]):
    succ_add: list[schemas.Manager] = []
    skip: list[schemas.Manager] = []
    try:
        if not models.Manager.table_exists():
            raise HTTPException(status_code=500, detail="Manager table been dropped")
        for manager in managers:
            db_manager = crud.select_manager_by_dept_and_name(manager.name, manager.dept_id)
            if db_manager:       # check if manager exist, even if two people have same name.
                skip.append(manager)
                print("******** Insert skipped. Manager " + manager.name + " already existed in this department." 
                        +" For people have same name, try nickname such as: Mike & Mike Junior. ")
                continue
                # raise HTTPException(status_code=400, detail="Manager already registered")
            elif crud.select_department_by_id(dept_id=manager.dept_id) is None:
                skip.append(manager)
                print("******** Insert skipped. Department " + str(manager.dept_id) + " does not exist!")
                continue
            else:
                succ_add.append(crud.insert_manager(manager))
    except ValidationError:
        raise HTTPException(status_code=500, detail="response_model not match")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        print("******** Success add " + str(len(succ_add)) + " record(s).  \n******** Skip " + str(len(skip)) + " record(s).  ")
    return succ_add

@app.post("/employee/", response_model=list[schemas.Employee], dependencies=[Depends(get_db)])
def add_employees(employees: list[schemas.EmployeeCreate]):
    succ_add: list[schemas.Employee] = []
    skip: list[schemas.Employee] = []
    try:
        for employee in employees:
            db_employee = crud.select_employee_by_all(check=employee)
            db_dept = crud.select_department_by_id(dept_id=employee.dept_id)
            db_manager = crud.select_manager_by_id(mng_id=employee.manager_id)
            
            if db_employee:       # check if employee exist, even if two people have same name.
                skip.append(employee)
                print("******** Insert skipped. Employee " + employee.name + " already existed with same manager and department." 
                        +" For people have same name, try nickname such as: Mike & Mike Junior. ")
                continue
                # raise HTTPException(status_code=400, detail="Manager already registered")
            elif db_dept is None:
                skip.append(employee)
                print("******** Insert skipped. Department " + str(employee.dept_id) + " does not exist!")
                continue
            elif db_manager is None:
                skip.append(employee)
                print("******** Insert skipped. Manager " + str(employee.manager_id) + " does not exist!")
                continue
            elif db_manager.dept_id != employee.dept_id:
                skip.append(employee)
                print("******** Insert skipped. Department " + str(employee.dept_id) + " does not have manager " + str(employee.manager_id))
                continue
            else:
                succ_add.append(crud.insert_employee(employee))
    except ValidationError:
        raise HTTPException(status_code=500, detail="response_model not match")
    except Exception as e:       # table been dropped
        raise HTTPException(status_code=500,  detail=str(e))
    finally:
        print("******** Success add " + str(len(succ_add)) + " record(s).  \n******** Skip " + str(len(skip)) + " record(s).  ")
    return succ_add



# update department by id
@app.put("/department/{dept_id}", response_model=schemas.Department, dependencies=[Depends(get_db)])
def update_department_by_id(dept_id: int, modi_dept: schemas.DepartmentCreate):
    try:
        db_dept = crud.select_department_by_id(dept_id=dept_id)
        if db_dept is None:            # rise exception
            raise HTTPException(status_code=404, detail="Department not found")
        elif crud.select_department_by_name(dept_name=modi_dept.name):
            raise HTTPException(status_code=400, detail="Department already existed")
        else:
            crud.update_department_by_id(dept_id=dept_id, modi_name=modi_dept.name)
    except ValidationError:
        raise HTTPException(status_code=500, detail="response_model not match")
    except Exception as e:       # table been dropped
        raise HTTPException(status_code=500, detail=str(e))
    return db_dept

#update manager by mng_id
@app.put("/manager/{mng_id}", response_model=schemas.Manager, dependencies=[Depends(get_db)])
def update_manager_by_id(mng_id: int, modi_mng: schemas.ManagerCreate):
    try:
        db_mng = crud.select_manager_by_id(mng_id= mng_id)
        if db_mng is None:            # rise exception
            raise HTTPException(status_code=404, detail="Manager not found")
        elif crud.select_manager_by_dept_and_name(name=modi_mng.name, dept_id=modi_mng.dept_id):
            raise HTTPException(status_code=400, 
                detail="Manager already existed in department. For people have same name, try nickname such as: Mike & Mike Junior.")
        elif crud.select_department_by_id(dept_id=modi_mng.dept_id) is None:
            raise HTTPException(status_code=500, detail="Update manager failed. Target department does not exist.")
        else:
            crud.update_manager_by_id(id=mng_id, modi_manager=modi_mng)
    except ValidationError:
        raise HTTPException(status_code=500, detail="response_model not match")
    except Exception as e:       # table been dropped
        raise HTTPException(status_code=500, detail=str(e))
    return db_mng


#update employee by emp_id
@app.put("/employee/{emp_id}", response_model=schemas.Employee, dependencies=[Depends(get_db)])
def update_employee_by_id(emp_id: int, modi_emp: schemas.EmployeeCreate):
    try:
        db_emp = crud.select_employee_by_id(emp_id=emp_id)
        db_manager = crud.select_manager_by_id(mng_id=modi_emp.manager_id)
        if db_emp is None:            # rise exception
            raise HTTPException(status_code=404, detail="Employee not found")
        elif crud.select_employee_by_all(check=modi_emp):
            raise HTTPException(status_code=400, 
                detail="Employee already existed with same manager and department. For people have same name, try nickname such as: Mike & Mike Junior.")
        elif crud.select_department_by_id(dept_id=modi_emp.dept_id) is None:
            raise HTTPException(status_code=500, detail="Update employee failed. Target department does not exist.")
        # elif crud.select_manager_by_id(mng_id=modi_emp.manager_id) is None:
        #     raise HTTPException(status_code=500, detail="Update employee failed. Target manager does not exist.")
        elif db_manager.dept_id != modi_emp.dept_id :
            raise HTTPException(status_code=500, detail="Update employee failed. Target manager does not exist in this department.")
        else:
            crud.update_employee_by_id(id=emp_id, modi_employee=modi_emp)
    except ValidationError:
        raise HTTPException(status_code=500, detail="response_model not match")
    except Exception as e:       # table been dropped
        raise HTTPException(status_code=500, detail=str(e))
    return db_emp

@app.delete("/department/", dependencies=[Depends(get_db)])
def drop_departments():
    try:
        response = crud.drop_department_table()
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    return response

@app.delete("/department/{dept_id}", response_model=list[schemas.Department], dependencies=[Depends(get_db)])
def delete_department_by_id(dept_id: int):
    try:
        department = crud.select_department_by_id(dept_id)
        if department is None:            # rise exception
            raise HTTPException(status_code=404, detail="Department does not exist")
        else:
            crud.delete_department_by_id(dept_id)
    except ValidationError:
        raise HTTPException(status_code=500, detail="response_model not match")
    except Exception as e:       # table been dropped
        raise HTTPException(status_code=500, detail=str(e))
    return crud.select_departments(None, None)


@app.delete("/manager/", dependencies=[Depends(get_db)])
def drop_managers():
    try:
        response = crud.drop_manager_table()
        # print(type(response))
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    return response

@app.delete("/manager/{mng_id}", response_model=list[schemas.Manager], dependencies=[Depends(get_db)])
def delete_manager_by_id(mng_id: int):
    try:
        manager = crud.select_manager_by_id(mng_id)
        if manager is None:            # rise exception
            raise HTTPException(status_code=404, detail="Manager does not exist")
        else:
            crud.delete_manager(manager)
    except ValidationError:
        raise HTTPException(status_code=500, detail="response_model not match")
    except Exception as e:       # table been dropped
        raise HTTPException(status_code=500, detail=str(e))
    return crud.select_managers(None, None)

@app.delete("/employee/", dependencies=[Depends(get_db)])
def drop_employee():
    try:
        response = crud.drop_employee_table()
        # print(type(response))
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
    return response

@app.delete("/employee/{emp_id}", response_model=list[schemas.Employee], dependencies=[Depends(get_db)])
def delete_employee_by_id(emp_id: int):
    try:
        employee = crud.select_employee_by_id(emp_id)
        if employee is None:            # rise exception
            raise HTTPException(status_code=404, detail="Employee does not exist")
        else:
            crud.delete_employee(employee)
    except ValidationError:
        raise HTTPException(status_code=500, detail="response_model not match")
    except Exception as e:       # table been dropped
        raise HTTPException(status_code=500,detail=str(e))
    return crud.select_employees(None, None)
