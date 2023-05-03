from pydantic import BaseModel, validator
from datetime import date


class GetStatisticsValidator(BaseModel):
    end_date: date = None
    start_date: date = None
    symbol: str = ""

    @validator("start_date")
    def check_start_date(cls, value, values):
        if value is None:
            raise ValueError("start_date is required")
        if "end_date" in values and value >= values["end_date"]:
            raise ValueError("start_date must be before end_date")
        return value

    @validator("end_date")
    def validate_end_date(cls, value):
        if value is None:
            raise ValueError("end_date is required")
        if value >= date.today():
            raise ValueError("End date must be before today")
        return value

    @validator("symbol")
    def validate_symbol(cls, value):
        if value not in ["AAPL", "IBM"]:
            raise ValueError('symbol must be one of "AAPL" or "IBM"')
        return value


class GetFinancialDataValidator(BaseModel):
    end_date: date = None
    start_date: date = None
    symbol: str = None
    limit: int = 5
    page: int = 1

    @validator("start_date", pre=True)
    def parse_start_date(cls, value):
        if value is not None and not isinstance(value, date):
            return date.fromisoformat(value)
        return value

    @validator("end_date", pre=True)
    def parse_end_date(cls, value):
        if value is not None and not isinstance(value, date):
            return date.fromisoformat(value)
        return value

    @validator("start_date")
    def check_start_date(cls, value, values):
        if (
            value
            and "end_date" in values
            and isinstance(values["end_date"], date)
            and value >= values["end_date"]
        ):
            raise ValueError("start_date must be before end_date")
        return value

    @validator("end_date")
    def validate_end_date(cls, value):
        if value and value >= date.today():
            raise ValueError("End date must be before today")
        return value

    @validator("symbol")
    def validate_symbol(cls, value):
        if value and value not in ["AAPL", "IBM"]:
            raise ValueError('symbol must be one of "AAPL" or "IBM"')
        return value

    @validator("limit")
    def validate_limit(cls, value):
        if value < 1:
            raise ValueError("limit must be at least 1")
        return value

    @validator("page")
    def validate_page(cls, value):
        if value < 1:
            raise ValueError("page must be at least 1")
        return value
