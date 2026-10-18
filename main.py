
import logging

from src.extract import extract_csv
from src.transform import transform_customers, transform_orders
from src.report import save_rejected_records
from src.load import load_data
from src.logger_config import get_logger

logger = get_logger(__name__)


def run_pipeline():
    logger.info("=" * 20 + " ETL PIPELINE STARTED " + "=" * 20)

    try:
        logger.info("Step 1: Extracting CSV files")
        customers = extract_csv("customers.csv")
        orders = extract_csv("orders.csv")

        logger.info("Step 2: Transforming data")
        valid_customers, rejected_customers = transform_customers(
            customers
        )
        valid_orders, rejected_orders = transform_orders(
            orders, valid_customers
        )

        logger.info(
            "Customer counts | source=%s valid=%s rejected=%s",
            len(customers),
            len(valid_customers),
            len(rejected_customers),
        )
        logger.info(
            "Order counts | source=%s valid=%s rejected=%s",
            len(orders),
            len(valid_orders),
            len(rejected_orders),
        )

        logger.info("Step 3: Generating rejection reports")
        save_rejected_records(rejected_customers, rejected_orders)

        logger.info("Step 4: Loading data into PostgreSQL")
        load_data(valid_customers, valid_orders)

        logger.info("ETL PIPELINE COMPLETED SUCCESSFULLY")

    except Exception:
        logger.exception("ETL PIPELINE FAILED")
        raise


if __name__ == "__main__":
    run_pipeline()
