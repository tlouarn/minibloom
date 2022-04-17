import typer

from src.presentation.terminal import TerminalApp

app = typer.Typer(add_completion=False)


@app.command()
def launch():
    TerminalApp.run(title="minibloom")


if __name__ == "__main__":
    app()
