import datetime as dt
from typing import List, Dict

import yfinance as yf

from src.domain.models.historical_price import HistoricalPrice
from src.domain.repositories.prices_repository import IPricesRepository


class YahooRepository(IPricesRepository):

    def __init__(self):
        pass

    def get_history(self, symbol: str) -> List[HistoricalPrice]:
        history_df = yf.Ticker(symbol).history(
            start=dt.date(2022, 1, 1),
            end=dt.date(2022, 3, 31)
        )

        history = history_df.reset_index().to_dict('records')
        historical_prices = list()
        for point in history:
            historical_price = HistoricalPrice(date=point['Date'], close=point['Close'], volume=point['Volume'])
            historical_prices.append(historical_price)

        return historical_prices

    def get_info(self, symbol: str) -> Dict:
        pass
