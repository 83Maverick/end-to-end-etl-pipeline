
from sqlalchemy import text

from src.db import get_engine
from src.logger_config import get_logger

logger = get_logger(__name__)


def load_data(valid_customers, valid_orders):
    engine = get_engine()

    try:
        with engine.begin() as connection:
            if not valid_customers.empty:
                connection.execute(
                    text("""
                        INSERT INTO public.customers
                            (customer_id, customer_name, email, city)
                        VALUES
                            (:customer_id, :customer_name, :email, :city)
                        ON CONFLICT (customer_id) DO NOTHING
                    """),
                    valid_customers.to_dict(orient="records"),
                )

            if not valid_orders.empty:
                connection.execute(
                    text("""
                        INSERT INTO public.orders
                            (order_id, customer_id, order_date, amount, status)
                        VALUES
                            (:order_id, :customer_id, :order_date, :amount, :status)
                        ON CONFLICT (order_id) DO NOTHING
                    """),
                    valid_orders.to_dict(orient="records"),
                )

        logger.info(
            "Load completed | customers_processed=%s orders_processed=%s",
            len(valid_customers),
            len(valid_orders),
        )

    except Exception:
        logger.exception("Database load failed")
        raise

    finally:
        engine.dispose()
