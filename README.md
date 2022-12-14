# Summer23

## `PostgreSQL`
```bash
PostgreSQL
├── PostgreSQL_Python.ipynb
├── PostgreSQL_Python_Advanced.ipynb
└── peewee_module.py
```
- [`PostgreSQL_Python.ipynb`](/PostgreSQL/PostgreSQL_Python.ipynb) final run time: 14/08/2022 14:53(GMT)
	- Link Postgres database to python
	- Use python to do database CRUD (create, read, update, delete)
	- Join query, Group By, Order By, Aggregate Functions
	- Views
- [`PostgreSQL_Python_Advanced.ipynb`](/PostgreSQL/PostgreSQL_Python_Advanced.ipynb) final run time: 20/08/2022 12:51(GMT)
	- WITH clause, CTE (common table expression)
	- Recursion clause
	- Case clause
	- Tree
		- parent_id column vs. ltree module
	- Link PostgreSQL with python ORM and Pandas.
		- Peewee: warp sql statement with class, more secure and so on
		- SQLAlchemy: same as Peewee
		- Pandas: useful when need data visualization
- [`peewee_module.py`](/PostgreSQL/peewee_module.py) : auto generated file by *Peewee -> Working with existing databases* block in *PostgreSQL_Python_Advanced.ipynb*.

## `fastapi-postgresql`
```bash
fastapi-postgresql
├── readme.md
├── sqlalchemy_app
│	├── __init__.py
│	├── crud.py
│	├── database.py
│	├── main.py
│	├── models.py
│	├── schemas.py
│	└── TestPlan.md
├── peewee_app
│	├── __init__.py
│	├── crud.py
│	├── database.py
│	├── main.py
│	├── models.py
│	├── schemas.py
└──	└── TestPlan.md
```
### `sqlalchemy_app`
- [`crud.py`](/fastapi-postgresql/sqlalchemy_app/crud.py): All CRUD functions and make main file more readable.
- [`database.py`](/fastapi-postgresql/sqlalchemy_app/database.py):  Establish a SQLAlchemy db connection by configure.
- [`main.py`](/fastapi-postgresql/sqlalchemy_app/main.py) : Main entrance, all path and corresponding operations.
- [`models.py`](/fastapi-postgresql/sqlalchemy_app/models.py) : Create database models to represent db tables.
- [`schemes.py`](/fastapi-postgresql/sqlalchemy_app/schemes.py) : Pydantic data schemas to handle data validation and data structure, make main file more readable.
- [`TestPlan.md`](/fastapi-postgresql/sqlalchemy_app/TestPlan.md) : Test plan records for `main.py`. Ordered by table, operation.

### `peewee_app`
- [`crud.py`](/fastapi-postgresql/peewee_app/crud.py): All CRUD functions and make main file more readable.
- [`database.py`](/fastapi-postgresql/peewee_app/database.py):  Establish a Peewee db connection configure.
- [`main.py`](/fastapi-postgresql/peewee_app/main.py) : Main entrance, all path and corresponding operations.
- [`models.py`](/fastapi-postgresql/peewee_app/models.py) : Create database models to represent db tables.
- [`schemes.py`](/fastapi-postgresql/peewee_app/schemes.py) : Pydantic data schemas to handle data validation and data structure, make main file more readable.
- [`TestPlan.md`](/fastapi-postgresql/peewee_app/TestPlan.md) : Test plan records for `main.py`. Ordered by table, operation.
