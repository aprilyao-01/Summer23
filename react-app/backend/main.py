from xml.dom import ValidationErr
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .peewee_app import crud, database, models, schemas
from .peewee_app.database import db_state_default
from pydantic import ValidationError


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

# create db tables
database.db.connect()
database.db.create_tables([models.Department, models.Manager, models.Employee])
database.db.close()

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

#  make cross-origin requests -- i.e., requests that originate from a different protocol, IP address, domain name, or port
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", dependencies=[Depends(get_db)])
def home_sweet_home():
    return {"detail": "Home Sweet Home"}

@app.get("/employee/", response_model=list[schemas.Employee], dependencies=[Depends(get_db)])
async def read_all_employees(skip: int = 0, limit: int = 50):
    try:
        if not models.Employee.table_exists():
            raise HTTPException(status_code=500, detail="Employee table been dropped")
        employees = crud.select_employees(skip=skip, limit=limit)
    except ValidationErr:
        raise HTTPException(status_code=500, detail="response_model not match")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return employees


@app.post("/employee/", response_model=list[schemas.Employee], dependencies=[Depends(get_db)])
async def add_employees(employee: schemas.EmployeeCreate):
    succ_add: list[schemas.Employee] = []
    skip: list[schemas.Employee] = []
    try:
        db_employee = crud.select_employee_by_all(check=employee);
        if db_employee:       # check if employee exist, even if two people have same name.
            skip.append(employee)
            print("******** Insert skipped. Employee " + employee.name + " already existed with same manager and department." 
                    +" For people have same name, try nickname such as: Mike & Mike Junior. ")
            # continue
            # raise HTTPException(status_code=400, detail="Manager already registered")
        else:
            succ_add.append(crud.insert_employee(employee))

        # for employee in employees:
        #     db_employee = crud.select_employee_by_all(check=employee)
        #     db_dept = crud.select_department_by_id(dept_id=employee.dept_id)
        #     db_manager = crud.select_manager_by_id(mng_id=employee.manager_id)
            
        #     if db_employee:       # check if employee exist, even if two people have same name.
        #         skip.append(employee)
        #         print("******** Insert skipped. Employee " + employee.name + " already existed with same manager and department." 
        #                 +" For people have same name, try nickname such as: Mike & Mike Junior. ")
        #         continue
        #         # raise HTTPException(status_code=400, detail="Manager already registered")
        #     elif db_dept is None:
        #         skip.append(employee)
        #         print("******** Insert skipped. Department " + str(employee.dept_id) + " does not exist!")
        #         continue
        #     elif db_manager is None:
        #         skip.append(employee)
        #         print("******** Insert skipped. Manager " + str(employee.manager_id) + " does not exist!")
        #         continue
        #     elif db_manager.dept_id != employee.dept_id:
        #         skip.append(employee)
        #         print("******** Insert skipped. Department " + str(employee.dept_id) + " does not have manager " + str(employee.manager_id))
        #         continue
        #     else:
        #         succ_add.append(crud.insert_employee(employee))
    except ValidationErr:
        raise HTTPException(status_code=500, detail="response_model not match")
    # except Exception as e:       # table been dropped
    #     raise HTTPException(status_code=500,  detail=str(e))
    finally:
        print("******** Success add " + str(len(succ_add)) + " record(s).  \n******** Skip " + str(len(skip)) + " record(s).  ")
    return succ_add

@app.put("/employee/{emp_id}", response_model=schemas.Employee, dependencies=[Depends(get_db)])
def update_employee_by_id(emp_id: int, modi_emp: schemas.EmployeeCreate):
    try:
        db_emp = crud.select_employee_by_id(emp_id=emp_id)
        # db_manager = crud.select_manager_by_id(mng_id=modi_emp.manager_id)
        # if modi_emp.salary < 0:
        #     raise HTTPException(status_code=500, detail="Update employee failed. Salary cannot less than 0.")
        if crud.select_employee_by_all(check=modi_emp):
            raise HTTPException(status_code=400, 
                detail="Employee already existed with same manager and department. For people have same name, try nickname such as: Mike & Mike Junior.")
        # elif crud.select_department_by_id(dept_id=modi_emp.dept_id) is None:
        #     raise HTTPException(status_code=500, detail="Update employee failed. Target department does not exist.")
        # elif db_manager is None:
        #     raise HTTPException(status_code=500, detail="Update employee failed. Target manager does not exist.")
        # elif db_manager.dept_id != modi_emp.dept_id :
        #     raise HTTPException(status_code=500, detail="Update employee failed. Target manager does not exist in this department.")
        else:
            db_emp = crud.update_employee(id=emp_id, modi_employee=modi_emp)
    except models.Employee.DoesNotExist:
        raise HTTPException(status_code=500, detail="Update employee failed. Target employee does not exist.")
    except ValidationError:
        raise HTTPException(status_code=500, detail="response_model not match")
    # except Exception as e:       # table been dropped
    #     raise HTTPException(status_code=500, detail=str(e))
    return db_emp



@app.delete("/employee/{emp_id}", response_model=list[schemas.Employee], dependencies=[Depends(get_db)])
def delete_employee_by_id(emp_id: int):
    try:
        if not models.Employee.table_exists():
            print(1)
            raise HTTPException(status_code=500, detail="Employee table been dropped")
        
        crud.select_employee_by_id(emp_id)        #raise does not exist if cannot found
        crud.delete_employee_by_id(emp_id)
    except models.Employee.DoesNotExist:
        raise HTTPException(status_code=404, detail="Employee does not exist")
    except ValidationError:
        raise HTTPException(status_code=500, detail="response_model not match")
    # except Exception as e:
    #     raise HTTPException(status_code=500,detail=str(e))
    return crud.select_employees(None, None)