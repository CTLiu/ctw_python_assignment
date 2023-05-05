from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

db_user = os.getenv("MYSQL_USERNAME")
db_password = os.getenv("MYSQL_PASSWORD")
db_host = os.getenv("MYSQL_HOST")

engine = create_engine(
    "mysql+pymysql://{}:{}@{}:3306/finance".format(db_user, db_password, db_host),
    echo=True,
)

Base = declarative_base()
Session = sessionmaker(bind=engine)
