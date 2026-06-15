import click
from dotenv import load_dotenv


@click.group()
def app() -> None:
    load_dotenv()
