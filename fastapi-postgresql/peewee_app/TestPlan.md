# Test Plan
This file records the test plan for [`main.py`](/fastapi-postgresql/sqlalchemy_app/main.py). Ordered by table, operation.
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
### Operation: @app.post("/department/", response_model=list[schemas.Department], dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|[{"name": "IT"}]|[{"name": "IT","id": 1,"has_managers": [],"has_employees": []}], Success add 1 record(s). Skip 0 record(s).|AttributeError: type object 'Department' has no attribute 'where'|Fail|replace all `where()` with `filter()`|
|2|[{"name": "IT"}]|[{"name": "IT","id": 1,"has_managers": [],"has_employees": []}], Success add 1 record(s). Skip 0 record(s).|peewee_app.models.DepartmentDoesNotExist: <Model: Department> instance matching query does not exist: SQL: SELECT "t1"."id", "t1"."name" FROM "department" AS "t1" WHERE ("t1"."name" = %s) LIMIT %s OFFSET %s Params: ['IT', 1, 0]|Fail|replace `.filter.get()` with `filter().first()`|
|3|[{"name": "IT"}]|<mark>[{"name": "IT","id": 1,"has_managers": [],"has_employees": []}]</mark>, Success add 1 record(s). Skip 0 record(s).|~~pydantic.error_wrappers.ValidationError: 2 validation errors for Department response -> 0 -> has_managers value is not a valid list (type=type_error.list) response -> 0 -> has_employees value is not a valid list (type=type_error.list)~~, Success add 1 record(s). Skip 0 record(s).|Fail|`models.Department.create()` returns an int for success inserted number. change `succ_add.append()`|
|4|[{"name": "IT"}, {"name": "HR"}, {"name": "Finance"}, {"name": "Admin"}]|[{ "name": "IT","id": 1,"has_managers": [],"has_employees": []},{"name": "HR","id": 2,"has_managers": [],"has_employees": []},{"name": "Finance","id": 3,"has_managers": [],"has_employees": []},{"name": "Admin","id": 4,"has_managers": [],"has_employees": []}]|pydantic.error_wrappers.ValidationError|Fail|because the `peewee lazy loading`, add new function in crud `response_department(department: schemas.Department)`|
|5|[{"name": "test"}]|[{ "name": "test","id": 5,"has_managers": [],"has_employees": []}]|



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

