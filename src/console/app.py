import click
from dotenv import load_dotenv

from commands.download_command import download_dataset_command


@click.group()
def app() -> None:
    load_dotenv()


app.add_command(download_dataset_command, name="download")
