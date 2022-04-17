import datetime as dt
from decimal import Decimal

from src.domain.shared.value_object import ValueObject


class HistoricalPrice(ValueObject):
    date: dt.date
    close: Decimal
    volume: Decimal
