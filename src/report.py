
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"


def save_rejected_records(
    rejected_customers: pd.DataFrame,
    rejected_orders: pd.DataFrame,
) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    customers_path = REPORTS_DIR / "rejected_customers.csv"
    orders_path = REPORTS_DIR / "rejected_orders.csv"

    rejected_customers.to_csv(customers_path, index=False)
    rejected_orders.to_csv(orders_path, index=False)

    print(f"Customer rejection report: {customers_path}")
    print(f"Order rejection report: {orders_path}")


if __name__ == "__main__":
    from extract import extract_csv
    from transform import transform_customers, transform_orders

    customers = extract_csv("customers.csv")
    orders = extract_csv("orders.csv")

    valid_customers, rejected_customers = transform_customers(customers)
    valid_orders, rejected_orders = transform_orders(
        orders, valid_customers
    )

    save_rejected_records(rejected_customers, rejected_orders)

    print("\n--- Reconciliation Summary ---")
    print(f"Customers: source={len(customers)}, "
          f"valid={len(valid_customers)}, "
          f"rejected={len(rejected_customers)}")
    print(f"Orders: source={len(orders)}, "
          f"valid={len(valid_orders)}, "
          f"rejected={len(rejected_orders)}")
