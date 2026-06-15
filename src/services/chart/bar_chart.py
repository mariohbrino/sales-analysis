import os

import matplotlib.pyplot as plt
import polars as pl


class BarChart:
    def plot(
        self,
        dataframe: pl.DataFrame,
        output_dir: str,
        horizontal_data: str,
        vertical_data: str,
        title: str,
        horizontal_label: str,
        vertical_label: str,
        output_image_name: str,
        horizontal_size: int = 20,
        vertical_size: int = 15,
        title_size: int = 16,
        label_size: int = 12,
        colors: list[str] | None = None,
    ) -> None:
        plt.figure(figsize=(horizontal_size, vertical_size))

        # If no colors provided, use matplotlib's default color cycle for each bar
        if colors is None:
            colors = plt.cm.Set3.colors[: len(dataframe)]

        plt.bar(
            dataframe[horizontal_data],  # x-axis
            dataframe[vertical_data],  # y-axis
            color=colors,
            edgecolor="navy",
            alpha=0.8,
        )

        plt.title(title, fontsize=title_size)
        plt.xlabel(horizontal_label, fontsize=label_size)
        plt.ylabel(vertical_label, fontsize=label_size)

        os.makedirs(output_dir, exist_ok=True)
        output_image_path = os.path.join(output_dir, output_image_name)

        plt.savefig(output_image_path, format="png", dpi=200, bbox_inches="tight")
        plt.close()  # Close the figure to free memory

        print(f"Bar chart saved to: '{output_image_path}'")
