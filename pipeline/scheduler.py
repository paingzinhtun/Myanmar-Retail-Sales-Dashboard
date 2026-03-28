import time

import schedule

from pipeline.config import settings
from pipeline.etl import run_pipeline


def scheduled_job() -> None:
    print("Running scheduled pipeline job...")
    cleaned_sales, daily_revenue, weekly_revenue = run_pipeline()
    print(
        "Pipeline completed:",
        f"{len(cleaned_sales)} cleaned rows,",
        f"{len(daily_revenue)} daily aggregates,",
        f"{len(weekly_revenue)} weekly aggregates",
    )


def main() -> None:
    interval_seconds = settings.scheduler_interval_seconds
    if interval_seconds <= 0:
        raise ValueError("SCHEDULER_INTERVAL_SECONDS must be greater than 0")

    schedule.every(interval_seconds).seconds.do(scheduled_job)

    print(f"Scheduler started. Running ETL every {interval_seconds} seconds.")
    scheduled_job()

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
