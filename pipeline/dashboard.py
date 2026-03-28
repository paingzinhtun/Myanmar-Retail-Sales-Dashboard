from pathlib import Path
import sys

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from pipeline.database import get_engine


st.set_page_config(page_title="Myanmar Sales Dashboard", layout="wide")


@st.cache_data(ttl=60)
def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    engine = get_engine()
    sales = pd.read_sql("SELECT * FROM sales_cleaned ORDER BY sale_date", engine)
    daily = pd.read_sql("SELECT * FROM revenue_daily ORDER BY sale_day", engine)
    weekly = pd.read_sql("SELECT * FROM revenue_weekly ORDER BY sale_week", engine)
    return sales, daily, weekly


def main() -> None:
    st.title("Myanmar Retail Sales Dashboard")
    st.caption("KPIs and revenue trends from the PostgreSQL-backed sales pipeline")

    try:
        sales, daily, weekly = load_data()
    except Exception as exc:
        st.error(
            "Unable to load dashboard data from PostgreSQL. Run the pipeline first and confirm the database is available."
        )
        st.code(str(exc))
        return

    total_revenue = float(sales["revenue_mmk"].sum())
    total_orders = int(sales["sale_id"].count())
    avg_order_value = total_revenue / total_orders if total_orders else 0
    top_region = sales.groupby("region")["revenue_mmk"].sum().sort_values(ascending=False).index[0]

    metric_1, metric_2, metric_3, metric_4 = st.columns(4)
    metric_1.metric("Total Revenue (MMK)", f"{total_revenue:,.0f}")
    metric_2.metric("Total Orders", f"{total_orders}")
    metric_3.metric("Average Order Value (MMK)", f"{avg_order_value:,.0f}")
    metric_4.metric("Top Region", str(top_region))

    left, right = st.columns(2)

    with left:
        st.subheader("Daily Revenue")
        daily_chart = daily.copy()
        daily_chart["sale_day"] = pd.to_datetime(daily_chart["sale_day"])
        st.line_chart(daily_chart.set_index("sale_day")["total_revenue_mmk"])

    with right:
        st.subheader("Weekly Revenue")
        weekly_chart = weekly.copy()
        weekly_chart["sale_week"] = pd.to_datetime(weekly_chart["sale_week"])
        st.bar_chart(weekly_chart.set_index("sale_week")["total_revenue_mmk"])

    bottom_left, bottom_right = st.columns(2)

    with bottom_left:
        st.subheader("Revenue by Region")
        region_summary = (
            sales.groupby("region", as_index=False)["revenue_mmk"].sum().sort_values("revenue_mmk", ascending=False)
        )
        st.dataframe(region_summary, use_container_width=True, hide_index=True)

    with bottom_right:
        st.subheader("Top Products")
        product_summary = (
            sales.groupby("product_name", as_index=False)["revenue_mmk"]
            .sum()
            .sort_values("revenue_mmk", ascending=False)
            .head(10)
        )
        st.dataframe(product_summary, use_container_width=True, hide_index=True)

    st.subheader("Cleaned Sales Data")
    st.dataframe(sales, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
