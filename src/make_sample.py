"""Create a small sample of the Olist data (about 200 orders) for demo and tests."""

from pathlib import Path

import pandas as pd

DATA_DIR = Path("data")
SAMPLE_DIR = DATA_DIR / "sample"


def read(filename: str) -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / filename)


if __name__ == "__main__":
    SAMPLE_DIR.mkdir(exist_ok=True)

    orders = read("olist_orders_dataset.csv").sample(200, random_state=42)
    items = read("olist_order_items_dataset.csv")
    items = items[items["order_id"].isin(orders["order_id"])]
    customers = read("olist_customers_dataset.csv")
    customers = customers[customers["customer_id"].isin(orders["customer_id"])]
    products = read("olist_products_dataset.csv")
    products = products[products["product_id"].isin(items["product_id"])]
    translation = read("product_category_name_translation.csv")

    samples = {
        "olist_orders_dataset.csv": orders,
        "olist_order_items_dataset.csv": items,
        "olist_customers_dataset.csv": customers,
        "olist_products_dataset.csv": products,
        "product_category_name_translation.csv": translation,
    }
    for filename, df in samples.items():
        df.to_csv(SAMPLE_DIR / filename, index=False)
        print(f"{filename}: {len(df)} rows")
