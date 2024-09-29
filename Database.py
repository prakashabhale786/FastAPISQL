from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base

SQLALCHEMY_DB_URL="sqlite:///./sql_app.db"   

# if we connect mysql db_url
# SQLALCHEMY_DB_URL="mysql://root:Password@localhost/first_db"

engine=create_engine(SQLALCHEMY_DB_URL,connect_args={"check_same_thread":False})  
SessionLocal=sessionmaker(autocommit=False,bind=engine)

Base=declarative_base()
