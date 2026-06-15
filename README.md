# Overview

This application is designed for show case purposes of data analysis by using Python and dependencies
that can provide data processing and output results to respond commun or specific questions to give a
expected result with csv reports for review of decision makers.

The dataset used contains a list of retail transactions with sales, products, customers, and channels
with actionable sales insights providing a structured view of how customers purchase, how products
perform, and how reveneu is generated.

The purpose of this application is for research and development for show case of a given datase for data
analysis. By using Polars to read data and write reports. Polars provides an intuitive API that's familiar
with Pandas, high performance, and efficiency capabilities.

# Data Analysis Results

What are the purchasing trends by gender for Brands 1 and 2 in the sports category?
Which sales channel performed best on the first year post the COVID-19 pandemic?

# Development Environment

Worked with Python 3.13 and VSCode on macOS Tahoe, and using UV as package management
and Ruff for linting and code formating. Using Polars to analysis of the data and Kaggle
to download the dataset.

## Set up

Install UV package manager if you haven't already:
```bash
pip install uv
```

Create and activate a virtual environment with Python 3.13:
```bash
uv sync
source .venv/bin/activate
```

> [!IMPORTANT]
> When working with Apple Silicon (ARM64), it requires to install python 3.13 using homebrew
> and define flag --python /opt/homebrew/bin/python3.13 due to architecture-specific
> dependencies.

Install the package in editable mode:
```bash
uv pip install -e .
```

# Useful Websites

* [Kaggle](https://www.kaggle.com/)
* [VSCode](https://code.visualstudio.com/)
* [Python](https://www.python.org/)
* [Ruff](https://docs.astral.sh/ruff/)
* [Polars](https://pola.rs/)
* [Matplotlib](https://matplotlib.org/)
