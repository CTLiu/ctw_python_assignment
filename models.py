from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Numeric
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

db_user = os.getenv("MYSQL_USERNAME")
db_password = os.getenv("MYSQL_PASSWORD")
db_host = os.getenv("MYSQL_HOST_LOCAL")
db_port = os.getenv("MYSQL_PORT")

engine = create_engine(
    "mysql+pymysql://{}:{}@{}:{}/finance".format(
        db_user, db_password, db_host, db_port
    ),
)

Base = declarative_base()
Session = sessionmaker(bind=engine)


class FinancialData(Base):
    __tablename__ = "financial_data"
    symbol = Column(String(10), primary_key=True)
    date = Column(Date, primary_key=True)
    open_price = Column(Numeric(10, 2))
    close_price = Column(Numeric(10, 2))
    volume = Column(Integer)


class FinancialDataRepository:
    def __init__(self):
        self.session = Session()

    def upsert(self, prices):
        try:
            for symbol, date, open_price, close_price, volume in prices:
                self.session.merge(
                    FinancialData(
                        symbol=symbol,
                        date=date,
                        open_price=open_price,
                        close_price=close_price,
                        volume=volume,
                    )
                )
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()
            return
