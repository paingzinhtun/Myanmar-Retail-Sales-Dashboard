# Sample Output

This file shows the kind of output this project produces after the pipeline runs successfully.

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
| 1       | 2026-03-01 | Shan Noodles | Food       | Yangon   | Yangon   | Cash     | MMK      | 3              | 2500.00  | 7500.00       |
| 2       | 2026-03-01 | Tea Mix      | Beverage   | Mandalay | Mandalay | Kbzpay   | MMK      | 5              | 1800.00  | 9000.00       |
| 3       | 2026-03-02 | Laphet       | Food       | Naypyitaw| Naypyitaw| Wavepay  | MMK      | 4              | 3200.00  | 12800.00      |
+---------+------------+------------+--------------+----------+----------+----------+----------+----------------+----------+---------------+
```

## 3. Example Daily Revenue Table

Sample rows from `revenue_daily`:

```text
+------------+-------------------+--------------+
| sale_day   | total_revenue_mmk | total_orders |
+------------+-------------------+--------------+
| 2026-03-01 | 16500.00          | 2            |
| 2026-03-02 | 26000.00          | 2            |
| 2026-03-03 | 110000.00         | 2            |
+------------+-------------------+--------------+
```

## 4. Example Weekly Revenue Table

Sample rows from `revenue_weekly`:

```text
+------------+-------------------+--------------+
| sale_week  | total_revenue_mmk | total_orders |
+------------+-------------------+--------------+
| 2026-02-23 | 16500.00          | 2            |
| 2026-03-02 | 350900.00         | 14           |
| 2026-03-09 | 267700.00         | 14           |
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
