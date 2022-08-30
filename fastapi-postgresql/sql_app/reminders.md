## Run the code
cd to folder `fastapi-postgresql`, then run `uvicorn sql_app.main:app --reload`
    where `sql_app.main` is the file name with src
    `app` is the name of app variable 
    and `— reload` will restart server anytime when make a change to the code and should only be used in development

## Swagger UI and ReDoc
Advantages of FastAPI is it provides interactive API documentations.
- Add `/docs` at hte end of route, can go to the API provided by *Swagger UI*: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    Every routes will be list out and can be used for easily debugging and testing. Click the available route, then click "**Try it out**" and then "**Execute**".
- Add `/redoc` at hte end of route, can go to the API provided by *ReDoc*: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## CRUD and Path Operations
- `Post` -> `C`: to create/add data.
- `Get` -> `R`: to read data.
- `Put` -> `U`: to update data.
- `Delete` -> `D`: to delete data.
