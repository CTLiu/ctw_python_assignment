from datetime import datetime, timedelta
from dotenv import load_dotenv

from models import FinancialDataRepository
import requests
import os

load_dotenv()

api_domain = os.getenv("ALPHAVANTAGE_DOMAIN")
apikey = os.getenv("ALPHAVANTAGE_APIKEY")
symbol = ["IBM", "AAPL"]
financial_data_repository = FinancialDataRepository()

for stockname in symbol:
    url = "{}/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}".format(
        api_domain, stockname, apikey
    )
    r = requests.get(url)
    data = r.json()

    # start date will be the date of 14 days ago
    start = (datetime.now() - timedelta(14)).strftime("%Y-%m-%d")
    end = datetime.today().strftime("%Y-%m-%d")

    try:
        prices = list(data.values())[1].items()
    except IndexError:
        print(data.values())
        break
    prices_to_save = []

    for key, value in prices:
        # compares key with the start dat, if the start date is starting to be later than the current date
        # this iteration should be terminated
        if key < start:
            break
        else:
            day_stock = list(value.values())
            # daystock[0] is the open price
            # daystock[3] is the close price
            # daystock[5] is the volume
            prices_to_save.append(
                (stockname, key, day_stock[0], day_stock[3], day_stock[5])
            )
            print(
                "Got financial data: {} {} {} {} {}".format(
                    stockname, key, day_stock[0], day_stock[3], day_stock[5]
                )
            )

    financial_data_repository.upsert(prices_to_save)
