import polars as pl


def format_and_print(
    dataframe: pl.DataFrame,
) -> None:
    with pl.Config(float_precision=2, set_tbl_width_chars=200, set_fmt_float="full"):
        print(dataframe)
