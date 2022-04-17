from typing import List

from src.application.dtos.price_dto import PriceDto
from src.domain.repositories.prices_repository import IPricesRepository


class GetHistoricalPricesQuery:

    def __init__(self, prices_repo: IPricesRepository):
        self.prices_repo = prices_repo

    def execute(self, symbol: str) -> List[PriceDto]:
        prices = self.prices_repo.get_history(symbol)
        return [PriceDto(date=x.date, price=x.close) for x in prices]
