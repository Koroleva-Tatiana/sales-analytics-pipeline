import pandas as pd

from clean import clean_products


def make_products() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "product_id": ["a", "b"],
            "product_category_name": ["toys", None],
        }
    )


def test_missing_category_becomes_unknown():
    result = clean_products(make_products())
    assert result.loc[0, "product_category_name"] == "toys"
    assert result.loc[1, "product_category_name"] == "unknown"


def test_original_table_is_not_changed():
    products = make_products()
    clean_products(products)
    assert products["product_category_name"].isna().sum() == 1
