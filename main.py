"""Run the whole pipeline: CSV -> cleaning -> SQLite -> Excel report."""

import argparse
import logging
import sqlite3
import sys
from pathlib import Path

# make the modules in src/ importable
sys.path.insert(0, str(Path(__file__).parent / "src"))

from clean import clean_orders, clean_products  # noqa: E402
from database import save_table  # noqa: E402
from load import load_csv  # noqa: E402
from report import create_report  # noqa: E402

logger = logging.getLogger(__name__)

FILES = {
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "products": "olist_products_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}


def run_pipeline(data_dir: Path, db_path: Path, report_path: Path) -> None:
    """Load, clean and store the data, then create the Excel report."""
    tables = {name: load_csv(data_dir / filename) for name, filename in FILES.items()}
    tables["orders"] = clean_orders(tables["orders"])
    tables["products"] = clean_products(tables["products"])

    conn = sqlite3.connect(db_path)
    for name, df in tables.items():
        save_table(df, name, conn)
    create_report(conn, report_path)
    conn.close()
    logger.info("Done. Report: %s", report_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Sales analytics pipeline")
    parser.add_argument("--data-dir", type=Path, default=Path("data"),
                        help="folder with the Olist CSV files")
    parser.add_argument("--db", type=Path, default=Path("data/olist.db"),
                        help="path of the SQLite database")
    parser.add_argument("--output", type=Path, default=Path("output/report.xlsx"),
                        help="path of the Excel report")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    run_pipeline(args.data_dir, args.db, args.output)


if __name__ == "__main__":
    main()
