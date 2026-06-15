import click
from dotenv import load_dotenv

from commands.analyze_trends_command import analyze_trends_command
from commands.download_command import download_dataset_command


@click.group()
def app() -> None:
    load_dotenv()


app.add_command(download_dataset_command, name="download")
app.add_command(analyze_trends_command, name="analyze-trends")