### Operation: @app.delete("/department/{dept_id}", response_model=list[schemas.Department], dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|1|[ ]|[ ]|Pass||
|2|4|[{"name": "IT","id": 1,"has_managers": [{"name": "Nick"},{"name": "Cory"}],"has_employees": [{"name": "James"},{"name": "Jack"},{"name": "May"}]},{"name": "HR","id": 2,"has_managers": [],"has_employees": [{"name": "Bob"},{"name": "Amy"}]},{"name": "Finance","id": 3,"has_managers": [{"name": "Prem"}],"has_employees": [{"name": "Eva"},{"name": "Robin"}]}| "detail": "null value in column \"dept_id\" of relation \"manager\" violates not-null constraint\nDETAIL:  Failing row contains (2, Shripadh, null).\nCONTEXT:  SQL statement \"UPDATE ONLY \"public\".\"manager\" SET \"dept_id\" = NULL WHERE $1 OPERATOR(pg_catalog.=) \"dept_id\"\"\n"|Fail|add `null=True` in `models.Manager.dept`|
|3|4|[{"name": "IT","id": 1,"has_managers": [{"name": "Nick"},{"name": "Cory"}],"has_employees": [{"name": "James"},{"name": "Jack"},{"name": "May"}]},{"name": "HR","id": 2,"has_managers": [],"has_employees": [{"name": "Bob"},{"name": "Amy"}]},{"name": "Finance","id": 3,"has_managers": [{"name": "Prem"}],"has_employees": [{"name": "Eva"},{"name": "Robin"}]}|**TO TEST after drop all tables and reset**|


### Operation: @app.delete("/department/", dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|/|{"Drop table department": "True"}|{"Drop table department": "True"}|Pass||




## Table: manager
### Operation: @app.get("/manager/", response_model=list[schemas.Manager], dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|/|[{"name": "Prem","id": 1,"dept_id": 3,"with_employee": [{"name": "Eva"},{"name": "Robin"}]},{"name": "Nick","id": 3,"dept_id": 1,"with_employee": [{"name": "Jack"},{"name": "May"}]},{"name": "Cory","id": 4,"dept_id": 1,"with_employee": [{"name": "James"}]},{"name": "Jack","id": 2,"dept_id": 2,"with_employee": [{"name": "Bob"},{"name": "Amy"}]}]|pydantic.error_wrappers.ValidationError: 4 validation errors for Manager response -> 0 -> with_employee value is not a valid list (type=type_error.list)|Fail|because the `peewee lazy loading`, change the crud method, add `for manager in managers: manager.with_employee = list(manager.with_employee)`|
|2|/|[{"name": "Prem","id": 1,"dept_id": 3,"with_employee": [{"name": "Eva"},{"name": "Robin"}]},{"name": "Nick","id": 3,"dept_id": 1,"with_employee": [{"name": "Jack"},{"name": "May"}]},{"name": "Cory","id": 4,"dept_id": 1,"with_employee": [{"name": "James"}]},{"name": "Jack","id": 2,"dept_id": 2,"with_employee": [{"name": "Bob"},{"name": "Amy"}]}]|[{"name": "Prem","id": 1,"dept_id": 3,"with_employee": [{"name": "Eva"},{"name": "Robin"}]},{"name": "Nick","id": 3,"dept_id": 1,"with_employee": [{"name": "Jack"},{"name": "May"}]},{"name": "Cory","id": 4,"dept_id": 1,"with_employee": [{"name": "James"}]},{"name": "Jack","id": 2,"dept_id": 2,"with_employee": [{"name": "Bob"},{"name": "Amy"}]}]|Pass|change the previous test changes to new function in crud `response_manager(manager: schemas.Manager)`|
|3|/|[{"name": "Prem","id": 1,"dept_id": 3,"with_employee": [{"name": "Eva"},{"name": "Robin"}]},{"name": "Shripadh","id": 2,"dept_id": 4,"with_employee": [{"name": "Bob"},{"name": "Amy"}]},{"name": "Nick","id": 3,"dept_id": 1,"with_employee": [{"name": "Jack"},{"name": "May"}]},{"name": "Cory","id": 4,"dept_id": 1,"with_employee": [{"name": "James"}]}]|[{"name": "Prem","id": 1,"dept_id": 3,"with_employee": [{"name": "Eva"},{"name": "Robin"}]},{"name": "Shripadh","id": 2,"dept_id": 4,"with_employee": [{"name": "Bob"},{"name": "Amy"}]},{"name": "Nick","id": 3,"dept_id": 1,"with_employee": [{"name": "Jack"},{"name": "May"}]},{"name": "Cory","id": 4,"dept_id": 1,"with_employee": [{"name": "James"}]}]|Pass||
|4|/|{"detail": "Manager table been dropped"}|{"detail": ""}|Fail|**TODO**|

### Operation: @app.get("/manager/{dept_id}", response_model=list[schemas.Manager], dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|3|[{"name": "Prem","id": 1,"dept_id": 3,"with_employee": [{"name": "Robin"}]}]|pydantic.error_wrappers.ValidationError: 4 validation errors for Manager response -> 0 -> with_employee value is not a valid list (type=type_error.list)|Fail|because the `peewee lazy loading`, add new function in crud `response_manager(manager: schemas.Manager)`|
|2|3|[{"name": "Prem","id": 1,"dept_id": 3,"with_employee": [{"name": "Robin"}]}]|[{"name": "Prem","id": 1,"dept_id": 3,"with_employee": [{"name": "Robin"}]}]|Pass||
|3|20|{"detail": "Manager not found"}|[]|Fail|since function return `None`, change the `models.Manager.DoesNotExist` exception handle to if statement|
|4|20|{"detail": "Department does not exist"}|{"detail": "Department does not exist"}|Pass||
|5|2|404 Not Found, {"detail": <mark>"Manager not found in this department"</mark>}|~~500 Internal Server Error~~, {"detail": ~~""~~}|Fail|**TODO**|


### Operation: @app.delete("/manager/{mng_id}", response_model=list[schemas.Manager], dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|5|[{"name": "Prem","id": 1,"dept_id": 3,"with_employee": [{"name": "Eva"},{"name": "Robin"}]},{"name": "Shripadh","id": 2,"dept_id": 4,"with_employee": [{"name": "Bob"},{"name": "Amy"}]},{"name": "Nick","id": 3,"dept_id": 1,"with_employee": [{"name": "Jack"},{"name": "May"}]},{"name": "Cory","id": 4,"dept_id": 1,"with_employee": [{"name": "James"}]}]|[{"name": "Prem","id": 1,"dept_id": 3,"with_employee": [{"name": "Eva"},{"name": "Robin"}]},{"name": "Shripadh","id": 2,"dept_id": 4,"with_employee": [{"name": "Bob"},{"name": "Amy"}]},{"name": "Nick","id": 3,"dept_id": 1,"with_employee": [{"name": "Jack"},{"name": "May"}]},{"name": "Cory","id": 4,"dept_id": 1,"with_employee": [{"name": "James"}]}]|Pass||
|2|10|{"detail": "Manager does not exist"}|{"detail": "Manager does not exist"}|Pass||
|3|1|{"detail": "Manager table been dropped"}|{"detail": ""}|Fail|**TODO**|

### Operation: @app.delete("/manager/", dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|/|{"Drop table manager": "True"}|{"Drop table manager": "True"}|Pass||




## Table: employee

### Operation: @app.get("/employee/", response_model=list[schemas.Employee], dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|/|[{"name": "James","id": 1,"dept_id": 1,"manager_id": 4},{"name": "Bob","id": 2,"dept_id": 2,"manager_id": 2},{"name": "Eva","id": 3,"dept_id": 3,"manager_id": 1},{"name": "Jack","id": 4,"dept_id": 1,"manager_id": 3},{"name": "Robin","id": 5,"dept_id": 3,"manager_id": 1},{"name": "Amy","id": 6,"dept_id": 2,"manager_id": 2},{"name": "May","id": 7,"dept_id": 1,"manager_id": 3}]|[{"name": "James","id": 1,"dept_id": 1,"manager_id": 4},{"name": "Bob","id": 2,"dept_id": 2,"manager_id": 2},{"name": "Eva","id": 3,"dept_id": 3,"manager_id": 1},{"name": "Jack","id": 4,"dept_id": 1,"manager_id": 3},{"name": "Robin","id": 5,"dept_id": 3,"manager_id": 1},{"name": "Amy","id": 6,"dept_id": 2,"manager_id": 2},{"name": "May","id": 7,"dept_id": 1,"manager_id": 3}]|Pass||


### Operation: @app.get("/employee/{emp_id}", response_model=schemas.Employee, dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|2|{"name": "Bob","id": 2,"dept_id": 2,"manager_id": 2}|{"name": "Bob","id": 2,"dept_id": 2,"manager_id": 2}|Pass||
|2|20|{"detail":"Employee not found"}|{"detail":"Employee not found"}|Pass||
|2|2|{"detail":"Employee table been dropped"}|{"detail": ""}|Fail|**TODO**|


### Operation: @app.delete("/employee/{emp_id}", response_model=list[schemas.Employee], dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|3|[{"name": "James","id": 1,"dept_id": 1,"manager_id": 4},{"name": "Bob","id": 2,"dept_id": 2,"manager_id": 2},{"name": "Jack","id": 4,"dept_id": 1,"manager_id": 3},{"name": "Robin","id": 5,"dept_id": 3,"manager_id": 1},{"name": "Amy","id": 6,"dept_id": 2,"manager_id": 2},{"name": "May","id": 7,"dept_id": 1,"manager_id": 3}]|{"detail": "int() argument must be a string, a bytes-like object or a number, not 'builtin_function_or_method'"}|Fail|change the `crud.delete_employee_by_id` parameter setting|
|2|3|[{"name": "James","id": 1,"dept_id": 1,"manager_id": 4},{"name": "Bob","id": 2,"dept_id": 2,"manager_id": 2},{"name": "Jack","id": 4,"dept_id": 1,"manager_id": 3},{"name": "Robin","id": 5,"dept_id": 3,"manager_id": 1},{"name": "Amy","id": 6,"dept_id": 2,"manager_id": 2},{"name": "May","id": 7,"dept_id": 1,"manager_id": 3}]|[{"name": "James","id": 1,"dept_id": 1,"manager_id": 4},{"name": "Bob","id": 2,"dept_id": 2,"manager_id": 2},{"name": "Jack","id": 4,"dept_id": 1,"manager_id": 3},{"name": "Robin","id": 5,"dept_id": 3,"manager_id": 1},{"name": "Amy","id": 6,"dept_id": 2,"manager_id": 2},{"name": "May","id": 7,"dept_id": 1,"manager_id": 3}]|Pass||
|3|20|{"detail": "Employee does not exist"}|{"detail": "Employee does not exist"}|Pass||
|4|1|{"detail": "Employee table been dropped"}|{ "detail": "relation \"employee\" does not exist\nLINE 1: ....\"salary\", \"t1\".\"dept_id\", \"t1\".\"manager_id\" FROM \"employee\"...\n ^\n"}|Fail|**TODO**|

### Operation: @app.delete("/employee/", dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|/|{"Drop table employee": "True"}|{"Drop table employee": "True"}|Pass||
