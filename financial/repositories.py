from .connection import Base, engine
from sqlalchemy import Column, Integer, String, Date, Numeric
from sqlalchemy.orm import Session


class FinancialData(Base):
    __tablename__ = "financial_data"
    symbol = Column(String(10), primary_key=True)
    date = Column(Date, primary_key=True)
    open_price = Column(Numeric(10, 2))
    close_price = Column(Numeric(10, 2))
    volume = Column(Integer)


Base.metadata.create_all(bind=engine)


class FinancialDataRepository:
    def get_symbol_prices_by_date_range_and_pagination(
        self, start_date, end_date, symbol, limit=None, page=None
    ):
        with Session(engine) as session:
            query_obj = session.query(FinancialData)

            if symbol:
                query_obj.filter(FinancialData.symbol == symbol)
            if start_date:
                query_obj = query_obj.filter(FinancialData.date >= start_date)
            if end_date:
                query_obj = query_obj.filter(FinancialData.date <= end_date)
            if page and limit:
                offset = (page - 1) * limit
                query_obj = query_obj.offset(offset).limit(limit)
            financial_data = query_obj.all()

            return financial_data

    def get_count_of_symbol_prices_by_date_range_and_pagination(
        self, start_date, end_date, symbol, limit, page
    ):
        with Session(engine) as session:
            query_obj = session.query(FinancialData)

            if symbol:
                query_obj.filter(FinancialData.symbol == symbol)
            if start_date:
                query_obj = query_obj.filter(FinancialData.date >= start_date)
            if end_date:
                query_obj = query_obj.filter(FinancialData.date <= end_date)
            count = query_obj.count()

            return count
