from peewee import *

from .database import db

# Relationships: 
# A department employs many employees. 
# A manager supervises many employees. 
# One department could have different managers.

#Create Peewee models from the peewee.Model class
class Department(Model):        # auto chose the name of the tables based on the class names.
    id = AutoField()    # id will be auto-incrementing PK. 
    # If do not specify a primary key, Peewee will automatically create an auto-incrementing primary key named “id”.

    name = CharField(unique=True)

    class Meta:
        database = db # This model uses the "peewee_test.db" database.


class Manager(Model): 
    name = CharField()
    dept= ForeignKeyField(Department, backref='has_managers', null=True, 
            on_update='CASCADE', on_delete='SET NULL', lazy_load=False)

    class Meta:
        database = db # This model uses the "peewee_test.db" database.


class Employee(Model):
    name = CharField()
    salary = IntegerField(null=True, constraints=[Check('salary >= 0')])
    dept= ForeignKeyField(Department, backref= 'has_employees', null=True, 
            on_update='CASCADE', on_delete='SET NULL', lazy_load=False)
            
    manager= ForeignKeyField(Manager, backref= 'with_employee', null=True, 
            on_update='CASCADE', on_delete='SET NULL',lazy_load=False )

    class Meta:
        database = db # This model uses the "peewee_test.db" database.
