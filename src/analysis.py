"""SQL analysis of the Olist database."""

import logging
import sqlite3
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

DB_PATH = Path("data/olist.db")

MONTHLY_REVENUE_SQL = """
SELECT
    strftime('%Y-%m', o.order_purchase_timestamp) AS month,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(i.price), 2) AS revenue
FROM orders AS o
JOIN order_items AS i ON i.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY month
ORDER BY month
"""


def run_query(sql: str, conn: sqlite3.Connection) -> pd.DataFrame:
    """Run an SQL query and return the result as a DataFrame."""
    return pd.read_sql_query(sql, conn)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    conn = sqlite3.connect(DB_PATH)
    monthly = run_query(MONTHLY_REVENUE_SQL, conn)
    print(monthly.to_string(index=False))
    conn.close()