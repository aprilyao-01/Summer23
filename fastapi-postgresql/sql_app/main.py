from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

#Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:            #make sure the db session is always closed after the request. Even if there was an exception while processing the request.
        db.close()

# fake db used for test
testDatabase = {
    1:{'User': 'U1'},
    2:{'User': 'U2'},
    3:{'User': 'U3'},
}

#TODO: display all records in home page
@app.get("/")
def get_all():
    return testDatabase

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

#test get by id
@app.get("/test/{id}")
def test_get_by_id(id: int):
    return testDatabase[id]


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items



#option1
@app.post("/test/")
def test_add_record(newUser: str):
    index = len(testDatabase.keys()) + 1      # get the next index
    testDatabase[index] = {"User": newUser}      # add new record to the test db
    return testDatabase






@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):       # when using the dependency in a path operation function, declare it with the type Session that imported directly from SQLAlchemy
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)



