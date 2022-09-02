from enum import unique
import imp
from textwrap import indent
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


# Relationships: 
# A department employs many employees. 
# A manager supervises many employees. 
# One department could have different managers.

#Create SQLALchemy models from the Base class
class Employee(Base):       # models
    __tablename__ = "employee"     #table name

    #attributes -> a column in table
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, nullable = False)
    salary = Column(Integer)
    dept_id = Column(Integer, ForeignKey("manager.id", onupdate="CASCADE", ondelete="SET NULL"))
    manager_id = Column(Integer, ForeignKey("department.id", onupdate="CASCADE", ondelete="SET NULL"))

    #relationship -> contain the values from other tables related to this one
    # employee-manager: M-O, employee-department: M-O
    with_manager = relationship("Manager", backref= "with_employee")
    belong_department = relationship("Department", backref= "has_employees")
    


class Manager(Base):       #models
    __tablename__ = "manager"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable = False)
    dept_id = Column(Integer, ForeignKey("department.id", onupdate="CASCADE", ondelete="SET NULL"))
  
    # department-manager: O-M
    belong_department = relationship("Department", backref="has_managers")
    # with_employee = relationship("Employee", back_populates="with_manager")


class Department(Base):       #models
    __tablename__ = "department"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable = False, unique = True)
   
    # has_managers = relationship("User", back_populates="items")
    # has_employees = relationship("User", back_populates="belong_department")

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