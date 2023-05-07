import math
from .repositories import FinancialDataRepository

finacial_data_repository = FinancialDataRepository()


def get_financial_data(start_date, end_date, symbol, limit, page):
    result = {"data": [], "pagination": {}, "info": {"error": ""}}

    try:
        symbol_prices = (
            finacial_data_repository.get_symbol_prices_by_date_range_and_pagination(
                start_date, end_date, symbol, limit, page
            )
        )
        total_count = finacial_data_repository.get_count_of_symbol_prices_by_date_range(
            start_date, end_date, symbol
        )

        result["pagination"] = create_pagination_object(total_count, page, limit)
        result["data"] = symbol_prices

    # Any kinds of error will be added to the result and responded
    except Exception as error:
        result["info"]["error"] = str(error)

    return result


def calculate_statistics_data(start_date, end_date, symbol):
    result = {"data": {}, "info": {"error": ""}}

    try:
        symbol_prices = (
            finacial_data_repository.get_symbol_prices_by_date_range_and_pagination(
                start_date, end_date, symbol
            )
        )
        count = 0
        open_price_sum = 0
        close_price_sum = 0
        volume_sum = 0

        # one iteration through the data would do the job
        for data in symbol_prices:
            count += 1
            open_price_sum += data.open_price
            close_price_sum += data.close_price
            volume_sum += data.volume

        result["data"]["start_date"] = start_date
        result["data"]["end_date"] = end_date
        result["data"]["symbol"] = symbol
        result["data"]["average_daily_open_price"] = round(open_price_sum / count, 2)
        result["data"]["average_daily_close_price"] = round(close_price_sum / count, 2)
        result["data"]["average_daily_volume"] = round(volume_sum / count, 2)

    # Any kinds of error will be added to the result and responded
    except Exception as error:
        result["info"]["error"] = str(error)

    return result


def create_pagination_object(total, page, limit):
    pagination_obj = {}
    pagination_obj["count"] = total
    pagination_obj["page"] = page
    pagination_obj["pages"] = math.ceil(total / limit)
    pagination_obj["limit"] = limit

    return pagination_obj
