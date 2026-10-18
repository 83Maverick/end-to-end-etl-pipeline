
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def extract_csv(file_name: str) -> pd.DataFrame:
    """Read a CSV file and return its contents as a DataFrame."""
    file_path = DATA_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    df = pd.read_csv(file_path)

    print(f"Extracted {len(df)} rows from {file_name}")
    return df


if __name__ == "__main__":
    customers = extract_csv("customers.csv")
    orders = extract_csv("orders.csv")

    print("\nCustomers preview:")
    print(customers.head())

    print("\nOrders preview:")
    print(orders.head())
