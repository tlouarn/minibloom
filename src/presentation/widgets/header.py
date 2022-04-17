from datetime import datetime
from logging import getLogger

from rich.console import RenderableType
from rich.repr import Result
from rich.style import StyleType
from rich.table import Table
from textual import events
from textual.reactive import watch, Reactive
from textual.widget import Widget

log = getLogger("rich")


class MinibloomHeader(Widget):
    def __init__(
            self,
            *,
            tall: bool = True,
            style: StyleType = "dark_orange on black",
            clock: bool = True,
    ) -> None:
        super().__init__()
        self.tall = tall
        self.style = style
        self.clock = clock

    tall: Reactive[bool] = Reactive(True, layout=True)
    style: Reactive[StyleType] = Reactive("white on blue")
    clock: Reactive[bool] = Reactive(True)
    title: Reactive[str] = Reactive("")
    sub_title: Reactive[str] = Reactive("")

    @property
    def full_title(self) -> str:
        return f"{self.title} - {self.sub_title}" if self.sub_title else self.title

    def __rich_repr__(self) -> Result:
        yield self.title

    def get_clock(self) -> str:
        return datetime.now().time().strftime("%X")

    async def watch_tall(self, tall: bool) -> None:
        self.layout_size = 1

    # async def on_click(self, event: events.Click) -> None:
    #     self.tall = self.tall

    def render(self) -> RenderableType:
        header_table = Table.grid(padding=(0, 1), expand=True)
        header_table.style = self.style
        header_table.add_column(justify="left", ratio=0, width=8)
        header_table.add_column("title", justify="center", ratio=1)
        header_table.add_column("clock", justify="right", width=8)
        header_table.add_row(
            "", self.full_title, self.get_clock() if self.clock else ""
        )
        header: RenderableType
        header = header_table
        return header

    async def on_mount(self, event: events.Mount) -> None:
        self.set_interval(1.0, callback=self.refresh)

        async def set_title(title: str) -> None:
            self.title = title

        async def set_sub_title(sub_title: str) -> None:
            self.sub_title = sub_title

        watch(self.app, "title", set_title)
        watch(self.app, "sub_title", set_sub_title)
