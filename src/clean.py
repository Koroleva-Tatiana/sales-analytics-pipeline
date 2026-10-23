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
    late = df["order_delivered_customer_date"] > df["order_estimated_delivery_date"]
    df["is_late"] = late.astype("boolean").mask(
        df["order_delivered_customer_date"].isna()
)

    logger.info("Cleaned orders: %d rows", len(df))
    return df


def clean_products(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing product categories with 'unknown'."""
    df = df.copy()
    df["product_category_name"] = df["product_category_name"].fillna("unknown")
    logger.info("Cleaned products: %d rows", len(df))
    return df
