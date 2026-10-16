
"""Loading CSV files and checking basic data quality."""

import logging 
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def load_csv(path: Path) -> pd.DataFrame:
    """Read a CSV file into a DataFrame."""
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    df = pd.read_csv(path)
    logger.info("Loaded %s: %d rows, %d columns", path.name, *df.shape)
    return df


def quality_report(df: pd.DataFrame, name: str) -> dict:
    """Return simple data quality metrics for a table."""
    return {
        "table": name,
        "rows": len(df),
        "columns": df.shape[1],
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_values": int(df.isna().sum().sum()),
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    orders = load_csv(Path("data/olist_orders_dataset.csv"))
    print(quality_report(orders, "orders"))
    print(orders.isna().sum())
    print(orders.dtypes)

