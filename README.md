# Myanmar Retail Sales Pipeline

This project is a small end-to-end data pipeline for a simulated Myanmar retail shop. It reads sales data from a CSV file, transforms it with Pandas, loads the results into PostgreSQL, supports scheduled runs with Python, and visualizes KPIs in Streamlit.

For a deeper explanation of how the project works, see [README_GUIDE.md](/C:/Users/HP/Documents/Myn_pipeline/README_GUIDE.md).
For example outputs and presentation-ready samples, see [SAMPLE_OUTPUT.md](/C:/Users/HP/Documents/Myn_pipeline/SAMPLE_OUTPUT.md).

## Features

- Extract sales data from a CSV source
- Clean nulls and standardize currency values into MMK
- Compute detailed, daily, and weekly revenue metrics
- Load processed tables into PostgreSQL
- Run the ETL manually or on a schedule
- Display business KPIs and trends in a Streamlit dashboard

## Project Structure

```text
.
|-- data/
|   `-- raw/sales_data.csv
|-- pipeline/
|   |-- __init__.py
|   |-- config.py
|   |-- dashboard.py
|   |-- database.py
|   |-- etl.py
|   `-- scheduler.py
|-- .env.example
|-- .gitignore
|-- README.md
|-- README_GUIDE.md
|-- requirements.txt
`-- run_pipeline.py
```

## Requirements

- Python 3.12 or compatible
- A running local PostgreSQL instance
- Valid PostgreSQL credentials in [`.env`](/C:/Users/HP/Documents/Myn_pipeline/.env)

## Quick Start

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Create your environment file:

```powershell
Copy-Item .env.example .env
```

4. Update [`.env`](/C:/Users/HP/Documents/Myn_pipeline/.env) with your real local PostgreSQL password.

5. Run the pipeline once:

```powershell
python run_pipeline.py
```

6. Launch the dashboard:

```powershell
streamlit run pipeline/dashboard.py
```

## Scheduler

To run the ETL automatically every 60 seconds:

```powershell
python -m pipeline.scheduler
```

The schedule is controlled by `SCHEDULER_INTERVAL_SECONDS` in [`.env`](/C:/Users/HP/Documents/Myn_pipeline/.env). The default is `60`.

## Output Tables

The pipeline loads these tables into PostgreSQL:

- `sales_cleaned`
- `revenue_daily`
- `revenue_weekly`

## Current Setup

This repository is currently configured for an existing local PostgreSQL installation. Docker is not part of the active setup.

## Notes

- Revenue is standardized into `MMK`
- The sample CSV includes a few nulls and inconsistent currency labels for cleaning practice
- The scheduler is intentionally simple so it can be replaced later with Airflow or another orchestrator
