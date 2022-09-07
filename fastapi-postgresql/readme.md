# README part
The two folders implements the same db and operations except using different ORM. 
## [SQLAlchemy_sql App](/fastapi-postgresql/sqlalchemy_app)
### Run the code:
- Option 1:
    cd to folder `fastapi-postgresql`, then run `uvicorn sqlalchemy_app.main:app --reload`. 
- Option 2:
    cd to folder `sqlalchemy_app`, replace all `from . import xxx` with `import xxx`, then run `uvicorn main:app --reload`.

Where `main` is the file name(`sqlalchemy_app.`with src), `app` is the name of app variable and `— reload` will restart server anytime when make a change to the code and should only be used in development.

### Test Records
The [`TestPlan`](/fastapi-postgresql/sqlalchemy_app/TestPlan.md) file records test plans for [`sqlalchemy_app/main.py`](/fastapi-postgresql/sqlalchemy_app/main.py). Ordered by table, operation.

## [PeeWee_sql App](/fastapi-postgresql/peewee_app)
**Require: Python 3.7 or above to safely use Peewee with FastAPI.**
### Run the code
- Option 1:
    cd to folder `fastapi-postgresql`, then run `uvicorn peewee_app.main:app --reload`.
- Option 2:
    cd to folder `peewee_app`, replace all `from . import xxx` with `import xxx`, then run `uvicorn main:app --reload` .

Where `main` is the file name(`peewee_app. `with src), `app` is the name of app variable and `— reload` will restart server anytime when make a change to the code and should only be used in development.

### Test Records
The [`TestPlan`](/fastapi-postgresql/peewee_app/TestPlan.md) file records test plans for [`peewee_app/main.py`](/fastapi-postgresql/peewee_app/main.py). Ordered by table, operation.


## Swagger UI and ReDoc
Advantages of FastAPI is it provides interactive API documentations.
- Add `/docs` at hte end of route, can go to the API provided by *Swagger UI*: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)<br>
    Every routes will be list out and can be used for easily debugging and testing. Click the available route, then click "**Try it out**" and then "**Execute**".
- Add `/redoc` at hte end of route, can go to the API provided by *ReDoc*: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

# Notes part
## CRUD and Path Operations
- `Post` -> `C`: to create/add data.
- `Get` -> `R`: to read data.
- `Put` -> `U`: to update data.
- `Delete` -> `D`: to delete data.

## Response Model
A parameter of the "decorator" method (get, post, etc) not of *path operation function*. It receives **a** Pydantic model or a **list** of Pydantic models, like `List[Item]`.

FastAPI will use this `response_model` to:
- Convert the output data to its type declaration.
- Validate the data.
- Add a JSON Schema for the response, in the OpenAPI path operation.
- Will be used by the automatic documentation systems.
- **Most importantly**: will limit the output data to that of the model. Kinda like `SELECT * FROM myview` no need to specify columns.

## Relationship Patterns in SQLAlchemy
|   |O - M|M - O|O - O|M - M|
|---|-----|-----|-----|-----|
|**E/R Diagram**|![O-M E/R](/img/O-M.png)|![M-O E/R](/img/M-O.png)|![O-O E/R](/img/O-O.png)|![M-M E/R](/img/M-M.png)|
|**Describe**|Each department employs a number of lecturers|Students enrol in a particular course|One person has a nose|Students take several modules|
|**ForeignKey() on table**|Many / lecturer|Many / student|One?, `unique`?|Third association table / enrolment|
|**relationship() on table**|One / department|Many / student|relationship() and `back_populates` on both, `uselist=False` on one side **OR** `relationship("the other", backref=backref("self", uselist=False))` on only department or lecturer|`relationship.secondary` on one of the two tables|
|**Bidirectional**|relationship() with `back_populates` on both **OR** `backref` on only lecturer or department|relationship() with `back_populates` on both **OR** `backref` on only student or course|(Essentially)|relationship() with `back_populates` and `secondary` on both **OR** `backref` on only student or module ( the same `secondary`argument will be automatically used ) |
|**Notes**|||Usually merge the two entities together to become a single entity has all attributes of the oud ones. If there aren't any contradictions, the O-O might be a sign of an unconsidered decision.|Usually split a M - M relationship into two O-M relationships|

- `back_populates`: Informs each relationship about the other, so that they are kept in sync. MUST explicitly create the relationships on **both** A and B classes.
- `backref`: Shortcut for configuring both parent.children and child.parent relationships at **one place only** on the A or the B class (not both).
- `uselist`: A boolean value auto determined by relationship() according to relationship types. A list for O-M and M-M, a scalar for M-O. Set to **False** in bi-directional O-O.
- `secondary`: For a many-to-many relationship, specifies the intermediary table, and is typically an instance of Table.

## Peewee and FastAPI
###  Make Peewee async-compatible
The main issue with Peewee and FastAPI is that Peewee relies heavily on Python's `threading.local`(to have a "magic" variable that has a different value for each thread)), and it doesn't have a direct way to override it or let you handle connections/sessions directly (as is done in the SQLAlchemy).And `threading.local` is not compatible with the new async features of modern Python.

