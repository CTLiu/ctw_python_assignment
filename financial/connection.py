from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

db_user = os.getenv("MYSQL_USERNAME")
db_password = os.getenv("MYSQL_PASSWORD")

engine = create_engine(
    "mysql+pymysql://{}:{}@localhost:3306/finance".format(db_user, db_password)
)

with engine.connect() as conn:
    conn.execute(text("CREATE DATABASE IF NOT EXISTS finance"))

Base = declarative_base()


Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
