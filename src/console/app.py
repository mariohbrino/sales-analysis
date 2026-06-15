import click
from dotenv import load_dotenv

from commands.analyze_trends_command import analyze_trends_command
from commands.download_command import download_dataset_command
from commands.sales_channel_command import sales_channel_command


@click.group()
def app() -> None:
    load_dotenv()


app.add_command(download_dataset_command)
app.add_command(analyze_trends_command)
app.add_command(sales_channel_command)
