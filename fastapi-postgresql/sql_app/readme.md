# README part
## Run the code
**Option 1**:
cd to folder `fastapi-postgresql`, then run `uvicorn sql_app.main:app --reload`
**Option 2**:
cd to folder `sql_app`, change all `from . import xxx` to `import xxx`, then run `uvicorn main:app --reload`
<br>
Where `main` is the file name(`sql_app.`with src), `app` is the name of app variable and `— reload` will restart server anytime when make a change to the code and should only be used in development.

## Swagger UI and ReDoc
Advantages of FastAPI is it provides interactive API documentations.
- Add `/docs` at hte end of route, can go to the API provided by *Swagger UI*: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)<br>
    Every routes will be list out and can be used for easily debugging and testing. Click the available route, then click "**Try it out**" and then "**Execute**".
- Add `/redoc` at hte end of route, can go to the API provided by *ReDoc*: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
<br> 
---

# Notes part
## CRUD and Path Operations
- `Post` -> `C`: to create/add data.
- `Get` -> `R`: to read data.
- `Put` -> `U`: to update data.
- `Delete` -> `D`: to delete data.

## Relationship Patterns in SQLAlchemy
|   |O - M|M - O|O - O|M - M|
|---|-----|-----|-----|-----|
|**E/R Diagram**|![O-M E/R](/Users/i52/Downloads/myGit/Summer23/img/O-M.png)|![M-O E/R](/Users/i52/Downloads/myGit/Summer23/img/M-O.png)|![O-O E/R](/Users/i52/Downloads/myGit/Summer23/img/O-O.png)|![M-M E/R](/Users/i52/Downloads/myGit/Summer23/img/M-M.png)|
|**Describe**|Each department employs a number of lecturers|Students enrol in a particular course|One person has a nose|Students take several modules|
|**ForeignKey() on table**|Many / lecturer|Many / student|One?, `unique`?|Third association table / enrolment|
|**relationship() on table**|One / department|Many / student|relationship() and `back_populates` on both, `uselist=False` on one side **OR** `relationship("the other", backref=backref("self", uselist=False))` on only department or lecturer|`relationship.secondary` on one of the two tables|
|**Bidirectional**|relationship() with `back_populates` on both **OR** `backref` on only lecturer or department|relationship() with `back_populates` on both **OR** `backref` on only student or course|(Essentially)|relationship() with `back_populates` and `secondary` on both **OR** `backref` on only student or module ( the same `secondary`argument will be automatically used ) |
|**Notes**|||Usually merge the two entities together to become a single entity has all attributes of the oud ones. If there aren't any contradictions, the O-O might be a sign of an unconsidered decision.|Usually split a M - M relationship into two O-M relationships|

- `back_populates`: Informs each relationship about the other, so that they are kept in sync. MUST explicitly create the relationships on **both** A and B classes.
- `backref`: Shortcut for configuring both parent.children and child.parent relationships at **one place only** on the A or the B class (not both).
- `uselist`: A boolean value auto determined by relationship() according to relationship types. A list for O-M and M-M, a scalar for M-O. Set to **False** in bi-directional O-O.
- `secondary`: For a many-to-many relationship, specifies the intermediary table, and is typically an instance of Table.


### others
in post option 3, using docs, you will see `"string"` in the initial request body, and you have to specify the data structure in request body as you wish, like `{"user" : "test user in body"}`. Notice that when specified, use **" " double quotes** and not single quotes to ensure the string is able to be parsed on the receiving end.

`sqlalchemy.orm.Query.all()`:Return the results represented by this Query as a list.

`join()` will attempt to create a JOIN along the **natural foreign key relationship** between two entities or you can explicitly specify ON clause with `session.query(A).join(B, A.id==B.a_id)`. Add `isouter = True` to join query to implement left join.

`database.py`: establish a db connection configure.
`models.py` : create database models to represent db tables.
`crud.py`: all CRUD functions,  to make main file more readable.
