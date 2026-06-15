import os
from datetime import date

import polars as pl

from services.loader.load_dataset import load_dataframe
from services.writter.csv_writter import export_dataframe_to_csv
from utils.console_display import format_and_print


class SalesChannel:
    def _aggregate_sales_by_channel(
        self,
        lazyframe: pl.LazyFrame,
    ) -> pl.LazyFrame:
        return (
            lazyframe.group_by(["sales_channel"])
            .agg(
                [
                    pl.sum("sales_amount").alias("total_sales"),
                    pl.sum("quantity").alias("total_quantity"),
                ]
            )
            .sort(by=["total_sales"], descending=True)
        )

    def _filter_by_date_range(
        self,
        lazyframe: pl.LazyFrame,
    ) -> pl.LazyFrame:
        return lazyframe.filter(
            pl.col("transaction_date").is_between(
                date(2023, 1, 1),
                date(2024, 1, 1),
            )
        )

    def _calculate_sales_share(
        self,
        lazyframe: pl.LazyFrame,
    ) -> pl.LazyFrame:
        return lazyframe.with_columns(
            (pl.col("total_sales") / pl.col("total_sales").sum() * 100).alias("sales_share"),
            (pl.col("total_quantity") / pl.col("total_quantity").sum() * 100).alias("quantity_share"),
        )

    def process(
        self,
        input_dir: str,
        output_dir: str,
        output_filename: str,
    ) -> None:
        # Load the dataset into a LazyFrame
        input_path: str = os.path.join(input_dir, "retail_sales_dataset.csv")
        lazyframe: pl.LazyFrame = load_dataframe(
            input_path=input_path,
            schema=pl.Schema(
                {
                    "transaction_id": pl.String,
                    "transaction_date": pl.Date,
                    "customer_id": pl.String,
                    "customer_gender": pl.String,
                    "customer_age_group": pl.String,
                    "customer_segment": pl.String,
                    "product_id": pl.String,
                    "product_name": pl.String,
                    "category": pl.String,
                    "brand": pl.String,
                    "quantity": pl.Int64,
                    "unit_price": pl.Float64,
                    "discount_pct": pl.Int64,
                    "sales_amount": pl.Float64,
                    "payment_method": pl.String,
                    "sales_channel": pl.String,
                    "region": pl.String,
                }
            ),
        )

        # Apply filters and aggregations as needed
        period: pl.LazyFrame = self._filter_by_date_range(lazyframe=lazyframe)

        # Aggregate sales by channel
        period_by_sales_channel: pl.LazyFrame = self._aggregate_sales_by_channel(lazyframe=period)

        # Calculate sales share by channel
        sales_channels_share: pl.LazyFrame = self._calculate_sales_share(period_by_sales_channel)

        # Collect the main data
        period_collected: pl.DataFrame = sales_channels_share.collect()

        # Configure Polars to display numbers without scientific notation
        format_and_print(dataframe=period_collected)

        # Export the final result to CSV
        export_dataframe_to_csv(
            output_dir=output_dir,
            output_filename=output_filename,
            dataframe=period_collected,
        )

        output_file_path = os.path.join(output_dir, output_filename)

        print(f"Sales channels period exported to: '{output_file_path}'")
