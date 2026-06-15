import os

import polars as pl


def export_dataframe_to_csv(
    output_dir: str,
    output_filename: str,
    dataframe: pl.DataFrame,
) -> None:
    os.makedirs(output_dir, exist_ok=True)
    output_path: str = os.path.join(output_dir, output_filename)

    dataframe.write_csv(output_path, quote_style="always")
