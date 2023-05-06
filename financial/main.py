from fastapi import FastAPI
from .validations import GetStatisticsValidator, GetFinancialDataValidator
from pydantic import ValidationError
from .services import get_financial_data, calculate_statistics_data
from datetime import date

description = """
## Project Descriptions
The service is a prototype for the CTW take home assignment.
It is implemented by python 3 and integrated with MYSQL db.

## APIs
### Get prices of symbols
- Can query the prices by symbols.
- Symbols may be one of **AAPL** or **IBM**.
- Date range for **start_date** and **end_date** has to be a date before today, and **start_date** has to be before **end_date**.
- Date format should be YYYY-MM-DD, 2023-01-01
- Pagination is also implemented.

### Get statistics by symbol
- Can query the prices by symbols.
- Symbols may be one of **AAPL** or **IBM**.
- Date range for **start_date** and **end_date** has to be a date before today, and **start_date** has to be before **end_date**.
- Date format should be YYYY-MM-DD, 2023-01-01
"""

tags_metadata = [
    {
        "name": "Get prices of symbols",
        "description": "",
    },
    {
        "name": "Get statistics by symbol",
        "description": "",
    },
]

app = FastAPI(
    title="CTW Take Home Assignment",
    description=description,
    version="0.0.1",
    openapi_tags=tags_metadata,
)


@app.get("/api/financial_data", tags=["Get prices of symbols"])
def financial_data(
    start_date: str = None,
    end_date: str = None,
    symbol: str = None,
    limit: int = 5,
    page: int = 1,
):
    try:
        query_params = GetFinancialDataValidator(
            end_date=end_date,
            start_date=start_date,
            symbol=symbol,
            limit=limit,
            page=page,
        )

        return get_financial_data(
            query_params.start_date,
            query_params.end_date,
            query_params.symbol,
            query_params.limit,
            query_params.page,
        )
    except ValidationError as e:
        return parse_error_response(e)


@app.get("/api/statistics", tags=["Get statistics by symbol"])
def statistics(end_date: date = None, start_date: date = None, symbol=""):
    try:
        query_params = GetStatisticsValidator(
            end_date=end_date, start_date=start_date, symbol=symbol
        )

        return calculate_statistics_data(
            query_params.start_date, query_params.end_date, query_params.symbol
        )
    except ValidationError as e:
        return parse_error_response(e)


def parse_error_response(e):
    result = {"data": [], "pagination": {}, "info": {"error": ""}}
    error_messages = []
    for error in e.errors():
        error_messages.append(error["msg"])
    result["info"]["error"] = error_messages
    return result
