import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def get_engine():
    required = ["DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD"]
    missing = [key for key in required if not os.getenv(key)]

    if missing:
        raise ValueError(f"Missing .env settings: {', '.join(missing)}")

    connection_url = URL.create(
        drivername="postgresql+psycopg",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.environ["DB_NAME"],
    )

    return create_engine(connection_url, pool_pre_ping=True)


if __name__ == "__main__":
    engine = get_engine()

    with engine.connect() as connection:
        result = connection.execute(text("SELECT current_database()"))
        print(f"Connected successfully to: {result.scalar()}")

    engine.dispose()
