import os

from dotenv import load_dotenv


def download_kaggle_dataset(
    dataset: str,
    output_dir: str,
) -> None:
    from kaggle.api.kaggle_api_extended import KaggleApi

    api = KaggleApi()

    print(f"Creating output directory: '{output_dir}'")
    os.makedirs(output_dir, exist_ok=True)

    api.authenticate()

    print(f"Downloading dataset: '{dataset}'")
    api.dataset_download_files(
        dataset,
        path=output_dir,
        unzip=True,
    )


def main() -> None:
    load_dotenv()

    output_dir = "./storage/datasets"

    download_kaggle_dataset(
        dataset="noopurbhatt/retail-sales-dataset",
        output_dir=output_dir,
    )


if __name__ == "__main__":
    main()
