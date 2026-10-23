import pandas as pd

from clean import clean_orders


def make_orders() -> pd.DataFrame:
    """Three orders: on time, late, not delivered."""
    return pd.DataFrame(
        {
            "order_id": ["on_time", "late", "not_delivered"],
            "order_purchase_timestamp": ["2018-01-01 10:00:00"] * 3,
            "order_approved_at": ["2018-01-01 11:00:00"] * 3,
            "order_delivered_carrier_date": ["2018-01-02 10:00:00"] * 3,
            "order_delivered_customer_date": [
                "2018-01-05 10:00:00",
                "2018-01-12 10:00:00",
                None,
            ],
            "order_estimated_delivery_date": ["2018-01-10 00:00:00"] * 3,
        }
    )


def test_delivery_days():
    result = clean_orders(make_orders())
    assert result.loc[0, "delivery_days"] == 4
    assert result.loc[1, "delivery_days"] == 11
    assert pd.isna(result.loc[2, "delivery_days"])


def test_is_late():
    result = clean_orders(make_orders())
    assert not result.loc[0, "is_late"]
    assert result.loc[1, "is_late"]
    assert pd.isna(result.loc[2, "is_late"])
