from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from  psycopg2.extras  import RealDictCursor
import psycopg2
import time


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:elvispro1993@localhost/fastapi'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
Base = declarative_base()

 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
  
##  HOW TO CONNECT TO THE POSTGRES DATA BASE USING RAW SQL COMMANDS      
# while True:    
#     try:
#         conn =psycopg2.connect(host='localhost',database='fastapi',user='postgres',
#                             password='elvispro1993',cursor_factory=RealDictCursor)
#         cursor =conn.cursor()
#         print("database connection was successfully")
#         break
#     except Exception as error:
#         print("Connection to the database failed")
#         print("Error :",error)
#         time.sleep(3)