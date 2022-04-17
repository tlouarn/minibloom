import abc
from typing import List

from src.domain.models.historical_price import HistoricalPrice


class IPricesRepository(abc.ABC):

    def get_history(self, symbol: str) -> List[HistoricalPrice]:
        raise NotImplementedError
