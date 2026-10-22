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


CATEGORY_REVENUE_SQL = """
SELECT
    p.product_category_name AS category,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(i.price), 2) AS revenue
FROM orders AS o
JOIN order_items AS i ON i.order_id = o.order_id
JOIN products AS p ON p.product_id = i.product_id
WHERE o.order_status = 'delivered'
GROUP BY category
ORDER BY revenue DESC
LIMIT 10
"""


def run_query(sql: str, conn: sqlite3.Connection) -> pd.DataFrame:
    """Run an SQL query and return the result as a DataFrame."""
    return pd.read_sql_query(sql, conn)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    conn = sqlite3.connect(DB_PATH)
    monthly = run_query(MONTHLY_REVENUE_SQL, conn)
    print(monthly.to_string(index=False))

    print("\nTop 10 categories by revenue:")
    categories = run_query(CATEGORY_REVENUE_SQL, conn)
    print(categories.to_string(index=False))


    unknown_sql = """
    SELECT
        COUNT(DISTINCT o.order_id) AS orders,
        ROUND(SUM(i.price), 2) AS revenue
    FROM orders AS o
    JOIN order_items AS i ON i.order_id = o.order_id
    JOIN products AS p ON p.product_id = i.product_id
    WHERE o.order_status = 'delivered'
      AND p.product_category_name = 'unknown'
    """
    print("\nCategory 'unknown':")
    print(run_query(unknown_sql, conn).to_string(index=False))



    total_sql = """
    SELECT ROUND(SUM(i.price), 2)
    FROM orders AS o
    JOIN order_items AS i ON i.order_id = o.order_id
    WHERE o.order_status = 'delivered'
    """
    unknown_sql_total = """
    SELECT ROUND(SUM(i.price), 2)
    FROM orders AS o
    JOIN order_items AS i ON i.order_id = o.order_id
    JOIN products AS p ON p.product_id = i.product_id
    WHERE o.order_status = 'delivered'
      AND p.product_category_name = 'unknown'
    """
    total = conn.execute(total_sql).fetchone()[0]
    unknown = conn.execute(unknown_sql_total).fetchone()[0]

    print(f"\nTotal revenue: {total:,.2f}")
    print(f"Revenue of 'unknown' category: {unknown:,.2f}")
    print(f"Share of 'unknown': {unknown / total:.1%}")


    conn.close()