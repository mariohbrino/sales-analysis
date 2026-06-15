import os


def download_dataset(
    dataset: str,
    output_dir: str,
    output_filename: str,
) -> None:
    output_path: str = os.path.join(output_dir, output_filename)

    if os.path.exists(output_path):
        print(f"Dataset already exists at: '{output_path}'")
        return

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

    print(f"Dataset downloaded and extracted to: '{output_path}'")
