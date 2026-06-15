import click

from domains.analyze_trends import AnalyzeTrend


@click.command(name="analyze-trends", help="Analyze the retail sales dataset")
@click.option("--input-dir", default="./storage/datasets", help="Input directory")
@click.option("--output-dir", default="./storage/reports", help="Output directory")
@click.option("--output-filename", default="trends_analysis.csv", help="Output filename")
def analyze_trends_command(
    input_dir: str,
    output_dir: str,
    output_filename: str,
) -> None:
    """
    Analyze the purchasing trends by gender for Brands 1 and 2 in the sports category.
    Question: What are the purchasing trends by gender for Brands 1 and 2 in the sports category?
    """

    analyze_trends = AnalyzeTrend()

    analyze_trends.process(
        input_dir=input_dir,
        output_dir=output_dir,
        output_filename=output_filename,
    )
