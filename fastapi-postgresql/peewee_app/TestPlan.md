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
|4|[{"name": "IT"}, {"name": "HR"}, {"name": "Finance"}, {"name": "Admin"}]|[{ "name": "IT","id": 1,"has_managers": [],"has_employees": []},{"name": "HR","id": 2,"has_managers": [],"has_employees": []},{"name": "Finance","id": 3,"has_managers": [],"has_employees": []},{"name": "Admin","id": 4,"has_managers": [],"has_employees": []}]|pydantic.error_wrappers.ValidationError|Fail|**TODO: fix conflict**|



### Operation: @app.get("/department/", response_model=list[schemas.Department], dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|/|[{"name": "IT","id": 1,"has_managers": [],"has_employees": []}]|pydantic.error_wrappers.ValidationError: 2 validation errors for Department response -> has_managers value is not a valid list (type=type_error.list) response -> has_employees value is not a valid list (type=type_error.list)|Fail|`list(models.Department.select().offset(skip).limit(limit))` return list `[<Department: 1>]`, which has {"id":1,"name": IT,~~"has_managers":"SELECT "t1"."id", "t1"."name", "t1"."dept_id" FROM "manager" AS "t1" WHERE ("t1"."dept_id" = 1)", "has_employees": "SELECT "t1"."id", "t1"."name", "t1"."salary", "t1"."dept_id", "t1"."manager_id" FROM "employee" AS "t1" WHERE ("t1"."dept_id" = 1)"~~}. Conflict with `response_model`. **TODO: fix conflict**|

### Operation: @app.get("/department/{dept_id}", response_model=schemas.Department, dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|1|[{"name": "IT","id": 1,"has_managers": [],"has_employees": []}]| peewee_app.models.DepartmentDoesNotExist: <Model: Department> instance matching query does not exist: SQL: SELECT "t1"."id", "t1"."name" FROM "department" AS "t1" WHERE ("t1"."id" = %s) LIMIT %s OFFSET %s Params: [1, 1, 0]|Fail| replace all `department is None` to `except module.Department.DoesNotExist:`|
|1|1|{ "detail": "Department not found"}| { "detail": "Department not found"}|Pass||

### Operation: @app.delete("/department/{dept_id}", response_model=list[schemas.Department], dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|1|[ ]|[ ]|Pass||

### Operation: @app.delete("/department/", dependencies=[Depends(get_db)])
|Test|Inputs|Expected Outcome|Test Outcome|Result|Changes|
|:--:|------|----------------|------------|------|-------|
|1|/|{"Drop table department": "True"}|{"Drop table department": "True"}|Pass||
