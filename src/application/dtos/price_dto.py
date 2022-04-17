import datetime as dt
from decimal import Decimal

from pydantic import BaseModel


class PriceDto(BaseModel):
    date: dt.date
    price: str
