from typer import Typer

from .records import app as records_app

app = Typer()

app.add_typer(records_app, name="rec")
