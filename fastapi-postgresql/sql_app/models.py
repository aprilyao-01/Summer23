from enum import unique
import imp
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


#Create SQLALchemy models from the Base class
class User(Base):       # models
    __tablename__ = "users"     #table name

    #attributes -> a column in table
    id = Column(Integer, primary_key = True, index = True)
    email = Column(String, unique = True, index = True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default = True)

    #relationship -> contain the values from other tables related to this one
    items = relationship("Item", back_populates = "owner")

class Item(Base):       #models
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")