# Sample Output

This file shows the kind of output this project produces after the pipeline runs successfully.

The project currently uses a sample dataset with more than 500 sales rows spanning January 1, 2026 to March 28, 2026.

## 1. Console Output From ETL Run

Example command:

```powershell
python run_pipeline.py
```

Example result:

```text
Pipeline completed successfully.
Loaded cleaned sales data into PostgreSQL.
Created tables:
- sales_cleaned
- revenue_daily
- revenue_weekly
```

Note:

The exact console output may vary depending on how you run the project and whether you add more logging later.

## 2. Example Cleaned Sales Data

Sample rows from `sales_cleaned`:

```text
+---------+------------+------------+--------------+----------+----------+----------+----------+----------------+----------+---------------+-------------+
| sale_id | sale_date  | product    | category     | region   | city     | payment  | currency | quantity       | unit_mmk | revenue_mmk   |
+---------+------------+------------+--------------+----------+----------+----------+----------+----------------+----------+---------------+
| 1       | 2026-01-01 | Tea Mix      | Beverage   | Mandalay | Mandalay | Kbzpay   | MMK      | 3              | 1800.00  | 5400.00       |
| 2       | 2026-01-01 | Coffee Mix   | Beverage   | Yangon   | Pathein  | Cash     | MMK      | 5              | 2200.00  | 11000.00      |
| 3       | 2026-01-01 | Cooking Oil  | Grocery    | Mandalay | Meiktila | Wavepay  | MMK      | 7              | 13500.00 | 94500.00      |
+---------+------------+------------+--------------+----------+----------+----------+----------+----------------+----------+---------------+
```

## 3. Example Daily Revenue Table

Sample rows from `revenue_daily`:

```text
+------------+-------------------+--------------+
| sale_day   | total_revenue_mmk | total_orders |
+------------+-------------------+--------------+
| 2026-01-01 | 167800.00         | 6            |
| 2026-01-02 | 84200.00          | 6            |
| 2026-01-03 | 128100.00         | 6            |
+------------+-------------------+--------------+
```

## 4. Example Weekly Revenue Table

Sample rows from `revenue_weekly`:

```text
+------------+-------------------+--------------+
| sale_week  | total_revenue_mmk | total_orders |
+------------+-------------------+--------------+
| 2025-12-29 | 380100.00         | 24           |
| 2026-01-05 | 782300.00         | 42           |
| 2026-01-12 | 737100.00         | 42           |
+------------+-------------------+--------------+
```

## 5. Example Dashboard KPIs

The Streamlit dashboard displays business-facing metrics such as:

- Total Revenue (MMK)
- Total Orders
- Average Order Value
- Top Region

It also shows:

- a daily revenue line chart
- a weekly revenue bar chart
- a revenue by region table
- a top products table
- the cleaned sales dataset

## 6. Suggested Screenshots For Submission

If you are preparing this project for a report, portfolio, or class submission, useful screenshots would be:

1. Terminal output after running `python run_pipeline.py`
2. PostgreSQL tables showing `sales_cleaned`, `revenue_daily`, and `revenue_weekly`
3. Streamlit dashboard homepage
4. Daily and weekly revenue charts
5. KPI cards at the top of the dashboard

## 7. One-Line Summary

```text
The pipeline converts raw Myanmar retail sales data into cleaned PostgreSQL tables and dashboard-ready business metrics.
```
