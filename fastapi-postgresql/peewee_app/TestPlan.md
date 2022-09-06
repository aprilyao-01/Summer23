# Test Plan
This file records the test plan for [`main.py`](/fastapi-postgresql/sqlalchemy_app/main.py). Ordered by table, operation.
* [Table: department](#table-department)
    * POST
        * [All](#operation-apppostdepartment-responsemodellistschemasdepartment-dependenciesdependsgetdb)
    * GET
        * [All](#operation-appgetdepartment-responsemodellistschemasdepartment-dependenciesdependsgetdb)
        * [By Id](#operation-appgetdepartmentdeptid-responsemodelschemasdepartment-dependenciesdependsgetdb)
    * PUT
        * [By Id](#operation-appputdepartmentdeptid-responsemodelschemasdepartment-dependenciesdependsgetdb)
    * DELETE
        * [By Id](#operation-appdeletedepartmentdeptid-responsemodellistschemasdepartment-dependenciesdependsgetdb)
        * [Drop Table](#operation-appdeletedepartment-dependenciesdependsgetdb)
* [Table: manager](#table-manager)
    * POST
        * [All](#operation-apppostmanager-responsemodellistschemasmanager-dependenciesdependsgetdb)
    * GET
        * [All](#operation-appgetmanager-responsemodellistschemasmanager-dependenciesdependsgetdb)
        * [By Department](#operation-appgetmanagerdeptid-responsemodellistschemasmanager-dependenciesdependsgetdb)
    * PUT
        * [By Id](#operation-appputmanagermngid-responsemodelschemasmanager-dependenciesdependsgetdb)
    * DELETE
        * [By Id](#operation-appdeletemanagermngid-responsemodellistschemasmanager-dependenciesdependsgetdb)
        * [Drop table](#operation-appdeletemanager-dependenciesdependsgetdb)
* [Table: employee](#table-employee)
    * POST
        * [All](#operation-apppostemployee-responsemodellistschemasemployee-dependenciesdependsgetdb)
    * GET
        * [All](#operation-appgetemployee-responsemodellistschemasemployee-dependenciesdependsgetdb)
        * [By Id](#operation-appgetemployeeempid-responsemodelschemasemployee-dependenciesdependsgetdb)
    * PUT
        * [By Id](#operation-appputemployeeempid-responsemodelschemasemployee-dependenciesdependsgetdb)
    * DELETE
        * [By Id](#operation-appdeleteemployeeempid-responsemodellistschemasemployee-dependenciesdependsgetdb)
        * [Drop table](#operation-appdeleteemployee-dependenciesdependsgetdb)


## Table: department
### Operation: @app.post("/department/", response_model=list[schemas.Department], dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|[{"name": "IT"}]|[{"name": "IT","id": 1,"has_managers": [],"has_employees": []}], Success add 1 record(s). Skip 0 record(s).|AttributeError: type object 'Department' has no attribute 'where'|Fail|replace all `where()` with `filter()`|
|2|[{"name": "IT"}]|[{"name": "IT","id": 1,"has_managers": [],"has_employees": []}], Success add 1 record(s). Skip 0 record(s).|peewee_app.models.DepartmentDoesNotExist: <Model: Department> instance matching query does not exist: SQL: SELECT "t1"."id", "t1"."name" FROM "department" AS "t1" WHERE ("t1"."name" = %s) LIMIT %s OFFSET %s Params: ['IT', 1, 0]|Fail|replace `.filter.get()` with `filter().first()`|
|3|[{"name": "IT"}]|<mark>[{"name": "IT","id": 1,"has_managers": [],"has_employees": []}]</mark>, Success add 1 record(s). Skip 0 record(s).|~~pydantic.error_wrappers.ValidationError: 2 validation errors for Department response -> 0 -> has_managers value is not a valid list (type=type_error.list) response -> 0 -> has_employees value is not a valid list (type=type_error.list)~~, Success add 1 record(s). Skip 0 record(s).|Fail|`models.Department.create()` returns an int for success inserted number. change `succ_add.append()`|
|4|[{"name": "IT"}, {"name": "HR"}, {"name": "Finance"}, {"name": "Admin"}]|[{ "name": "IT","id": 1,"has_managers": [],"has_employees": []},{"name": "HR","id": 2,"has_managers": [],"has_employees": []},{"name": "Finance","id": 3,"has_managers": [],"has_employees": []},{"name": "Admin","id": 4,"has_managers": [],"has_employees": []}]|pydantic.error_wrappers.ValidationError|Fail|because the `peewee lazy loading`, add new function in crud `response_department(department: schemas.Department)`|
|5|[{"name": "IT"}, {"name": "HR"}, {"name": "Finance"}, {"name": "Admin"}]|[{ "name": "IT","id": 1,"has_managers": [],"has_employees": []},{"name": "HR","id": 2,"has_managers": [],"has_employees": []},{"name": "Finance","id": 3,"has_managers": [],"has_employees": []},{"name": "Admin","id": 4,"has_managers": [],"has_employees": []}]|{"detail": "'NoneType' object has no attribute 'has_managers'"}|Fail|add `if statement` for `NoneType` in `crud.select_department_by_name`|
|6|[{"name": "test"}]|[{ "name": "test","id": 7,"has_managers": [],"has_employees": []}]|[{ "name": "test","id": 7,"has_managers": [],"has_employees": []}]|Pass||
|7|[{"name": "IT"}, {"name": "HR"}, {"name": "Finance"}, {"name": "Admin"}]|[{ "name": "IT","id": 1,"has_managers": [],"has_employees": []},{"name": "HR","id": 2,"has_managers": [],"has_employees": []},{"name": "Finance","id": 3,"has_managers": [],"has_employees": []},{"name": "Admin","id": 4,"has_managers": [],"has_employees": []}]|[{ "name": "IT","id": 1,"has_managers": [],"has_employees": []},{"name": "HR","id": 2,"has_managers": [],"has_employees": []},{"name": "Finance","id": 3,"has_managers": [],"has_employees": []},{"name": "Admin","id": 4,"has_managers": [],"has_employees": []}]|Pass||
|8|[{"name": "IT"}, {"name": "HR"}, {"name": "Finance"}, {"name": "Admin"}]|[ ], Success add 0 record(s). Skip 4 record(s).|[ ], Success add 0 record(s). Skip 4 record(s).|Pass||



### Operation: @app.get("/department/", response_model=list[schemas.Department], dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|/|[{"name": "IT","id": 1,"has_managers": [],"has_employees": []}]|pydantic.error_wrappers.ValidationError: 2 validation errors for Department response -> has_managers value is not a valid list (type=type_error.list) response -> has_employees value is not a valid list (type=type_error.list)|Fail|`list(models.Department.select().offset(skip).limit(limit))` return list `[<Department: 1>]`, which has {"id":1,"name": IT,~~"has_managers":"SELECT "t1"."id", "t1"."name", "t1"."dept_id" FROM "manager" AS "t1" WHERE ("t1"."dept_id" = 1)", "has_employees": "SELECT "t1"."id", "t1"."name", "t1"."salary", "t1"."dept_id", "t1"."manager_id" FROM "employee" AS "t1" WHERE ("t1"."dept_id" = 1)"~~}. Conflict with `response_model`. because the `peewee lazy loading`, add new function in crud `response_department(department: schemas.Department)`|
|2|/|[{"name": "IT","id": 1,"has_managers": [],"has_employees": []}]|pydantic.error_wrappers.ValidationError: 3 validation errors for Department response -> has_employees -> 0|Fail| change the schemas.py from ` has_employees: list[list[EmployeeNameList]] = []` to ` has_employees: list[EmployeeNameList] = []` |
|3|/|[{"name": "IT","id": 1,"has_managers": [{"name": "Nick"},{"name": "Cory"}],"has_employees": [{"name": "James"},{"name": "Jack"},{"name": "May"}]},{"name": "HR","id": 2,"has_managers": [],"has_employees": [{"name": "Bob"},{"name": "Amy"}]},{"name": "Finance","id": 3,"has_managers": [{"name": "Prem"}],"has_employees": [{"name": "Eva"},{"name": "Robin"}]},{"name": "Admin","id": 4,"has_managers": [{"name": "Shripadh"}],"has_employees": []}]|[{"name": "IT","id": 1,"has_managers": [{"name": "Nick"},{"name": "Cory"}],"has_employees": [{"name": "James"},{"name": "Jack"},{"name": "May"}]},{"name": "HR","id": 2,"has_managers": [],"has_employees": [{"name": "Bob"},{"name": "Amy"}]},{"name": "Finance","id": 3,"has_managers": [{"name": "Prem"}],"has_employees": [{"name": "Eva"},{"name": "Robin"}]},{"name": "Admin","id": 4,"has_managers": [{"name": "Shripadh"}],"has_employees": []}]|Pass||

### Operation: @app.get("/department/{dept_id}", response_model=schemas.Department, dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|1|[{"name": "IT","id": 1,"has_managers": [],"has_employees": []}]| peewee_app.models.DepartmentDoesNotExist: <Model: Department> instance matching query does not exist: SQL: SELECT "t1"."id", "t1"."name" FROM "department" AS "t1" WHERE ("t1"."id" = %s) LIMIT %s OFFSET %s Params: [1, 1, 0]|Fail| replace all `department is None` to `except module.Department.DoesNotExist:`|
|2|1|{ "detail": "Department not found"}| { "detail": "Department not found"}|Pass||
|3|2|{"name": "HR","id": 2,"has_managers": [],"has_employees": [{"name": "Bob"},{"name": "Amy"}]}|{"name": "HR","id": 2,"has_managers": [],"has_employees": [{"name": "Bob"},{"name": "Amy"}]}|Pass||


### Operation: @app.put("/department/{dept_id}", response_model=schemas.Department, dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|[8, {"name": "HR"}]|<mark>400 Bad Request</mark>, {"detail":<mark>"Department already existed"</mark>}|~~500 Internal Server Error~~, {"detail":~~""~~}|Fail|commented `except Exception as e:`|
|2|[8, {"name": "HR"}]|{"detail":"Department already existed"}|{"detail":"Department already existed"}|Pass||
|3|[8, {"name": "test"}]|{"name": <mark>"test"</mark>,"id": 8,"has_managers": [],"has_employees": []}|{"name":~~"IT"~~,"id": 8,"has_managers": [],"has_employees": []}|Fail|db changed, wrong response body message, change return variable|
|4|[8, {"name": "test"}]|{"name": "test","id": 8,"has_managers": [],"has_employees": []}|{"name": "test","id": 8,"has_managers": [],"has_employees": []}|Pass||
|5|[7,{"name": "dept not exist"}]|{"detail":"Department not found"}|{"detail":"Department not found"}|Pass||



### Operation: @app.delete("/department/{dept_id}", response_model=list[schemas.Department], dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|1|[ ]|[ ]|Pass||
|2|4|[{"name": "IT","id": 1,"has_managers": [{"name": "Nick"},{"name": "Cory"}],"has_employees": [{"name": "James"},{"name": "Jack"},{"name": "May"}]},{"name": "HR","id": 2,"has_managers": [],"has_employees": [{"name": "Bob"},{"name": "Amy"}]},{"name": "Finance","id": 3,"has_managers": [{"name": "Prem"}],"has_employees": [{"name": "Eva"},{"name": "Robin"}]}| "detail": "null value in column \"dept_id\" of relation \"manager\" violates not-null constraint\nDETAIL:  Failing row contains (2, Shripadh, null).\nCONTEXT:  SQL statement \"UPDATE ONLY \"public\".\"manager\" SET \"dept_id\" = NULL WHERE $1 OPERATOR(pg_catalog.=) \"dept_id\"\"\n"|Fail|add `null=True` in `models.Manager.dept`|
|3|4|[{"name": "IT","id": 1,"has_managers": [{"name": "Nick"},{"name": "Cory"}],"has_employees": [{"name": "James"},{"name": "Jack"},{"name": "May"}]},{"name": "HR","id": 2,"has_managers": [],"has_employees": [{"name": "Bob"},{"name": "Amy"}]},{"name": "Finance","id": 3,"has_managers": [{"name": "Prem"}],"has_employees": [{"name": "Eva"},{"name": "Robin"}]}|[{"name": "IT","id": 1,"has_managers": [{"name": "Nick"},{"name": "Cory"}],"has_employees": [{"name": "James"},{"name": "Jack"},{"name": "May"}]},{"name": "HR","id": 2,"has_managers": [],"has_employees": [{"name": "Bob"},{"name": "Amy"}]},{"name": "Finance","id": 3,"has_managers": [{"name": "Prem"}],"has_employees": [{"name": "Eva"},{"name": "Robin"}]}|Pass||
|4|1|{ "detail": "Department table been dropped"} |{ "detail": "Department table been dropped"}|Pass||



### Operation: @app.delete("/department/", dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|/|{"Drop table department": "True"}|{"Drop table department": "True"}|Pass||




## Table: manager
### Operation: @app.post("/manager/", response_model=list[schemas.Manager], dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|[{"name": "Prem","dept_id": 3}]|[{"name": "Prem","id": 1,"dept_id": 3,"monitor_employee": []}], Success add 1 record(s). Skip 0 record(s).|{"detail": "'NoneType' object has no attribute 'with_employee'"}|Fail|add `if statement` for `NoneType` in `crud.select_manager_by_dept_and_name`|
|2|[{"name": "Shripadh","dept_id": 4}]|[{"name": "Shripadh","id": 2,"dept_id": 4,"monitor_employee": []}], Success add 1 record(s). Skip 0 record(s).|[{"name": "Shripadh","id": 2,"dept_id": 4,"monitor_employee": []}], Success add 1 record(s). Skip 0 record(s).|Pass||
|3|[{"name": "Prem","dept_id": 3},{"name": "Shripadh","dept_id": 4},{"name": "Nick","dept_id": 1},{"name": "Cory","dept_id": 1}]|[{"name": "Nick","id": 3,"dept_id": 1,"with_employee": []},{"name": "Cory","id": 4,"dept_id": 1,"with_employee": []}], Success add 2 record(s). Skip 2 record(s).|[{"name": "Nick","id": 3,"dept_id": 1,"with_employee": []},{"name": "Cory","id": 4,"dept_id": 1,"with_employee": []}], Success add 2 record(s). Skip 2 record(s).|Pass||
|4|[{"name": "Prem","dept_id": 3},{"name": "Shripadh","dept_id": 4},{"name": "Nick","dept_id": 1},{"name": "Cory","dept_id": 1}]|[{"name": "Nick","id": 3,"dept_id": 1,"with_employee": []},{"name": "Cory","id": 4,"dept_id": 1,"with_employee": []}], Insert skipped. Manager Shripadh already existed in this department. For people have same name, try nickname such as: Mike & Mike Junior. Success add 2 record(s). Skip 2 record(s).|[{"name": "Nick","id": 3,"dept_id": 1,"with_employee": []},{"name": "Cory","id": 4,"dept_id": 1,"with_employee": []}], Insert skipped. Manager Shripadh already existed in this department. For people have same name, try nickname such as: Mike & Mike Junior. Success add 2 record(s). Skip 2 record(s).|Pass||
|5|[{"name": "dept not exist","dept_id": 30}]|[], Insert skipped. Department 30 does not exist! Success add 0 record(s). Skip 1 record(s).|[], Insert skipped. Department 30 does not exist! Success add 0 record(s). Skip 1 record(s).|Pass||


### Operation: @app.get("/manager/", response_model=list[schemas.Manager], dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|/|[{"name": "Prem","id": 1,"dept_id": 3,"with_employee": [{"name": "Eva"},{"name": "Robin"}]},{"name": "Nick","id": 3,"dept_id": 1,"with_employee": [{"name": "Jack"},{"name": "May"}]},{"name": "Cory","id": 4,"dept_id": 1,"with_employee": [{"name": "James"}]},{"name": "Jack","id": 2,"dept_id": 2,"with_employee": [{"name": "Bob"},{"name": "Amy"}]}]|pydantic.error_wrappers.ValidationError: 4 validation errors for Manager response -> 0 -> with_employee value is not a valid list (type=type_error.list)|Fail|because the `peewee lazy loading`, change the crud method, add `for manager in managers: manager.with_employee = list(manager.with_employee)`|
|2|/|[{"name": "Prem","id": 1,"dept_id": 3,"with_employee": [{"name": "Eva"},{"name": "Robin"}]},{"name": "Nick","id": 3,"dept_id": 1,"with_employee": [{"name": "Jack"},{"name": "May"}]},{"name": "Cory","id": 4,"dept_id": 1,"with_employee": [{"name": "James"}]},{"name": "Jack","id": 2,"dept_id": 2,"with_employee": [{"name": "Bob"},{"name": "Amy"}]}]|[{"name": "Prem","id": 1,"dept_id": 3,"with_employee": [{"name": "Eva"},{"name": "Robin"}]},{"name": "Nick","id": 3,"dept_id": 1,"with_employee": [{"name": "Jack"},{"name": "May"}]},{"name": "Cory","id": 4,"dept_id": 1,"with_employee": [{"name": "James"}]},{"name": "Jack","id": 2,"dept_id": 2,"with_employee": [{"name": "Bob"},{"name": "Amy"}]}]|Pass|change the previous test changes to new function in crud `response_manager(manager: schemas.Manager)`|
|3|/|[{"name": "Prem","id": 1,"dept_id": 3,"with_employee": [{"name": "Eva"},{"name": "Robin"}]},{"name": "Shripadh","id": 2,"dept_id": 4,"with_employee": [{"name": "Bob"},{"name": "Amy"}]},{"name": "Nick","id": 3,"dept_id": 1,"with_employee": [{"name": "Jack"},{"name": "May"}]},{"name": "Cory","id": 4,"dept_id": 1,"with_employee": [{"name": "James"}]}]|[{"name": "Prem","id": 1,"dept_id": 3,"with_employee": [{"name": "Eva"},{"name": "Robin"}]},{"name": "Shripadh","id": 2,"dept_id": 4,"with_employee": [{"name": "Bob"},{"name": "Amy"}]},{"name": "Nick","id": 3,"dept_id": 1,"with_employee": [{"name": "Jack"},{"name": "May"}]},{"name": "Cory","id": 4,"dept_id": 1,"with_employee": [{"name": "James"}]}]|Pass||
|4|/|{"detail": <mark>"Manager table been dropped"</mark>}|{"detail": ~~""~~}|Fail|commend `except Exception as e:`|
|5|/|{ "detail": "Manager table been dropped"} |{ "detail": "Manager table been dropped"}|Pass||

### Operation: @app.get("/manager/{dept_id}", response_model=list[schemas.Manager], dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|3|[{"name": "Prem","id": 1,"dept_id": 3,"with_employee": [{"name": "Robin"}]}]|pydantic.error_wrappers.ValidationError: 4 validation errors for Manager response -> 0 -> with_employee value is not a valid list (type=type_error.list)|Fail|because the `peewee lazy loading`, add new function in crud `response_manager(manager: schemas.Manager)`|
|2|3|[{"name": "Prem","id": 1,"dept_id": 3,"with_employee": [{"name": "Robin"}]}]|[{"name": "Prem","id": 1,"dept_id": 3,"with_employee": [{"name": "Robin"}]}]|Pass||
|3|20|{"detail": "Manager not found"}|[]|Fail|since function return `None`, change the `models.Manager.DoesNotExist` exception handle to if statement|
|4|20|{"detail": "Department does not exist"}|{"detail": "Department does not exist"}|Pass||
|5|2|404 Not Found, {"detail": <mark>"Manager not found in this department"</mark>}|~~500 Internal Server Error~~, {"detail": ~~""~~}|Fail|commend `except Exception as e:`|
|6|1|{ "detail": "Manager table been dropped"} |{ "detail": "Manager table been dropped"}|Pass||

### Operation: @app.put("/manager/{mng_id}", response_model=schemas.Manager, dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|[{"name": "Prem","dept_id": 3}]|[{"name": "Prem","id": 1,"dept_id": 3,"monitor_employee": []}], Success add 1 record(s). Skip 0 record(s).|{"detail": "'NoneType' object has no attribute 'with_employee'"}|Fail|add `if statement` for `NoneType` in `crud.select_manager_by_dept_and_name`|
|2|[{"name": "Shripadh","dept_id": 4}]|[{"name": "Shripadh","id": 2,"dept_id": 4,"monitor_employee": []}], Success add 1 record(s). Skip 0 record(s).|[{"name": "Shripadh","id": 2,"dept_id": 4,"monitor_employee": []}], Success add 1 record(s). Skip 0 record(s).|Pass||
|3|[{"name": "Prem","dept_id": 3},{"name": "Shripadh","dept_id": 4},{"name": "Nick","dept_id": 1},{"name": "Cory","dept_id": 1}]|[{"name": "Nick","id": 3,"dept_id": 1,"with_employee": []},{"name": "Cory","id": 4,"dept_id": 1,"with_employee": []}], Success add 2 record(s). Skip 2 record(s).|[{"name": "Nick","id": 3,"dept_id": 1,"with_employee": []},{"name": "Cory","id": 4,"dept_id": 1,"with_employee": []}], Success add 2 record(s). Skip 2 record(s).|Pass||
|4|[{"name": "Prem","dept_id": 3},{"name": "Shripadh","dept_id": 4},{"name": "Nick","dept_id": 1},{"name": "Cory","dept_id": 1}]|[{"name": "Nick","id": 3,"dept_id": 1,"with_employee": []},{"name": "Cory","id": 4,"dept_id": 1,"with_employee": []}], Insert skipped. Manager Shripadh already existed in this department. For people have same name, try nickname such as: Mike & Mike Junior. Success add 2 record(s). Skip 2 record(s).|[{"name": "Nick","id": 3,"dept_id": 1,"with_employee": []},{"name": "Cory","id": 4,"dept_id": 1,"with_employee": []}], Insert skipped. Manager Shripadh already existed in this department. For people have same name, try nickname such as: Mike & Mike Junior. Success add 2 record(s). Skip 2 record(s).|Pass||
|5|[{"name": "dept not exist","dept_id": 30}]|[], Insert skipped. Department 30 does not exist! Success add 0 record(s). Skip 1 record(s).|[], Insert skipped. Department 30 does not exist! Success add 0 record(s). Skip 1 record(s).|Pass||

### Operation: @app.delete("/manager/{mng_id}", response_model=list[schemas.Manager], dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|5|[{"name": "Prem","id": 1,"dept_id": 3,"with_employee": [{"name": "Eva"},{"name": "Robin"}]},{"name": "Shripadh","id": 2,"dept_id": 4,"with_employee": [{"name": "Bob"},{"name": "Amy"}]},{"name": "Nick","id": 3,"dept_id": 1,"with_employee": [{"name": "Jack"},{"name": "May"}]},{"name": "Cory","id": 4,"dept_id": 1,"with_employee": [{"name": "James"}]}]|[{"name": "Prem","id": 1,"dept_id": 3,"with_employee": [{"name": "Eva"},{"name": "Robin"}]},{"name": "Shripadh","id": 2,"dept_id": 4,"with_employee": [{"name": "Bob"},{"name": "Amy"}]},{"name": "Nick","id": 3,"dept_id": 1,"with_employee": [{"name": "Jack"},{"name": "May"}]},{"name": "Cory","id": 4,"dept_id": 1,"with_employee": [{"name": "James"}]}]|Pass||
|2|10|{"detail": "Manager does not exist"}|{"detail": "Manager does not exist"}|Pass||
|3|1|{"detail": <mark>"Manager table been dropped"</mark>}|{"detail": ~~""~~}|Fail|commend `except Exception as e:`|
|4|1|{"detail": "Manager table been dropped"}|{"detail": "Manager table been dropped"}|Pass||

### Operation: @app.delete("/manager/", dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|/|{"Drop table manager": "True"}|{"Drop table manager": "True"}|Pass||




## Table: employee
### Operation: @app.post("/employee/", response_model=list[schemas.Employee], dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|[{"name": "James","salary": 8000,"dept_id": 1,"manager_id": 1}]|[ ],Insert skipped. Department 1 does not have manager 1. Success add 0 record(s). Skip 1 record(s).|[ ], Insert skipped. Department 1 does not have manager 1. Success add 0 record(s). Skip 1 record(s).|Pass||
|2|[{"name": "James","salary": 8000,"dept_id": 1,"manager_id": 4},{"name": "Bob","salary": 9500,"dept_id": 2,"manager_id": 2},{"name": "Eva","salary": 7000,"dept_id": 3,"manager_id": 1},{"name": "Jack","salary": 8000,"dept_id": 1,"manager_id": 3},{"name": "Robin","salary": 20000,"dept_id": 3,"manager_id": 1},{"name": "Amy","salary": 15000,"dept_id": 2,"manager_id": 2},{"name": "May","salary": 5000,"dept_id": 1,"manager_id": 3}]|[{"name": "James","id": 2,"dept_id": 1,"manager_id": 4},{"name": "Bob","id": 3,"dept_id": 2,"manager_id": 2},{"name": "Eva","id": 4,"dept_id": 3,"manager_id": 1},{"name": "Jack","id": 5,"dept_id": 1,"manager_id": 3},{"name": "Robin","id": 6,"dept_id": 3,"manager_id": 1},{"name": "Amy","id": 7,"dept_id": 2,"manager_id": 2},{"name": "May","id": 8,"dept_id": 1,"manager_id": 3}], Success add 7 record(s). Skip 0 record(s).|[{"name": "James","id": 2,"dept_id": 1,"manager_id": 4},{"name": "Bob","id": 3,"dept_id": 2,"manager_id": 2},{"name": "Eva","id": 4,"dept_id": 3,"manager_id": 1},{"name": "Jack","id": 5,"dept_id": 1,"manager_id": 3},{"name": "Robin","id": 6,"dept_id": 3,"manager_id": 1},{"name": "Amy","id": 7,"dept_id": 2,"manager_id": 2},{"name": "May","id": 8,"dept_id": 1,"manager_id": 3}], Success add 7 record(s). Skip 0 record(s).|Pass||
|3|[{"name": "dept not exist","salary": 8000,"dept_id": 10,"manager_id": 1}]|[ ],Insert skipped. Department 10 does not exist! Success add 0 record(s). Skip 1 record(s).|[ ],Insert skipped. Department 10 does not exist! Success add 0 record(s). Skip 1 record(s).|Pass||
|4|[{"name": "mng not exist","salary": 8000,"dept_id": 2,"manager_id": 7}]|[ ],Insert skipped. Manager 7 does not exist! Success add 0 record(s). Skip 1 record(s).|peewee_app.models.ManagerDoesNotExist: <Model: Manager> instance matching query does not exist: |Fail|add another `select_manager_by_id` which return `None` instead of raise exception|
|5|[{"name": "mng not exist","salary": 8000,"dept_id": 2,"manager_id": 7}]|[ ],Insert skipped. Manager 7 does not exist! Success add 0 record(s). Skip 1 record(s).|[ ],Insert skipped. Manager 7 does not exist! Success add 0 record(s). Skip 1 record(s).|Pass||


### Operation: @app.get("/employee/", response_model=list[schemas.Employee], dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|/|[{"name": "James","id": 1,"dept_id": 1,"manager_id": 4},{"name": "Bob","id": 2,"dept_id": 2,"manager_id": 2},{"name": "Eva","id": 3,"dept_id": 3,"manager_id": 1},{"name": "Jack","id": 4,"dept_id": 1,"manager_id": 3},{"name": "Robin","id": 5,"dept_id": 3,"manager_id": 1},{"name": "Amy","id": 6,"dept_id": 2,"manager_id": 2},{"name": "May","id": 7,"dept_id": 1,"manager_id": 3}]|[{"name": "James","id": 1,"dept_id": 1,"manager_id": 4},{"name": "Bob","id": 2,"dept_id": 2,"manager_id": 2},{"name": "Eva","id": 3,"dept_id": 3,"manager_id": 1},{"name": "Jack","id": 4,"dept_id": 1,"manager_id": 3},{"name": "Robin","id": 5,"dept_id": 3,"manager_id": 1},{"name": "Amy","id": 6,"dept_id": 2,"manager_id": 2},{"name": "May","id": 7,"dept_id": 1,"manager_id": 3}]|Pass||


### Operation: @app.get("/employee/{emp_id}", response_model=schemas.Employee, dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|2|{"name": "Bob","id": 2,"dept_id": 2,"manager_id": 2}|{"name": "Bob","id": 2,"dept_id": 2,"manager_id": 2}|Pass||
|2|20|{"detail":"Employee not found"}|{"detail":"Employee not found"}|Pass||
|3|2|{"detail":<mark>"Employee table been dropped"</mark>}|{"detail": ~~""~~}|Fail|commend `except Exception as e:`|
|4|2|{"detail":"Employee table been dropped"}|{"detail":"Employee table been dropped"}|Pass||


### Operation: @app.put("/employee/{emp_id}", response_model=schemas.Employee, dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|[5, {"name": "Jim","salary": -2,"dept_id": 1,"manager_id": 3}]|{"detail": "Update employee failed. Salary cannot less than 0"}|peewee.IntegrityError: new row for relation "employee" violates check constraint "employee_salary_check" DETAIL:  Failing row contains (5, Jim, 0, 1, 3).|Fail|add salary check `salary>=0`|
|2|[5, {"name": "Jim","salary": -2,"dept_id": 1,"manager_id": 3}]|{"detail": "Update employee failed. Salary cannot less than 0"}|{"detail": "Update employee failed. Salary cannot less than 0"}|Pass||
|3|[5, {"name": "dept not exist","salary": 0,"dept_id": 10,"manager_id": 3}]|{"detail": "Update employee failed. Target department does not exist."}|{"detail": "Update employee failed. Target department does not exist."}|Pass||
|4|[5, {"name": "manager not match","salary": 100,"dept_id": 1,"manager_id": 2}]|{"detail": "Update employee failed. Target manager does not exist in this department."}|{"detail": "Update employee failed. Target manager does not exist in this department."}|Pass||



### Operation: @app.delete("/employee/{emp_id}", response_model=list[schemas.Employee], dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|3|[{"name": "James","id": 1,"dept_id": 1,"manager_id": 4},{"name": "Bob","id": 2,"dept_id": 2,"manager_id": 2},{"name": "Jack","id": 4,"dept_id": 1,"manager_id": 3},{"name": "Robin","id": 5,"dept_id": 3,"manager_id": 1},{"name": "Amy","id": 6,"dept_id": 2,"manager_id": 2},{"name": "May","id": 7,"dept_id": 1,"manager_id": 3}]|{"detail": "int() argument must be a string, a bytes-like object or a number, not 'builtin_function_or_method'"}|Fail|change the `crud.delete_employee_by_id` parameter setting|
|2|3|[{"name": "James","id": 1,"dept_id": 1,"manager_id": 4},{"name": "Bob","id": 2,"dept_id": 2,"manager_id": 2},{"name": "Jack","id": 4,"dept_id": 1,"manager_id": 3},{"name": "Robin","id": 5,"dept_id": 3,"manager_id": 1},{"name": "Amy","id": 6,"dept_id": 2,"manager_id": 2},{"name": "May","id": 7,"dept_id": 1,"manager_id": 3}]|[{"name": "James","id": 1,"dept_id": 1,"manager_id": 4},{"name": "Bob","id": 2,"dept_id": 2,"manager_id": 2},{"name": "Jack","id": 4,"dept_id": 1,"manager_id": 3},{"name": "Robin","id": 5,"dept_id": 3,"manager_id": 1},{"name": "Amy","id": 6,"dept_id": 2,"manager_id": 2},{"name": "May","id": 7,"dept_id": 1,"manager_id": 3}]|Pass||
|3|20|{"detail": "Employee does not exist"}|{"detail": "Employee does not exist"}|Pass||
|4|1|{"detail": "Employee table been dropped"}|{ "detail": "relation \"employee\" does not exist\nLINE 1: ....\"salary\", \"t1\".\"dept_id\", \"t1\".\"manager_id\" FROM \"employee\"...\n ^\n"}|Fail|commend `except Exception as e:`|
|5|1|{"detail": "Employee table been dropped"}|{"detail": "Employee table been dropped"}|Pass||


### Operation: @app.delete("/employee/", dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|/|{"Drop table employee": "True"}|{"Drop table employee": "True"}|Pass||
