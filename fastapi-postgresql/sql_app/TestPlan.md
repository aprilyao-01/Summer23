# Test Plan
This file records the test plan for [`main.py`](/fastapi-postgresql/sql_app/main.py). Ordered by table, operation.
* [Table: department](#table-department)
    * POST
        * [All](#operation-apppostdepartment-responsemodellistschemasdepartment)
    * GET
        * [All](#operation-appgetdepartment-responsemodellistschemasdepartment)
        * [By Id](#operation-appgetdepartmentdeptid-responsemodelschemasdepartment)
    * PUT
        * [By Id](#operation-appputdepartmentdeptid-responsemodelschemasdepartmentcreate)
    * DELETE
        * [By Id](#operation-appdeletedepartmentdeptid-responsemodellistschemasdepartment)
        * [Drop Table](#operation-appdeletedepartment)      
* [Table: manager](#table-manager)
    * POST
        * [~~By department~~](#operation-apppostdepartmentdeptidmanager-responsemodelschemasmanager)  **Discarded**
        * [All](#operation-apppostmanager-responsemodellistschemasmanager)
    * GET
        * [All](#operation-appgetmanager-responsemodellistschemasmanager)
        * [By Department](#operation-appgetmanagerdeptid-responsemodellistschemasmanager)
    * PUT
        * [By Id](#operation-appputmanagermngid-responsemodelschemasmanager)
    * DELETE
        * [By Id](#operation-appdeletemanagermngid-responsemodellistschemasmanager)
        * [Drop table](#operation-appdeletemanager)      
* [Table: employee](#table-employee)
    * POST
        * [All](#operation-apppostemployee-responsemodellistschemasemployee)
    * GET
        * [All](#operation-appgetemployee-responsemodellistschemasemployee)
        * [By Id](#operation-appgetemployeeempid-responsemodelschemasemployee)
    * PUT
        * [By Id](#operation-appputemployeeempid-responsemodelschemasemployee)
    * DELETE
        * [By Id](#operation-appdeleteemployeeempid-responsemodellistschemasemployee)
        * [Drop table](#operation-appdeleteemployee)


## Table: department
### Operation: @app.post("/department/", response_model=list[schemas.Department])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:----:|------|----------------|------------|------|-------|
|1|{"name": "IT"}|{"id": 1, "name": "IT"} |{"id": 1, "name": "IT"}|Pass||
|2|[{"name": "HR"}, {"name": "Finance"}, {"name": "Admin"}]|<mark>[{"name": "HR"}, {"name": "Finance"}, {"name": "Admin"}]</mark> |Internal Server Error, value is not a valid dict (type=type_error.dict)|Fail|change `succ_add` type and `response_model`|
|3|[{"name": "IT"}, {"name": "HR"}, {"name": "Finance"}, {"name": "Admin"}]|[{ "name": "IT","id": <mark>1</mark>,"has_managers": [],"has_employees": []},{"name": "HR","id": <mark>2</mark>,"has_managers": [],"has_employees": []},{"name": "Finance","id":  <mark>3</mark>,"has_managers": [],"has_employees": []},{"name": "Admin","id": <mark>4</mark>,"has_managers": [],"has_employees": []}] |[{ "name": "IT","id": ~~6~~,"has_managers": [],"has_employees": []},{"name": "HR","id": ~~7~~,"has_managers": [],"has_employees": []},{"name": "Finance","id": ~~8~~,"has_managers": [],"has_employees": []},{"name": "Admin","id": ~~9~~,"has_managers": [],"has_employees": []}]|Fail|change the `delete_department` to drop table|
|4|[{"name": "IT"}, {"name": "HR"}, {"name": "Finance"}, {"name": "Admin"}]|[{ "name": "IT","id": 1,"has_managers": [],"has_employees": []},{"name": "HR","id": 2,"has_managers": [],"has_employees": []},{"name": "Finance","id": 3,"has_managers": [],"has_employees": []},{"name": "Admin","id": 4,"has_managers": [],"has_employees": []}] |[{ "name": "IT","id": 1,"has_managers": [],"has_employees": []},{"name": "HR","id": 2,"has_managers": [],"has_employees": []},{"name": "Finance","id": 3,"has_managers": [],"has_employees": []},{"name": "Admin","id": 4,"has_managers": [],"has_employees": []}]|Pass|add terminal print and table dropped exception|
|5|[{"name": "IT"}, {"name": "HR"}, {"name": "Finance"}, {"name": "Admin"}]|[ ], Success add 0 record(s). Skip 4 record(s).|[ ], Success add 0 record(s). Skip 4 record(s).|Pass||


### Operation: @app.get("/department/", response_model=list[schemas.Department])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:----:|------|----------------|------------|------|-------|
|1|/|[ ]|[ ]|Pass|
|2|/|[{ "name": "IT","id": 1,"has_managers": [],"has_employees": []},{"name": "HR","id": 2,"has_managers": [],"has_employees": []},{"name": "Finance","id": 3,"has_managers": [],"has_employees": []},{"name": "Admin","id": 4,"has_managers": [],"has_employees": []}]|[{ "name": "IT","id": 1,"has_managers": [],"has_employees": []},{"name": "HR","id": 2,"has_managers": [],"has_employees": []},{"name": "Finance","id": 3,"has_managers": [],"has_employees": []},{"name": "Admin","id": 4,"has_managers": [],"has_employees": []}]|Pass| add `try except`|
|3|/|{"detail": "Departments been deleted"}|{"detail": "Departments been deleted"}|Pass||
|4|/|[{"name": "IT","id": 1,"has_managers": [{"name": "Nick","id": 2,"dept_id": 1,"with_employee": []},{"name": "Cory","id": 3,"dept_id": 1,"with_employee": []}],"has_employees": []},{"name": "HR","id": 2,"has_managers": [],"has_employees": []},{"name": "Finance","id": 3,"has_managers": [{"name": "Prem","id": 1,"dept_id": 3,"with_employee": []}],"has_employees": []},{"name": "Admin","id": 4,"has_managers": [],"has_employees": []}]|[{"name": "IT","id": 1,"has_managers": [{"name": "Nick","id": 2,"dept_id": 1,"with_employee": []},{"name": "Cory","id": 3,"dept_id": 1,"with_employee": []}],"has_employees": []},{"name": "HR","id": 2,"has_managers": [],"has_employees": []},{"name": "Finance","id": 3,"has_managers": [{"name": "Prem","id": 1,"dept_id": 3,"with_employee": []}],"has_employees": []},{"name": "Admin","id": 4,"has_managers": [],"has_employees": []}]|Pass|create orm mode class `schemas.EmployeeNameList` and `schemas.ManagerNameList` and change the `schemas.Department has_managers` and `schemas.Department has_employees`|
|5|/|[{"name": "IT","id": 1,"has_managers": [{"name": "Nick"},{"name": "Cory"}],"has_employees": []},{"name": "HR","id": 2,"has_managers": [],"has_employees": []},{"name": "Finance","id": 3,"has_managers": [{"name": "Prem"}],"has_employees": []},{"name": "Admin","id": 4,"has_managers": [],"has_employees": []}]|[{"name": "IT","id": 1,"has_managers": [{"name": "Nick"},{"name": "Cory"}],"has_employees": []},{"name": "HR","id": 2,"has_managers": [],"has_employees": []},{"name": "Finance","id": 3,"has_managers": [{"name": "Prem"}],"has_employees": []},{"name": "Admin","id": 4,"has_managers": [],"has_employees": []}]|Pass||


### Operation: @app.get("/department/{dept_id}", response_model=schemas.Department)
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:----:|------|----------------|------------|------|-------|
|1|3|{ "detail": "department not found"}|{ "detail": "department not found"}|Pass||
|2|1|[{ "name": "IT","id": 1,"has_managers": [],"has_employees": []}]|[{ "name": "IT","id": 1,"has_managers": [],"has_employees": []}]|Pass||
|3|1|{"detail": "Departments been deleted"}|{"detail": "Departments been deleted"}|Pass||
|4|1|{"name": "IT","id": 1,"has_managers": [{"name": "Nick"},{"name": "Cory"}],"has_employees": [{"name": "James"},{"name": "Jack"},{"name": "May"}]}|{"name": "IT","id": 1,"has_managers": [{"name": "Nick"},{"name": "Cory"}],"has_employees": [{"name": "James"},{"name": "Jack"},{"name": "May"}]}|Pass||

### Operation: @app.delete("/department/{dept_id}", response_model=list[schemas.Department])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:----:|------|----------------|------------|------|-------|
|1|2|[{ "name": "IT","id": 1,"has_managers": [],"has_employees": []}<mark>,</mark>{"name": "Finance","id": 3,"has_managers": [],"has_employees": []},{"name": "Admin","id": 4,"has_managers": [],"has_employees": []}]|[{ "name": "IT","id": 1,"has_managers": [],"has_employees": []},~~{"name": "HR","id": 2,"has_managers": [],"has_employees": []},~~{"name": "Finance","id": 3,"has_managers": [],"has_employees": []},{"name": "Admin","id": 4,"has_managers": [],"has_employees": []}]|Fail|not delete in db, add new crud functions `delete_department_by_id`|
|2|2|<mark>[{ "name": "IT","id": 1,"has_managers": [],"has_employees": []},{"name": "Finance","id": 3,"has_managers": [],"has_employees": []},{"name": "Admin","id": 4,"has_managers": [],"has_employees": []}]</mark>|Internal Server Error, AttributeError: 'Department' object has no attribute 'delete' |Fail|change `delete_department_by_id` to `delete_department` and add commit|
|3|2|[{ "name": "IT","id": 1,"has_managers": [],"has_employees": []},{"name": "Finance","id": 3,"has_managers": [],"has_employees": []},{"name": "Admin","id": 4,"has_managers": [],"has_employees": []}]|[{ "name": "IT","id": 1,"has_managers": [],"has_employees": []},{"name": "Finance","id": 3,"has_managers": [],"has_employees": []},{"name": "Admin","id": 4,"has_managers": [],"has_employees": []}] |Pass||

### Operation: @app.delete("/department/")
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:----:|------|----------------|------------|------|-------|
|1|/|[{"name": "IT", "id": 1, "has_managers": [],"has_employees": [] }]|[{"name": "IT", "id": 1, "has_managers": [],"has_employees": [] }]| Pass||
|2| /|<mark>{"Delete": "true"}</mark>|AttributeError: 'Session' object has no attribute '_run_ddl_visitor'| Fail| change the `delete_department` to db.execute raw SQL|
|3| /|<mark>{"Delete": "true"}</mark>|pydantic.error_wrappers.ValidationError: 1 validation error for Department response value is not a valid list (type=type_error.list)| Fail| delete `response_model`|
|4| /|{"Drop table department": "True"}|{"Drop table department": "True"}| Pass||

### Operation: @app.put("/department/{dept_id}", response_model=schemas.DepartmentCreate)
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:----:|------|----------------|------------|------|-------|
|1|[6, {"name": "Test"}]|{"detail": "Department not found"}|{"detail": "Department not found"}|Pass||
|2|[2, {"name": "IT"}]|{"detail": "Department already exists"}|{"detail": "Department already exists"}|Pass||
|3|[2, {"name": "Test"}]|<mark>"name": "Test","id": 2,"has_managers": [],"has_employees": []}</mark>|~~{"detail": "Department already exists"}~~, but db data updated|Fail|change `select_department_by_name` function|
|4|[2, {"name": "Test"}]|"name": "Test","id": 2,"has_managers": [],"has_employees": []}|pydantic.error_wrappers.ValidationError: 2 validation errors for Department response|Fail|change `return` to conform function `response_model`|
|5|[2, {"name": "HR"}]|{"name": "HR","id": 2,"has_managers": [],"has_employees": []}|{"name": "HR","id": 2,"has_managers": [],"has_employees": []}|Pass||

## Table: manager
### Operation: @app.post("/department/{dept_id}/manager/", response_model=schemas.Manager)
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|----|------|----------------|------------|------|-------|
|1|[3, [{"name": "Prem"}]]|[{ "name": "Prem","id": 1,"dept_id": 3,"with_employee": []}], Success add 1 record(s). Skip 0 record(s).For people have same name, try nickname such as: Mike & Mike Junior.|[{ "name": "Prem","id": 1,"dept_id": 3,"with_employee": []}], Success add 1 record(s). Skip 0 record(s).For people have same name, try nickname such as: Mike & Mike Junior.|Pass|change `For people have same name...` to print only when record skipped|
|2|[1, [{"name": "Nick"}, {"name": "Cory"}]]|[{ "name": "Nick","id": 2,"dept_id": 1,"with_employee": []}, { "name": "Cory","id": 3,"dept_id": 1,"with_employee": []}], Success add 2 record(s). Skip 0 record(s).|[{ "name": "Nick","id": 2,"dept_id": 1,"with_employee": []}, { "name": "Cory","id": 3,"dept_id": 1,"with_employee": []}], Success add 2 record(s). Skip 0 record(s).|Pass||
|3|[1, [{"name": "Nick"}, {"name": "Cory"}]]|[{ "name": "Nick","id": 2,"dept_id": 1,"with_employee": []}, { "name": "Cory","id": 3,"dept_id": 1,"with_employee": []}], Success add 2 record(s). Skip 0 record(s).|[{ "name": "Nick","id": 2,"dept_id": 1,"with_employee": []}, { "name": "Cory","id": 3,"dept_id": 1,"with_employee": []}], Success add 2 record(s). Skip 0 record(s).|Pass| **Discard this operation.** See [@app.post("/manager/", response_model=list[schemas.Manager])](#operation-apppostmanager-responsemodellistschemasmanager) instead|

### Operation: @app.post("/manager/", response_model=list[schemas.Manager])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|----|------|----------------|------------|------|-------|
|1|[{"name": "Shripadh","dept_id": 4}]|[{"name": "Shripadh","id": 4,"dept_id": 4,"monitor_employee": []}], Success add 1 record(s). Skip 0 record(s).|[{"name": "Shripadh","id": 4,"dept_id": 4,"monitor_employee": []}], Success add 1 record(s). Skip 0 record(s).|Pass||
|2| [{"name": "Prem","dept_id": 3},{"name": "Shripadh","dept_id": 4},{"name": "Nick","dept_id": 1},{"name": "Cory","dept_id": 1}]|[ ], Success add 0 record(s). Skip 4 record(s). For people have same name, try nickname such as: Mike & Mike Junior.|[ ], Success add 0 record(s). Skip 4 record(s). For people have same name, try nickname such as: Mike & Mike Junior.|Pass||
|3| [{"name": "Prem","dept_id": 3},{"name": "Shripadh","dept_id": 4},{"name": "Nick","dept_id": 1},{"name": "Cory","dept_id": 1}]|[{"name": "Prem","id": 5,"dept_id": 3,"monitor_employee": []}], Success add 1 record(s). Skip 3 record(s). For people have same name, try nickname such as: Mike & Mike Junior.|[{"name": "Prem","id": 5,"dept_id": 3,"monitor_employee": []}], Success add 1 record(s). Skip 3 record(s). For people have same name, try nickname such as: Mike & Mike Junior.|Pass||
|4| [{"name": "dept noe exist","dept_id": 78}]|<mark>[ ], Success add 0 record(s). Skip 1 record(s).</mark>|sqlalchemy.exc.IntegrityError: (psycopg2.errors.ForeignKeyViolation) insert or update on table "manager" violates foreign key constraint "manager_dept_id_fkey" DETAIL:  Key (dept_id)=(78) is not present in table "department".|Fail|add `check dept exists` first|
|5| [{"name": "dept noe exist","dept_id": 78}]|[ ], Insert skipped. Department 78 no exists! Success add 0 record(s). Skip 1 record(s).|[ ], Insert skipped. Department 78 no exists! Success add 0 record(s). Skip 1 record(s).|Pass||



### Operation: @app.get("/manager/", response_model=list[schemas.Manager])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|----|------|----------------|------------|------|-------|
|1|/|[{ "name": "Prem","id": 1,"dept_id": 3,"with_employee": []}]|[{ "name": "Prem","id": 1,"dept_id": 3,"with_employee": []}]|Pass||
|2|/|[{"name": "Prem","id": 1,"dept_id": 3,"monitor_employee": []},{"name": "Nick","id": 2,"dept_id": 1,"monitor_employee": []},{"name": "Cory","id": 3,"dept_id": 1,"monitor_employee": []},{"name": "Shripadh","id": 4,"dept_id": 4,"monitor_employee": []}]|[{"name": "Prem","id": 1,"dept_id": 3,"monitor_employee": []},{"name": "Nick","id": 2,"dept_id": 1,"monitor_employee": []},{"name": "Cory","id": 3,"dept_id": 1,"monitor_employee": []},{"name": "Shripadh","id": 4,"dept_id": 4,"monitor_employee": []}]|Pass||
|3|/|[{"name": "Prem","id": 1,"dept_id": 3,"with_employee": [{"name": "Eva"},{"name": "Robin"}]},{"name": "Nick","id": 3,"dept_id": 1,"with_employee": [{"name": "Jack"},{"name": "May"}]},{"name": "Cory","id": 4,"dept_id": 1,"with_employee": [{"name": "James"}]},{"name": "Jack","id": 2,"dept_id": 2,"with_employee": [{"name": "Bob"},{"name": "Amy"}]}]|[{"name": "Prem","id": 1,"dept_id": 3,"with_employee": [{"name": "Eva"},{"name": "Robin"}]},{"name": "Nick","id": 3,"dept_id": 1,"with_employee": [{"name": "Jack"},{"name": "May"}]},{"name": "Cory","id": 4,"dept_id": 1,"with_employee": [{"name": "James"}]},{"name": "Jack","id": 2,"dept_id": 2,"with_employee": [{"name": "Bob"},{"name": "Amy"}]}]|Pass||

### Operation: @app.get("/manager/{dept_id}", response_model=list[schemas.Manager])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|----|------|----------------|------------|------|-------|
|1|1|{"name": "Prem","id": 1,"dept_id": 3,"monitor_employee": []}|{"name": "Prem","id": 1,"dept_id": 3,"monitor_employee": []}|Pass|change to query all managers under dept_id, change `response_model` to list|
|2|1|[{"name": "Nick","id": 2,"dept_id": 1,"monitor_employee": []},{"name": "Cory","id": 3,"dept_id": 1,"monitor_employee": []}]|[{"name": "Nick","id": 2,"dept_id": 1,"monitor_employee": []},{"name": "Cory","id": 3,"dept_id": 1,"monitor_employee": []}]|Pass||


### Operation: @app.put("/manager/{mng_id}", response_model=schemas.Manager)
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|----|------|----------------|------------|------|-------|
|1|[2, {"name": "Jack","dept_id": 2}]|{"name": "Jack","id": 2,"dept_id": 2,"monitor_employee": []}|{"name": "Jack","id": 2,"dept_id": 2,"monitor_employee": []}|Pass|
|2|[2, {"name": "Jack","dept_id": 34}]|{"detail": "Department not exits."}|{"detail": "Department not exits."}|Pass|
|3|[7, {"name": "Jack","dept_id": 2}]|{ "detail": "Manager not found"}|{ "detail": "Manager not found"}|Pass|
|4|[4, {"name": "Nick","dept_id": 1}]|{"detail": "Manager already exists in department.For people have same name, try nickname such as: Mike & Mike Junior."}|{"detail": "Manager already exists in department.For people have same name, try nickname such as: Mike & Mike Junior."}|Pass|


### Operation: @app.delete("/manager/")
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|----|------|----------------|------------|------|-------|
|1|/|{"Drop table manager": "True"}|{"Drop table manager": "True"}|Pass||

### Operation: @app.delete("/manager/{mng_id}", response_model=list[schemas.Manager])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|----|------|----------------|------------|------|-------|
|1|1|[{"name": "Nick","id": 2,"dept_id": 1,"monitor_employee": []},{"name": "Cory","id": 3,"dept_id": 1,"monitor_employee": []},{"name": "Shripadh","id": 4,"dept_id": 4,"monitor_employee": []}]|[{"name": "Nick","id": 2,"dept_id": 1,"monitor_employee": []},{"name": "Cory","id": 3,"dept_id": 1,"monitor_employee": []},{"name": "Shripadh","id": 4,"dept_id": 4,"monitor_employee": []}]|Pass||


## Table: employee
### Operation: @app.post("/employee/", response_model=list[schemas.Employee])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|----|------|----------------|------------|------|-------|
|1|[{"name": "James","salary": 8000,"dept_id": 1,"manager_id": 1}]|[{"name": "James","salary": 8000,"dept_id": 1,"manager_id": 1}], Success add 1 record(s). Skip 0 record(s).|[{"name": "James","id": 1,"dept_id": 1,"manager_id": 1}], Success add 1 record(s). Skip 0 record(s).|Pass|add check if `manager is in the department`|
|2|[{"name": "James","salary": 8000,"dept_id": 1,"manager_id": 1}]|[ ],Insert skipped. Department 1 does not have manager 1. Success add 0 record(s). Skip 1 record(s).|[ ],Insert skipped. Department 1 does not have manager 1. Success add 0 record(s). Skip 1 record(s)|Pass||
|3|[{"name": "James","salary": 8000,"dept_id": 1,"manager_id": 4},{"name": "Bob","salary": 9500,"dept_id": 2,"manager_id": 2},{"name": "Eva","salary": 7000,"dept_id": 3,"manager_id": 1},{"name": "Jack","salary": 8000,"dept_id": 1,"manager_id": 3},{"name": "Robin","salary": 20000,"dept_id": 3,"manager_id": 1},{"name": "Amy","salary": 15000,"dept_id": 2,"manager_id": 2},{"name": "May","salary": 5000,"dept_id": 1,"manager_id": 3}]|[{"name": "James","id": 2,"dept_id": 1,"manager_id": 4},{"name": "Bob","id": 3,"dept_id": 2,"manager_id": 2},{"name": "Eva","id": 4,"dept_id": 3,"manager_id": 1},{"name": "Jack","id": 5,"dept_id": 1,"manager_id": 3},{"name": "Robin","id": 6,"dept_id": 3,"manager_id": 1},{"name": "Amy","id": 7,"dept_id": 2,"manager_id": 2},{"name": "May","id": 8,"dept_id": 1,"manager_id": 3}], Success add 7 record(s). Skip 0 record(s).|[{"name": "James","id": 2,"dept_id": 1,"manager_id": 4},{"name": "Bob","id": 3,"dept_id": 2,"manager_id": 2},{"name": "Eva","id": 4,"dept_id": 3,"manager_id": 1},{"name": "Jack","id": 5,"dept_id": 1,"manager_id": 3},{"name": "Robin","id": 6,"dept_id": 3,"manager_id": 1},{"name": "Amy","id": 7,"dept_id": 2,"manager_id": 2},{"name": "May","id": 8,"dept_id": 1,"manager_id": 3}], Success add 7 record(s). Skip 0 record(s).|Pass||
|4|[{"name": "dept not exist","salary": 8000,"dept_id": 10,"manager_id": 1}]|[ ],Insert skipped. Department 10 does not exist! Success add 0 record(s). Skip 1 record(s).|[ ],Insert skipped. Department 10 does not exist! Success add 0 record(s). Skip 1 record(s).|Pass||
|5|[{"name": "mng not exist","salary": 8000,"dept_id": 2,"manager_id": 7}]|[ ],Insert skipped. Manager 7 does not exist! Success add 0 record(s). Skip 1 record(s).|[ ],Insert skipped. Manager 7 does not exist! Success add 0 record(s). Skip 1 record(s).|Pass||


### Operation: @app.get("/employee/", response_model=list[schemas.Employee])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|----|------|----------------|------------|------|-------|
|1|/|[{"name": "James","id": 2,"dept_id": 1,"manager_id": 4},{"name": "Bob","id": 3,"dept_id": 2,"manager_id": 2},{"name": "Eva","id": 4,"dept_id": 3,"manager_id": 1},{"name": "Jack","id": 5,"dept_id": 1,"manager_id": 3},{"name": "Robin","id": 6,"dept_id": 3,"manager_id": 1},{"name": "Amy","id": 7,"dept_id": 2,"manager_id": 2},{"name": "May","id": 8,"dept_id": 1,"manager_id": 3}]|[{"name": "James","id": 2,"dept_id": 1,"manager_id": 4},{"name": "Bob","id": 3,"dept_id": 2,"manager_id": 2},{"name": "Eva","id": 4,"dept_id": 3,"manager_id": 1},{"name": "Jack","id": 5,"dept_id": 1,"manager_id": 3},{"name": "Robin","id": 6,"dept_id": 3,"manager_id": 1},{"name": "Amy","id": 7,"dept_id": 2,"manager_id": 2},{"name": "May","id": 8,"dept_id": 1,"manager_id": 3}]|Pass||

### Operation: @app.get("/employee/{emp_id}", response_model=schemas.Employee)
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|----|------|----------------|------------|------|-------|
|1|2|{"name": "James","id": 2,"dept_id": 1,"manager_id": 4}|{"name": "James","id": 2,"dept_id": 1,"manager_id": 4}|Pass|
|2|10|{"detail": "Employee not found"}|{"detail": "Employee not found"}|Pass||




### Operation: @app.put("/employee/{emp_id}", response_model=schemas.Employee)
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|----|------|----------------|------------|------|-------|
|1|[5, {"name": "Jim","salary": 0,"dept_id": 1,"manager_id": 3}]|{"name": "Jim","id": 5,"dept_id": 1,"manager_id": 3}|{"name": "Jim","id": 5,"dept_id": 1,"manager_id": 3}|Pass||
|2|[5, {"name": "dept not exist","salary": 0,"dept_id": 10,"manager_id": 3}]|{"detail": "Update employee failed. Target department does not exist."}|{"detail": "Update employee failed. Target department does not exist."}|Pass||
|3|[5, {"name": "manager not match","salary": 0,"dept_id": 1,"manager_id": 2}]|{"detail": "Update employee failed. Target manager does not exist in this department."}|{"detail": "Update employee failed. Target manager does not exist in this department."}|Pass||


### Operation: @app.delete("/employee/{emp_id}", response_model=list[schemas.Employee])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|----|------|----------------|------------|------|-------|
|1|1|[ ]|[ ]|Pass||
|2|5|[{"name": "James","id": 2,"dept_id": 1,"manager_id": 4},{"name": "Bob","id": 3,"dept_id": 2,"manager_id": 2},{"name": "Eva","id": 4,"dept_id": 3,"manager_id": 1},{"name": "Robin","id": 6,"dept_id": 3,"manager_id": 1},{"name": "Amy","id": 7,"dept_id": 2,"manager_id": 2},{"name": "May","id": 8,"dept_id": 1,"manager_id": 3}]|[{"name": "James","id": 2,"dept_id": 1,"manager_id": 4},{"name": "Bob","id": 3,"dept_id": 2,"manager_id": 2},{"name": "Eva","id": 4,"dept_id": 3,"manager_id": 1},{"name": "Robin","id": 6,"dept_id": 3,"manager_id": 1},{"name": "Amy","id": 7,"dept_id": 2,"manager_id": 2},{"name": "May","id": 8,"dept_id": 1,"manager_id": 3}]|Pass||

### Operation: @app.delete("/employee/")
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|----|------|----------------|------------|------|-------|
|1|/|{"Drop table employee": "True"}|{"Drop table employee": "True"}|Pass||