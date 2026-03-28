from sqlalchemy import create_engine, text

from pipeline.config import settings


def get_engine():
    return create_engine(settings.sqlalchemy_url, future=True)


def ensure_database_exists() -> None:
    admin_engine = create_engine(settings.admin_sqlalchemy_url, future=True, isolation_level="AUTOCOMMIT")
    with admin_engine.connect() as connection:
        exists = connection.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :database_name"),
            {"database_name": settings.postgres_db},
        ).scalar()
        if not exists:
            connection.execute(text(f'CREATE DATABASE "{settings.postgres_db}"'))


def ensure_database_ready(engine) -> None:
    ensure_database_exists()
    with engine.begin() as connection:
        connection.execute(text("SELECT 1"))
