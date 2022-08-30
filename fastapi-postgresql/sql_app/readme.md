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
|   |O - O|O - M|M - O|M - M|
|:--|---|---|---|---|
|**ForeignKey() on**|a|child|c|d|
|**relationship() on**|a|parent|c|d|
|**Bidirectional**|a|relationship() and `back_populates` on both|c|d|
||a|OR relationship() and `backref` on only child or parent|c|d|

- `back_populates`: Informs each relationship about the other, so that they are kept in sync. MUST explicitly create the relationships on **both** parent and child classes.
- `backref`: Shortcut for configuring both parent.children and child.parent relationships at **one place only** on the parent or the child class (not both).


### others
in post option 3, using docs, you will see `"string"` in the initial request body, and you have to specify the data structure in request body as you wish, like `{"user" : "test user in body"}`. Notice that when specified, use **" " double quotes** and not single quotes to ensure the string is able to be parsed on the receiving end.


`database.py` file: establish a db connection configure.
`models.py` : create database models to represent db tables.
