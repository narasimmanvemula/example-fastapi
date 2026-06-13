from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings
from urllib.parse import quote_plus

# URL-encode username and password to safely include special characters (eg. '@')
db_username = quote_plus(str(settings.database_username))
db_password = quote_plus(str(settings.database_password))

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{db_username}:{db_password}"
    f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='Rmkec@123',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database  connection was succesfull!")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error: ", error)    
#         time.sleep(2)
