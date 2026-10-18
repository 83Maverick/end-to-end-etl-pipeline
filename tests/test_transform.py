
import pandas as pd

from src.transform import transform_customers, transform_orders


def test_transform_customers_rejects_missing_name():
    customers = pd.DataFrame([
        {
            "customer_id": 101,
            "customer_name": "Amit Sharma",
            "email": "amit@example.com",
            "city": "Mumbai",
        },
        {
            "customer_id": 102,
            "customer_name": None,
            "email": "missing@example.com",
            "city": "Pune",
        },
    ])

    valid, rejected = transform_customers(customers)

    assert len(valid) == 1
    assert len(rejected) == 1
    assert rejected.iloc[0]["customer_id"] == 102


def test_transform_orders_rejects_non_positive_amount():
    customers = pd.DataFrame([
        {
            "customer_id": 101,
            "customer_name": "Amit Sharma",
            "email": "amit@example.com",
            "city": "Mumbai",
        }
    ])

    valid_customers, _ = transform_customers(customers)

    orders = pd.DataFrame([
        {
            "order_id": 1001,
            "customer_id": 101,
            "order_date": "2026-10-01",
            "amount": 2500,
            "status": "Completed",
        },
        {
            "order_id": 1002,
            "customer_id": 101,
            "order_date": "2026-10-02",
            "amount": 0,
            "status": "Pending",
        },
    ])

    valid, rejected = transform_orders(orders, valid_customers)

    assert len(valid) == 1
    assert len(rejected) == 1
    assert rejected.iloc[0]["order_id"] == 1002

def test_transform_customers_rejects_duplicate_ids():
    customers = pd.DataFrame([
        {
            "customer_id": 101,
            "customer_name": "Amit Sharma",
            "email": "amit@example.com",
            "city": "Mumbai",
        },
        {
            "customer_id": 101,
            "customer_name": "Amit Sharma Duplicate",
            "email": "amit2@example.com",
            "city": "Pune",
        },
    ])

    valid, rejected = transform_customers(customers)

    assert len(valid) == 1
    assert len(rejected) == 1


def test_transform_orders_rejects_unknown_customer():
    customers = pd.DataFrame([
        {
            "customer_id": 101,
            "customer_name": "Amit Sharma",
            "email": "amit@example.com",
            "city": "Mumbai",
        }
    ])

    valid_customers, _ = transform_customers(customers)

    orders = pd.DataFrame([
        {
            "order_id": 1001,
            "customer_id": 999,
            "order_date": "2026-10-05",
            "amount": 1500,
            "status": "Completed",
        }
    ])

    valid, rejected = transform_orders(orders, valid_customers)

    assert len(valid) == 0
    assert len(rejected) == 1


def test_transform_orders_rejects_invalid_date():
    customers = pd.DataFrame([
        {
            "customer_id": 101,
            "customer_name": "Amit Sharma",
            "email": "amit@example.com",
            "city": "Mumbai",
        }
    ])

    valid_customers, _ = transform_customers(customers)

    orders = pd.DataFrame([
        {
            "order_id": 1001,
            "customer_id": 101,
            "order_date": "not-a-date",
            "amount": 1500,
            "status": "Completed",
        }
    ])

    valid, rejected = transform_orders(orders, valid_customers)

    assert len(valid) == 0
    assert len(rejected) == 1
