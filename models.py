from sqlalchemy import Column, Integer, String, Date, Numeric


class FinancialData:
    __tablename__ = "financial_data"
    symbol = Column(String(10), primary_key=True)
    date = Column(Date, primary_key=True)
    open_price = Column(Numeric(10, 2))
    close_price = Column(Numeric(10, 2))
    volume = Column(Numeric)
