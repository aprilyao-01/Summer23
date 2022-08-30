from enum import unique
import imp
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

# TODO: change the models to employee and manager
#Create SQLALchemy models from the Base class
class Employee(Base):       # models
    __tablename__ = "employee"     #table name

    #attributes -> a column in table
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, nullable = False)
    salary = Column(Integer)
    dept_id = Column(Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="SET NULL"))
    manager_id = Column(Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="SET NULL"))

    #relationship -> contain the values from other tables related to this one
    # TODO: rewrite the relationships
    belong_department = relationship("Item", back_populates = "owner")
    with_manager = relationship("Item", back_populates = "owner")


class Manager(Base):       #models
    __tablename__ = "manager"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable = False)
    dept_id = Column(Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="SET NULL"))
  
    belong_department = relationship("User", back_populates="items")
    with_employee = relationship("User", back_populates="items")


class Department(Base):       #models
    __tablename__ = "department"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable = False)
   
    has_manager = relationship("User", back_populates="items")
    has_employee = relationship("User", back_populates="items")