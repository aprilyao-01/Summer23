from peewee import *

database = PostgresqlDatabase('mydb')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Department(BaseModel):
    dept_id = CharField(null=True)
    dept_name = CharField(null=True)

    class Meta:
        table_name = 'department'
        primary_key = False

class Employee(BaseModel):
    dept_id = CharField(null=True)
    emp_id = CharField(primary_key=True)
    manager_id = CharField(null=True)
    name = CharField()
    salary = IntegerField(null=True)
    sex = UnknownField(null=True)  # USER-DEFINED

    class Meta:
        table_name = 'employee'

class Family(BaseModel):
    age = IntegerField(null=True)
    member_id = CharField(null=True)
    name = CharField(null=True)
    parent_id = CharField(null=True)

    class Meta:
        table_name = 'family'
        primary_key = False

class Manager(BaseModel):
    dept_id = CharField(null=True)
    manager_id = CharField(null=True)
    manager_name = CharField(null=True)

    class Meta:
        table_name = 'manager'
        primary_key = False

class Projects(BaseModel):
    project_id = CharField(null=True)
    project_name = CharField(null=True)
    team_member_id = CharField(null=True)

    class Meta:
        table_name = 'projects'
        primary_key = False

class Tree(BaseModel):
    name = TextField(null=True)
    parent_path = UnknownField(index=True, null=True)  # USER-DEFINED

    class Meta:
        table_name = 'tree'

