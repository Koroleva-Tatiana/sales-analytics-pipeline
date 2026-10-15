"""Cleaning the orders table: dates and delivery metrics."""

import logging

import pandas as pd

logger = logging.getLogger(__name__)

DATE_COLUMNS = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]


def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    """Convert date columns and add delivery metrics."""
    df = df.copy()

    for col in DATE_COLUMNS:
        # errors="coerce": unparseable values become NaT (missing date)
        df[col] = pd.to_datetime(df[col], errors="coerce")

    # days from purchase to delivery (missing if not delivered yet)
    df["delivery_days"] = (
        df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
    ).dt.days

    # True if delivered later than estimated
    df["is_late"] = (
        df["order_delivered_customer_date"] > df["order_estimated_delivery_date"]
    )

    logger.info("Cleaned orders: %d rows", len(df))
    return df


if __name__ == "__main__":
    from pathlib import Path

    from load import load_csv

    logging.basicConfig(level=logging.INFO)
    orders = clean_orders(load_csv(Path("data/olist_orders_dataset.csv")))
    print(orders.dtypes)
    print(orders["delivery_days"].describe())
    print(orders[orders["order_delivered_customer_date"].isna()]["order_status"].value_counts())