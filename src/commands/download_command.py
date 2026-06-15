import os

import click

from services.repository.download_repository import download_dataset


@click.command(help="Download the retail sales dataset from Kaggle")
@click.option("--output-dir", default="./storage/datasets", help="Output directory")
def download_dataset_command(
    output_dir: str,
) -> None:
    profile: str = "noopurbhatt"
    repository: str = "retail-sales-dataset"
    output_filename: str = "retail_sales_dataset.csv"
    dataset: str = os.path.join(profile, repository)

    download_dataset(
        dataset=dataset,
        output_dir=output_dir,
        output_filename=output_filename,
    )
