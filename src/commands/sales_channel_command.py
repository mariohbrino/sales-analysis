import click

from domains.sales_channels import SalesChannel


@click.command(name="analyze-sales-channel", help="Analyze sales by channel")
@click.option("--input-dir", default="./storage/datasets", help="Input directory")
@click.option("--output-dir", default="./storage/reports", help="Output directory")
@click.option("--output-filename", default="sales_channels_analysis.csv", help="Output filename")
def sales_channel_command(
    input_dir: str,
    output_dir: str,
    output_filename: str,
) -> None:
    """
    Analyze sales by channel.
    Question: Which sales channel performed best on the first year post the COVID-19 pandemic?
    Info: Covid-19 was considered ended by May 2023 on the United States, for our
    use case it will consider January 2023 as the end of the pandemic period.
    """

    sales_channel = SalesChannel()

    sales_channel.process(
        input_dir=input_dir,
        output_dir=output_dir,
        output_filename=output_filename,
    )
