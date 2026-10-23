# Sales Analytics Pipeline

A Python pipeline that loads e-commerce data (Olist Brazilian E-Commerce
dataset from Kaggle), checks and cleans it, stores it in SQLite, analyses it
with SQL and creates an Excel report with a chart.

![Excel report](docs/report_preview.png)

## What it does

1. **Load** the CSV files and check data quality (rows, duplicates, missing values).
2. **Clean** the data: convert dates, calculate delivery time, flag late deliveries.
3. **Store** the tables in a SQLite database.
4. **Analyse** with SQL (JOINs, aggregations): revenue by month and by category.
5. **Report**: Excel file with two sheets and a line chart.

## Project structure

```
main.py              # runs the whole pipeline (command line)
src/
  load.py            # reading CSV files, data quality report
  clean.py           # cleaning orders and products
  database.py        # saving tables to SQLite
  analysis.py        # SQL queries
  report.py          # Excel report
  explore.py         # data exploration (not part of the pipeline)
  make_sample.py     # creates the small sample dataset
tests/               # pytest tests
data/sample/         # small sample (200 orders)
```

## How to run

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py --data-dir data/sample --db data/sample.db --output output/sample_report.xlsx
```

This uses the sample in `data/sample/`. To run it on the full dataset,
download it from Kaggle, put the CSV files into `data/` and run `python main.py`.

Tests: `pytest`

## Data quality notes

- 2,965 of 99,441 orders have no delivery date. Most of them are orders that
  are still in transit (`shipped`) or will never arrive (`canceled`,
  `unavailable`). These gaps are expected, so the missing values were kept.
- 8 orders have the status `delivered` but no delivery date. They are excluded
  from the delivery time calculation.
- 6 `canceled` orders have a delivery date. They are kept in the data, and the
  reason is unknown.
- 288 delivered orders (about 0.3%) took more than 60 days. Several of the
  slowest ones share the same delivery date, so the date may have been entered
  in bulk. These orders are kept. Excluding them changes the mean delivery time
  only slightly (12.1 to 11.9 days), the median stays at 10 days.
- Delivery time and the share of late deliveries (8.1%) are calculated only for
  orders with a delivery date. Orders without one are not counted as "on time".
- 610 products have no category. They are labeled `unknown` and account for
  about 1.3% of revenue from delivered orders.
- Two categories (`pc_gamer`, `portateis_cozinha_e_preparadores_de_alimentos`)
  have no English translation. They keep their Portuguese names
  (`LEFT JOIN` + `COALESCE`).
- Revenue is the sum of item prices of delivered orders (without freight).
  The data for 2016 is incomplete, and the dataset ends in August 2018.

## Tech stack

Python, pandas, SQLite (sqlite3), SQL, openpyxl, argparse, logging, pytest, Git.

## Data source

Olist Brazilian E-Commerce Public Dataset (Kaggle). The files in `data/sample/`
are a random subset of it (created with `src/make_sample.py`). Please check the
license on the Kaggle page before reusing the data.
