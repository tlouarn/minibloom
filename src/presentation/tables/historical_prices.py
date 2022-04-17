import datetime as dt
from typing import List

from dateutil.rrule import DAILY, rrule, MO, TU, WE, TH, FR
from rich.style import Style
from rich.table import Table

from src.application.dtos.price_dto import PriceDto


class HistoricalPricesTableFormatter:

    def __init__(self, prices: List[PriceDto]) -> None:
        self.prices = prices

    def format(self) -> Table:
        """
        A formatted table is a 45-day window made of 9 full weeks around the list of prices.
        """

        if len(self.prices) == 0:
            return Table()

        last_day = self.prices[-1].date

        end_date = last_day + dt.timedelta(days=4 - last_day.weekday())
        start_date = end_date - dt.timedelta(days=60)
        calendar_range = list(rrule(DAILY, dtstart=start_date, until=end_date, byweekday=(MO, TU, WE, TH, FR)))
        calendar_range = [x.date() for x in calendar_range]
        calendar_range.sort(reverse=True)

        self.prices = {x.date: x for x in self.prices}
        calendar = list()
        for day in calendar_range:
            if day in self.prices:
                calendar.append(self.prices[day])
            else:
                calendar.append(PriceDto(date=day, price=''))

        table = Table(border_style='grey19', row_styles=[Style(bgcolor='grey11'), ''])

        table.add_column('', style='dodger_blue2')
        table.add_column('Date', style='orange3')
        table.add_column('Price', style='white', justify='right')
        table.add_column('', style='dodger_blue2')
        table.add_column('Date', style='orange3')
        table.add_column('Price', style='white', justify='right')
        table.add_column('', style='dodger_blue2')
        table.add_column('Date', style='orange3')
        table.add_column('Price', style='white', justify='right')

        slice_1 = calendar[0:15]
        slice_2 = calendar[15:30]
        slice_3 = calendar[30:45]

        for i in range(15):
            price_1 = slice_1[i]
            price_2 = slice_2[i]
            price_3 = slice_3[i]

            rich_day_1 = price_1.date.strftime('%a')[0]
            rich_date_1 = price_1.date.strftime('%Y-%m-%d')
            rich_price_1 = str(price_1.price)

            rich_day_2 = price_2.date.strftime('%a')[0]
            rich_date_2 = price_2.date.strftime('%Y-%m-%d')
            rich_price_2 = str(price_2.price)

            rich_day_3 = price_3.date.strftime('%a')[0]
            rich_date_3 = price_3.date.strftime('%Y-%m-%d')
            rich_price_3 = str(price_3.price)

            table.add_row(rich_day_1, rich_date_1, rich_price_1, rich_day_2, rich_date_2, rich_price_2, rich_day_3,
                          rich_date_3, rich_price_3)

            if rich_day_1 == 'M':
                table.add_row('', '', '')

        return table
