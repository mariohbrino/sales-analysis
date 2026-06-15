import os

import polars as pl

from services.loader.load_dataset import load_dataframe
from services.writter.csv_writter import export_dataframe_to_csv
from utils.console_display import format_and_print


class AnalyzeTrend:
    def _aggregate_sales_by_gender(
        self,
        lazyframe: pl.LazyFrame,
    ) -> pl.LazyFrame:
        return (
            lazyframe.group_by(["brand", "customer_gender"])
            .agg(
                pl.col("sales_amount").sum().alias("total_sales"),
            )
            .sort(
                by=["brand", "customer_gender", "total_sales"],
                descending=[False, False, True],
            )
        )

    def _filter_sports_brands(
        self,
        lazyframe: pl.LazyFrame,
    ) -> pl.LazyFrame:
        return lazyframe.filter(
            pl.col("category") == "Sports",
            pl.col("brand").is_in(["Brand 1", "Brand 2"]),
        )

    def _calculate_sales_share(
        self,
        lazyframe: pl.LazyFrame,
    ) -> pl.LazyFrame:
        return lazyframe.with_columns(
            (pl.col("total_sales") / pl.col("total_sales").sum().over("brand") * 100).alias("sales_share")
        )

    def _add_row_type_column(
        self,
        dataframe: pl.DataFrame,
    ) -> pl.DataFrame:
        return dataframe.with_columns(pl.lit("Detail").alias("row_type"))

    def _organize_trend_data(
        self,
        trends_with_type: pl.DataFrame,
        subtotals: pl.DataFrame,
        grand_total: pl.DataFrame,
    ) -> pl.DataFrame:
        # Combine all: main data + subtotals + grand total
        final_result: pl.DataFrame = pl.concat([trends_with_type, subtotals, grand_total])

        final_result: pl.DataFrame = (
            final_result.with_columns(
                pl.when(pl.col("row_type") == "Detail")
                .then(1)
                .when(pl.col("row_type") == "Subtotal")
                .then(2)
                .when(pl.col("row_type") == "Grand Total")
                .then(3)
                .otherwise(4)
                .alias("sort_order")
            )
            .sort(by=["brand", "sort_order", "customer_gender"], nulls_last=True)
            .drop("sort_order")
        )

        # Reorder columns for better readability
        final_result: pl.DataFrame = final_result.select(
            [
                "row_type",
                "brand",
                "customer_gender",
                "total_sales",
                "sales_share",
            ]
        )
        return final_result

    def _calculate_brand_subtotals(
        self,
        dataframe: pl.DataFrame,
    ) -> pl.DataFrame:
        return (
            dataframe.group_by("brand")
            .agg(pl.col("total_sales").sum())
            .with_columns(
                pl.lit(None).cast(pl.String).alias("customer_gender"),
                pl.lit(100.0).alias("sales_share"),
                pl.lit("Subtotal").alias("row_type"),
            )
            .select(["brand", "customer_gender", "total_sales", "sales_share", "row_type"])
        )

    def _calculate_grand_total(
        self,
        dataframe: pl.DataFrame,
    ) -> pl.DataFrame:
        return pl.DataFrame(
            {
                "brand": [None],
                "customer_gender": [None],
                "total_sales": [dataframe["total_sales"].sum()],
                "sales_share": [100.0],
                "row_type": ["Grand Total"],
            }
        )

    def process(
        self,
        input_dir: str,
        output_dir: str,
        output_filename: str,
    ) -> None:
        # Load the dataset into a LazyFrame
        input_path: str = os.path.join(input_dir, "retail_sales_dataset.csv")
        dataframe: pl.LazyFrame = load_dataframe(
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

        # Filter for sports brands
        sports_brands: pl.LazyFrame = self._filter_sports_brands(lazyframe=dataframe)

        # Aggregate sales by gender
        trends_by_gender: pl.LazyFrame = self._aggregate_sales_by_gender(lazyframe=sports_brands)

        # Calculate sales share by gender
        trends_share: pl.LazyFrame = self._calculate_sales_share(lazyframe=trends_by_gender)

        # Collect the main data
        trends_collected: pl.DataFrame = trends_share.collect()

        # Add row_type column to main data
        trends_with_type: pl.DataFrame = self._add_row_type_column(dataframe=trends_collected)

        # Create subtotals per brand
        subtotals: pl.DataFrame = self._calculate_brand_subtotals(dataframe=trends_collected)

        # Create grand total
        grand_total: pl.DataFrame = self._calculate_grand_total(dataframe=trends_collected)

        # Sort to keep brand groups together with correct order (details, then subtotals, then grand total)
        final_result: pl.DataFrame = self._organize_trend_data(
            trends_with_type=trends_with_type,
            subtotals=subtotals,
            grand_total=grand_total,
        )

        # Configure Polars to display numbers without scientific notation
        format_and_print(dataframe=final_result)

        # Export the final result to CSV
        export_dataframe_to_csv(
            output_dir=output_dir,
            output_filename=output_filename,
            dataframe=final_result,
        )
