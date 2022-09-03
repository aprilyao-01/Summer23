from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


#Create db URL
pgsql = { 'hostname': 'localhost',
            'database' : 'sqlalchemy_test',
            'username' : 'i52',
            'pwd' : '',
            'port_id' : 5432
        }
SQLALCHEMY_DATABASE_URL = "postgresql://{username}:{pwd}@{hostname}:{port_id}/{database}".format(**pgsql)

#Create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#Create SessionLocal class, this instance will be the actual database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


#Create bass class
Base = declarative_base()