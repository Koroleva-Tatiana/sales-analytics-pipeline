"""Exploration of the cleaned orders and products (not part of the pipeline)."""

import logging
from pathlib import Path

from clean import clean_orders, clean_products
from load import load_csv

if __name__ == "__main__":

    

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