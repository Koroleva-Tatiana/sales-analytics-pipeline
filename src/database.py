"""Saving cleaned tables into a SQLite database."""

import logging
import sqlite3
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

DB_PATH = Path("data/olist.db")


def save_table(df: pd.DataFrame, table_name: str, conn: sqlite3.Connection) -> None:
    """Write a DataFrame to a SQLite table (replaces the table if it exists)."""
    df = df.copy()
    # SQLite has no date type, so dates are stored as text like "2018-01-05 10:30:00"
    for col in df.select_dtypes(include="datetime").columns:
        df[col] = df[col].dt.strftime("%Y-%m-%d %H:%M:%S")
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    logger.info("Saved table %s: %d rows", table_name, len(df))


if __name__ == "__main__":
    from clean import clean_orders, clean_products
    from load import load_csv

    logging.basicConfig(level=logging.INFO)

    tables = {
        "orders": clean_orders(load_csv(Path("data/olist_orders_dataset.csv"))),
        "order_items": load_csv(Path("data/olist_order_items_dataset.csv")),
        "customers": load_csv(Path("data/olist_customers_dataset.csv")),
        "products": clean_products(load_csv(Path("data/olist_products_dataset.csv"))),
    }

    conn = sqlite3.connect(DB_PATH)
    
    for name, df in tables.items():
        save_table(df, name, conn)

    cursor = conn.execute("SELECT COUNT(*) FROM orders")
    print("Rows in orders table:", cursor.fetchone()[0])
    conn.close()