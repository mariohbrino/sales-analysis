import os

import polars as pl


def load_dataframe(
    input_path: str,
    schema: pl.Schema = None,
) -> pl.LazyFrame:
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File not found, could not find '{input_path}'")

    lazyframe: pl.LazyFrame = pl.scan_csv(
        input_path,
        has_header=True,
        schema=schema,
    )

    return lazyframe
