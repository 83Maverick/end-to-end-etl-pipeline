
import pandas as pd


def transform_customers(
    customers: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = customers.copy()

    df["customer_name"] = df["customer_name"].fillna("").str.strip()
    df["email"] = df["email"].fillna("").str.strip()

    duplicate_id = df["customer_id"].duplicated(keep="first")
    missing_name = df["customer_name"].eq("")
    missing_email = df["email"].eq("")

    df["rejection_reason"] = ""

    df.loc[duplicate_id, "rejection_reason"] += "Duplicate customer_id; "
    df.loc[missing_name, "rejection_reason"] += "Missing customer_name; "
    df.loc[missing_email, "rejection_reason"] += "Missing email; "

    valid = df[df["rejection_reason"].eq("")].drop(
        columns=["rejection_reason"]
    )

    rejected = df[~df["rejection_reason"].eq("")].copy()

    return valid, rejected


def transform_orders(
    orders: pd.DataFrame,
    valid_customers: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = orders.copy()

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["order_date"] = pd.to_datetime(
        df["order_date"], errors="coerce"
    )

    duplicate_id = df["order_id"].duplicated(keep="first")
    invalid_amount = df["amount"].isna() | (df["amount"] <= 0)
    invalid_date = df["order_date"].isna()

    known_customer_ids = set(valid_customers["customer_id"])
    unknown_customer = ~df["customer_id"].isin(known_customer_ids)

    df["rejection_reason"] = ""

    df.loc[duplicate_id, "rejection_reason"] += "Duplicate order_id; "
    df.loc[invalid_amount, "rejection_reason"] += "Invalid amount; "
    df.loc[invalid_date, "rejection_reason"] += "Invalid order_date; "
    df.loc[unknown_customer, "rejection_reason"] += "Unknown customer_id; "

    valid = df[df["rejection_reason"].eq("")].drop(
        columns=["rejection_reason"]
    )

    rejected = df[~df["rejection_reason"].eq("")].copy()

    return valid, rejected


if __name__ == "__main__":
    from extract import extract_csv

    customers = extract_csv("customers.csv")
    orders = extract_csv("orders.csv")

    valid_customers, rejected_customers = transform_customers(customers)
    valid_orders, rejected_orders = transform_orders(
        orders, valid_customers
    )

    print("\nCustomer validation")
    print(f"Valid: {len(valid_customers)}")
    print(f"Rejected: {len(rejected_customers)}")
    print(rejected_customers[["customer_id", "rejection_reason"]])

    print("\nOrder validation")
    print(f"Valid: {len(valid_orders)}")
    print(f"Rejected: {len(rejected_orders)}")
    print(rejected_orders[["order_id", "rejection_reason"]])
