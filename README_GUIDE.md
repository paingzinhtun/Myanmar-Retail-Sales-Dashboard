# Myanmar Retail Sales Pipeline Guide

This document is a portfolio-style walkthrough of the project. The original quick-start documentation is still available in [README.md](/C:/Users/HP/Documents/Myn_pipeline/README.md).

## Project Overview

This project simulates a retail sales pipeline for a Myanmar shop. It takes raw transaction data from a CSV file, cleans and transforms it with Pandas, stores the results in PostgreSQL, and presents key business metrics in a Streamlit dashboard.

The sample dataset currently covers January 1, 2026 through March 28, 2026 and contains more than 500 sales records, which makes the trends and summaries more realistic for practice.

At a high level, the project covers five stages:

1. Extract raw sales data from a CSV file
2. Transform and clean the data with Pandas
3. Load detailed and aggregated tables into PostgreSQL
4. Orchestrate repeat runs with a lightweight Python scheduler
5. Visualize KPIs and trends in Streamlit

## Architecture Summary

```text
Source Layer        : CSV file
Processing Layer    : Pandas ETL
Storage Layer       : PostgreSQL
Orchestration Layer : Python scheduler
Presentation Layer  : Streamlit
```

## End-to-End Flow

```text
+----------------------+
| sales_data.csv       |
| Raw shop sales data  |
+----------+-----------+
           |
           v
+----------------------+
| Extract              |
| read CSV with Pandas |
+----------+-----------+
           |
           v
+-------------------------------+
| Transform                     |
| - clean nulls                 |
| - standardize currency to MMK |
| - calculate revenue           |
| - create daily summary        |
| - create weekly summary       |
+----------+--------------------+
           |
           v
+-------------------------------+
| Load to PostgreSQL            |
| - sales_cleaned               |
| - revenue_daily               |
| - revenue_weekly              |
+----------+--------------------+
           |
           v
+-------------------------------+
| Streamlit Dashboard           |
| - KPIs                        |
| - daily trend                 |
| - weekly trend                |
| - region and product views    |
+-------------------------------+
```

## What The Project Solves

Raw CSV files are simple for storing records, but they are not ideal for analytics, dashboards, or scheduled reporting. This project turns raw transaction rows into structured and queryable business tables, making the data easier to analyze and present.

It is designed as a small but realistic example of a beginner-to-intermediate data engineering project.

## File Responsibilities

### [run_pipeline.py](/C:/Users/HP/Documents/Myn_pipeline/run_pipeline.py)

This is the one-time pipeline entrypoint. It calls the ETL workflow and refreshes the PostgreSQL tables.

### [pipeline/config.py](/C:/Users/HP/Documents/Myn_pipeline/pipeline/config.py)

This file loads runtime settings from [`.env`](/C:/Users/HP/Documents/Myn_pipeline/.env), including database credentials, CSV path, and scheduler interval.

### [pipeline/database.py](/C:/Users/HP/Documents/Myn_pipeline/pipeline/database.py)

This file manages database connectivity. It creates the SQLAlchemy engine, checks that PostgreSQL is reachable, and creates the target database if it does not already exist.

### [pipeline/etl.py](/C:/Users/HP/Documents/Myn_pipeline/pipeline/etl.py)

This is the core ETL module. It contains the extract, transform, and load logic for the project.

### [pipeline/scheduler.py](/C:/Users/HP/Documents/Myn_pipeline/pipeline/scheduler.py)

This file runs the ETL repeatedly using the `schedule` library. It acts as a simple orchestrator and is intended as a stepping stone to Airflow or another workflow tool later.

### [pipeline/dashboard.py](/C:/Users/HP/Documents/Myn_pipeline/pipeline/dashboard.py)

This is the Streamlit application. It reads the processed tables from PostgreSQL and displays metrics, charts, and tabular summaries.

### [data/raw/sales_data.csv](/C:/Users/HP/Documents/Myn_pipeline/data/raw/sales_data.csv)

