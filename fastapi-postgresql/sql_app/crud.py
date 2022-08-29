# In this file we will have reusable functions to interact with the data in the database.
# CRUD: Create, Read, Update, and Delete
# ...although in this example we are only creating and reading

from sqlalchemy.orm import Session
# allow to declare the type of the db parameters and have better type checks and completion in functions

from . import models, schemas


# Read a single user by ID
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Read a single user by email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Read multiple users
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# Create a SQLAlchemy model instance with data
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"        # example is not secure, the password is not hashed. In a real life application you would need to hash the password and never save them in plaintext.
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)     # add instance object to database session
    db.commit()         # commit the changes to the database (so that they are saved)
    db.refresh(db_user) # refresh instance (so that it contains any new data from the database, like the generated ID)
    return db_user

# Read multiple items
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

# Create a SQLAlchemy model instance with your data.
def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
