from textual import events
from textual.app import App
from textual.widgets import ScrollView
from textual_inputs import TextInput

from src.application.queries.get_historical_prices import GetHistoricalPricesQuery
from src.infrastructure.repositories.yahoo_repository import YahooRepository
from src.presentation.tables.historical_prices import HistoricalPricesTableFormatter
from src.presentation.widgets.footer import MinibloomFooter
from src.presentation.widgets.header import MinibloomHeader


class TerminalApp(App):
    search_bar: TextInput
    body: ScrollView

    async def on_load(self, event: events.Load) -> None:
        await self.bind("ctrl+c", "quit", show=False)
        await self.bind("q", "quit", "Quit")
        await self.bind("enter", "submit", "Submit")

    async def on_mount(self, event: events.Mount) -> None:
        self.search_bar = TextInput(
            name="search",
            title="Search",
        )

        header = MinibloomHeader()
        footer = MinibloomFooter()

        self.body = ScrollView()

        await self.view.dock(header, edge="top")
        await self.view.dock(self.search_bar, edge="top", size=3)
        await self.view.dock(footer, edge="bottom")
        await self.view.dock(self.body, edge="top")

    async def action_submit(self):
        # with self.console.status("Searching..."):
        search_term = self.search_bar.value
        results = GetHistoricalPricesQuery(YahooRepository()).execute(search_term)

        table = HistoricalPricesTableFormatter(results).format()

        await self.body.update(table)
