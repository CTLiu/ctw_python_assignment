from fastapi import FastAPI
from .validations import GetStatisticsValidator, GetFinancialDataValidator
from pydantic import ValidationError
from .services import get_financial_data, calculate_statistics_data
from datetime import date

app = FastAPI()


@app.get("/api/financial_data")
def financial_data(
    start_date: str = None,
    end_date: str = None,
    symbol: str = "IBM",
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


@app.get("/api/statistics")
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
