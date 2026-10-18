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


if __name__ == "__main__":
    from pathlib import Path

    from load import load_csv

    logging.basicConfig(level=logging.INFO)
    orders = clean_orders(load_csv(Path("data/olist_orders_dataset.csv")))

    print(orders.dtypes)
    print(orders["delivery_days"].describe())
    print(orders[orders["order_delivered_customer_date"].isna()]["order_status"].value_counts())
    print(f"Share of late deliveries: {orders['is_late'].mean():.1%}")

    delivered = orders[orders["order_status"] == "delivered"]
    print( "Orders with status 'delivered':" , len(delivered))
    print("'delivered' orders without delivery date:",
          delivered["order_delivered_customer_date"].isna().sum())

    missing = delivered[delivered["order_delivered_customer_date"].isna()]
    print("\nThese orders (delivered, but no delivery date):")
    print(missing[["order_id", "order_purchase_timestamp", "order_delivered_carrier_date"]])

    with_date = orders[orders["order_delivered_customer_date"].notna()]
    print("\nStatuses of orders that DO have a delivery date:")
    print(with_date["order_status"].value_counts())

    slowest = orders.sort_values("delivery_days", ascending=False)
    print( "Slowest deliveries:" )
    print(slowest[["order_id", "order_purchase_timestamp", "order_delivered_customer_date","order_estimated_delivery_date", "delivery_days"]].head(5).to_string())


    very_slow = orders[orders["delivery_days"] > 60]
    print("Orders delivered after more than 60 days:", len(very_slow))


    normal = orders[orders["delivery_days"] <= 60]
    print("Average delivery time without orders over 60 days:", round(normal["delivery_days"].mean(), 1))
    print("Median delivery time:", orders["delivery_days"].median())


    products = clean_products(load_csv(Path("data/olist_products_dataset.csv")))
    print("Products with category 'unknown':", (products["product_category_name"] == "unknown").sum())