from __future__ import annotations

from pathlib import Path

import pandas as pd

from pipeline.config import settings
from pipeline.database import ensure_database_ready, get_engine


CURRENCY_MAP = {
    "mmk": "MMK",
    "ks": "MMK",
    "kyat": "MMK",
    "mmk ": "MMK",
}


def extract_sales_data(csv_path: str | None = None) -> pd.DataFrame:
    source = Path(csv_path or settings.source_csv)
    if not source.exists():
        raise FileNotFoundError(f"Sales CSV not found: {source}")
    return pd.read_csv(source)


def transform_sales_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    transformed = df.copy()

    transformed["sale_date"] = pd.to_datetime(transformed["sale_date"], errors="coerce")
    transformed = transformed.dropna(subset=["sale_date", "unit_price", "quantity"])

    transformed["product_name"] = (
        transformed["product_name"].fillna("Unknown Product").astype(str).str.strip().str.title()
    )
    transformed["category"] = transformed["category"].fillna("Unknown").astype(str).str.strip().str.title()
    transformed["region"] = transformed["region"].fillna("Unknown").astype(str).str.strip().str.title()
    transformed["city"] = transformed["city"].fillna("Unknown").astype(str).str.strip().str.title()
    transformed["payment_method"] = (
        transformed["payment_method"].fillna("Unknown").astype(str).str.strip().str.title()
    )

    transformed["currency"] = (
        transformed["currency"]
        .fillna("MMK")
        .astype(str)
        .str.strip()
        .str.lower()
        .map(CURRENCY_MAP)
        .fillna("MMK")
    )

    transformed["unit_price"] = pd.to_numeric(transformed["unit_price"], errors="coerce")
    transformed["quantity"] = pd.to_numeric(transformed["quantity"], errors="coerce")
    transformed = transformed.dropna(subset=["unit_price", "quantity"])

    transformed["quantity"] = transformed["quantity"].astype(int)
    transformed["unit_price_mmk"] = transformed["unit_price"].round(2)
    transformed["revenue_mmk"] = (transformed["unit_price_mmk"] * transformed["quantity"]).round(2)
    transformed["sale_day"] = transformed["sale_date"].dt.date
    transformed["sale_week"] = transformed["sale_date"].dt.to_period("W-SUN").apply(lambda period: period.start_time.date())

    cleaned_sales = transformed[
        [
            "sale_id",
            "sale_date",
            "sale_day",
            "sale_week",
            "product_name",
            "category",
            "region",
            "city",
            "payment_method",
            "currency",
            "quantity",
            "unit_price_mmk",
            "revenue_mmk",
        ]
    ].sort_values(["sale_date", "sale_id"])

    daily_revenue = (
        cleaned_sales.groupby("sale_day", as_index=False)
        .agg(total_revenue_mmk=("revenue_mmk", "sum"), total_orders=("sale_id", "count"))
        .sort_values("sale_day")
    )

    weekly_revenue = (
        cleaned_sales.groupby("sale_week", as_index=False)
        .agg(total_revenue_mmk=("revenue_mmk", "sum"), total_orders=("sale_id", "count"))
        .sort_values("sale_week")
    )

    return cleaned_sales, daily_revenue, weekly_revenue


def load_to_postgres(
    cleaned_sales: pd.DataFrame,
    daily_revenue: pd.DataFrame,
    weekly_revenue: pd.DataFrame,
) -> None:
    engine = get_engine()
    ensure_database_ready(engine)

    with engine.begin() as connection:
        cleaned_sales.to_sql("sales_cleaned", connection, if_exists="replace", index=False)
        daily_revenue.to_sql("revenue_daily", connection, if_exists="replace", index=False)
        weekly_revenue.to_sql("revenue_weekly", connection, if_exists="replace", index=False)


def run_pipeline(csv_path: str | None = None) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    extracted = extract_sales_data(csv_path)
    cleaned_sales, daily_revenue, weekly_revenue = transform_sales_data(extracted)
    load_to_postgres(cleaned_sales, daily_revenue, weekly_revenue)
    return cleaned_sales, daily_revenue, weekly_revenue