This is the raw source dataset. It contains sample Myanmar retail sales data with products, regions, cities, payment methods, quantities, and prices across more than 500 sales rows.

## ETL Flow In Detail

### 1. Extract

The pipeline reads [sales_data.csv](/C:/Users/HP/Documents/Myn_pipeline/data/raw/sales_data.csv) into a Pandas DataFrame.

At this stage, the data is still raw and may contain:

- missing values
- inconsistent currency labels
- formatting differences across text columns

### 2. Transform

The transformation step in [etl.py](/C:/Users/HP/Documents/Myn_pipeline/pipeline/etl.py) performs the main business logic.

It:

- parses `sale_date` into a proper datetime
- drops rows with invalid or missing required date and numeric fields
- fills null values in text fields such as product, region, city, and payment method
- standardizes currency labels like `ks`, `kyat`, and `mmk` into `MMK`
- converts `quantity` and `unit_price` into numeric types
- calculates `revenue_mmk`
- creates daily and weekly summary tables

Revenue is calculated as:

```text
revenue_mmk = quantity * unit_price_mmk
```

The transform step produces three datasets:

- `cleaned_sales`
- `daily_revenue`
- `weekly_revenue`

### 3. Load

The cleaned and aggregated DataFrames are written into PostgreSQL.

The resulting tables are:

- `sales_cleaned`
- `revenue_daily`
- `revenue_weekly`

These tables are then used by the dashboard for analytics and visualization.

## Database View

```text
PostgreSQL
|
+-- sales_cleaned
|    one row = one cleaned sale
|    used for detailed analysis
|
+-- revenue_daily
|    one row = one day
|    used for daily KPI trends
|
+-- revenue_weekly
     one row = one week
     used for higher-level trend reporting
```

## Dashboard Output

The Streamlit app reads the PostgreSQL tables and displays:

- total revenue
- total orders
- average order value
- top region
- daily revenue trend
- weekly revenue trend
- revenue by region
- top products
- cleaned sales records

Important separation of responsibility:

The dashboard does not perform the ETL logic itself. It only reads the output that has already been prepared and loaded into PostgreSQL.

## Run Modes

### Manual ETL Run

```powershell
python run_pipeline.py
```

Use this when you want to refresh the database tables once.

### Scheduled ETL Run

```powershell
python -m pipeline.scheduler
```

Use this when you want the ETL to run automatically every few seconds based on the value in [`.env`](/C:/Users/HP/Documents/Myn_pipeline/.env).

### Dashboard Run

```powershell
streamlit run pipeline/dashboard.py
```

Use this when you want to open the web dashboard and inspect the KPIs and charts.

## Current Local Setup

This repository is currently configured for an existing local PostgreSQL installation.

That means:

- PostgreSQL should already be running on your machine
- [`.env`](/C:/Users/HP/Documents/Myn_pipeline/.env) should contain your real local PostgreSQL password
- Docker is not part of the active project setup

## Why The Structure Matters

The project is split into clear layers:

- configuration
- database connectivity
- ETL logic
- orchestration
- visualization

This structure makes the project easier to understand, maintain, and extend. It also mirrors how larger production data workflows are often organized.

## Learning Value

This project is useful for practicing:

- Python project organization
- environment-based configuration
- Pandas data cleaning and aggregation
- PostgreSQL integration with SQLAlchemy
- scheduled job execution
- Streamlit dashboard development

## Possible Future Improvements

Good next upgrades for this project would be:

1. Add logging instead of relying mainly on `print`
2. Add data quality checks and validation rules
3. Add unit tests for ETL functions
4. Support incremental loads instead of replacing tables
5. Add dashboard filters for region, category, or date
6. Replace the simple scheduler with Airflow
7. Add more analytics views for category and payment method performance

## Final Mental Model

```text
sales_data.csv -> ETL logic in etl.py -> PostgreSQL tables -> Streamlit dashboard
```

In one sentence:

This project takes raw Myanmar retail sales data, transforms it into useful business tables, stores it in PostgreSQL, and presents it through a dashboard.