To make Peewee async-compatible, create [`PeeWeeConnectionSate`](/fastapi-postgresql/peewee_app/db.py), which is override the internal parts of Peewee that use `threading.local` and replace them with Python 3.7+ `contextvars`, with the corresponding updates. Make sure overwrite `db._state` **after** creating `db`.

This will just make Peewee behave correctly when used with FastAPI. Not randomly opening or closing connections that are being used, creating errors, etc. But it doesn't give Peewee async super-powers. You should still use normal `def` functions and not `async def`.

The changes is needed for any Peewee db, including `SqliteDatabase`, `MySQLSqliteDatabase`, etc.

### Create a `PeeweeGetterDict` for the Pydantic schemas
When you access a relationship in a Peewee object, like in `some_department.employees`, Peewee doesn't provide a `list` of Item. Instead, tt provides a special custom object of class `ModelSelect`.
It's possible to create a list of its items with `list(some_user.items)`. But the object itself is not a `list`. And it's also not an actual Python generator. Because of this, Pydantic doesn't know by default how to convert it to a `list` of Pydantic schemas.
But recent versions of Pydantic allow providing a custom class that inherits from `pydantic.utils.GetterDict`, to provide the functionality used when using the `orm_mode = True` to retrieve the values for ORM model attributes. So a custom [`PeeweeGetterDict` class](/fastapi-postgresql/peewee_app/schemas.py) is used in all Pydantic `orm_mode` with the configuration variable `getter_dict = PeeweeGetterDict`.

### Context variable sub-dependency
When create a dependency that will connect the db right at the beginning of a request and disconnect it at the end, the `yield` is empty because we are actually not using the db object directly. It is connecting to the db and storing the connection data in an internal variable that is independent for each request (using the `contextvars` tricks from above). Because of that, add it to the *path operation decorator* in the `dependencies` parameter instead of path operation function.

Create another `async` dependency `reset_db_state()` that is used as a sub-dependency in` get_db()`. It will make sure the value for the context variable (with just a default `dict`) that will be used as the db state for the whole request for all the `contextvars` parts to work. (i.e. the dependency `get_db()` will store in it the db state, connection, transactions, etc). For the next request, as we will reset that context variable again in the `async` dependency `reset_db_state()` and then create a new connection in the `get_db()` dependency, that new request will have its own database state (connection, transactions, etc).

### Peewee with async
The code implements does not include simulates long processing request in multiple threads without `contextvars`. See official document - [SQL Databases with Peewee](https://fastapi.tiangolo.com/advanced/sql-databases-peewee/#testing-peewee-with-async) for more.


## others
### sqlalchemy
- in post option 3, using docs, you will see `"string"` in the initial request body, and you have to specify the data structure in request body as you wish, like `{"user" : "test user in body"}`. Notice that when specified, use **" " double quotes** and not single quotes to ensure the string is able to be parsed on the receiving end.
<br>

- `sqlalchemy.orm.Query.all()`:Return the results represented by this Query as a list.
<br>

- `join()` will attempt to create a JOIN along the **natural foreign key relationship** between two entities or you can explicitly specify ON clause with `session.query(A).join(B, A.id==B.a_id)`. Add `isouter = True` to join query to implement left join.
<br>

- `limit()` and `offset()` apply LIMIT and OFFSET to the query and return the newly resulting Query, used when want to retrieve only a few records from query result. LIMIT will retrieve only the number of records specified after the LIMIT keyword, unless the query itself returns fewer records than the number specified by LIMIT. OFFSET is used to skip the number of records from the results.
<br>

### peewee
- in select, if a record does not exist, `.get()` will raise exception `<model_name>DoesNotExist`, but `.first()` will return `None`.
<br>

- for select return not match `response_model`
    ```python
    obj=Department.filter(Department.name == "IT").first()
    print(type(obj))
    print(obj.id, obj.name, obj.has_managers, obj.has_employees)
    if obj.has_managers is None:
        print("true")
    else:
        print("false")

    # Output:
    <Model: Department>
    5 IT SELECT "t1"."id", "t1"."name", "t1"."dept_id" FROM "manager" AS "t1" WHERE ("t1"."dept_id" = 5) SELECT "t1"."id", "t1"."name", "t1"."salary", "t1"."dept_id", "t1"."manager_id" FROM "employee" AS "t1" WHERE ("t1"."dept_id" = 5)
    false
    ```
this is because peewee use **`lazy loading`**, two options to fix this:

1. when specify `ForeignKeyField`, set parameter`lazy_load = False`, see [`ForeignKeyField` document](https://docs.peewee-orm.com/en/latest/peewee/api.html#ForeignKeyField) for example. Need to notice that, however, if we eagerly load the related object, then the foreign key will behave like usual, see [example code](http://docs.peewee-orm.com/en/latest/peewee/models.html?highlight=table%20generation#foreignkeyfield).
2. when querying, put a `list` around the attribute you want, see [`crud.py`](/fastapi-postgresql/peewee_app/crud.py)
