# End-to-End ETL Pipeline with Python and PostgreSQL

A portfolio project demonstrating an end-to-end Extract, Transform, and Load (ETL) pipeline using Python, Pandas, and PostgreSQL. The pipeline extracts data from CSV files, validates and transforms records, generates data quality reports, and loads valid data into a PostgreSQL database.

## Project Overview

This project simulates a small customer and order data processing workflow. It separates valid records from invalid records, records rejection reasons, and produces reconciliation summaries to help track data quality.

## Key Features

- **Data Extraction:** Read customer and order data from CSV files using Pandas.
- **Data Transformation:** Validate customer and order records and identify invalid data.
- **Data Quality Checks:** Handle missing customer information, duplicate IDs, invalid amounts, invalid dates, and orders referencing unknown customers.
- **Rejected Record Reports:** Export rejected customers and orders to CSV files with rejection reasons.
- **PostgreSQL Integration:** Load valid records into relational database tables using SQLAlchemy and Psycopg.
- **Duplicate-Safe Loading:** Use `ON CONFLICT DO NOTHING` to avoid inserting records with existing primary keys.
- **Logging and Error Handling:** Record pipeline execution details and errors in a log file.
- **Automated Testing:** Use Pytest to validate transformation and data-quality rules.
- **Environment Configuration:** Store database connection settings in a `.env` file.

## Technology Stack

- Python
- Pandas
- PostgreSQL
- SQLAlchemy
- Psycopg
- python-dotenv
- Pytest
- Git and GitHub

## Project Structure

```text
end-to-end-etl-pipeline/
├── data/
│   ├── customers.csv
│   └── orders.csv
├── logs/
├── reports/
├── sql/
├── src/
│   ├── db.py
│   ├── extract.py
│   ├── load.py
│   ├── logger_config.py
│   ├── report.py
│   └── transform.py
├── tests/
│   └── test_transform.py
├── .env
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

## ETL Workflow

```text
CSV Source Files
       |
       v
     Extract
       |
       v
    Transform
       |
       +----------------------+
       |                      |
       v                      v
 Valid Records          Rejected Records
       |                      |
       v                      v
 PostgreSQL Database    CSV Quality Reports
       |
       v
 Pipeline Logs and Summary
```

## Data Quality Rules

The pipeline checks customer and order data for common data-quality problems.

### Customers

- Reject records with missing customer names or email addresses.
- Reject duplicate customer IDs after the first occurrence.
- Clean string fields by trimming surrounding whitespace.

### Orders

- Reject duplicate order IDs after the first occurrence.
- Reject invalid or non-positive order amounts.
- Reject invalid order dates.
- Reject orders referencing customer IDs that do not exist in the valid customer dataset.

Rejected records include a `rejection_reason` field to explain why they failed validation.

## Prerequisites

Before running the project, install:

- Python 3.10 or newer
- PostgreSQL
- Git

You should also have access to a PostgreSQL database and permission to create tables.

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/83Maverick/end-to-end-etl-pipeline.git
cd end-to-end-etl-pipeline
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=etl_pipeline_db
DB_USER=postgres
DB_PASSWORD=your_local_password
```

Replace `your_local_password` with your local PostgreSQL password. Never commit your `.env` file or publish database credentials.

### 5. Create the database

Create a PostgreSQL database named `etl_pipeline_db`, or use another database and update `DB_NAME` accordingly.

Connect to the database in pgAdmin and execute:

```sql
CREATE TABLE IF NOT EXISTS public.customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    city VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS public.orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL
        REFERENCES public.customers(customer_id),
    order_date DATE NOT NULL,
    amount NUMERIC(12, 2) NOT NULL CHECK (amount > 0),
    status VARCHAR(30) NOT NULL
);
```

### 6. Run the pipeline

From the project root directory:

```powershell
python main.py
```

The pipeline extracts the CSV files, transforms the data, generates rejection reports, and loads valid records into PostgreSQL.

## Run Automated Tests

Execute the test suite with:

```powershell
python -m pytest -v
```

The current test suite contains five transformation tests covering missing customer information, non-positive order amounts, duplicate customer IDs, unknown customer references, and invalid order dates.

## Sample Data and Expected Results

The included sample CSV files contain five customer records and five order records.

| Dataset | Source Records | Valid Records | Rejected Records |
|---|---:|---:|---:|
| Customers | 5 | 4 | 1 |
| Orders | 5 | 3 | 2 |

These counts describe the included sample data. Database row counts may differ if the database already contains records.

## Output Files

After running the pipeline, check the following locations:

- `reports/rejected_customers.csv` — rejected customer records and reasons.
- `reports/rejected_orders.csv` — rejected order records and reasons.
- `logs/etl_pipeline.log` — execution logs and error details.

## Database Verification

Run these queries in pgAdmin to inspect the loaded data:

```sql
SELECT *
FROM public.customers
ORDER BY customer_id;

SELECT *
FROM public.orders
ORDER BY order_id;
```

## Design Notes

- Database credentials are loaded from environment variables.
- Database inserts are wrapped in a transaction so that a failed load can be rolled back.
- Existing primary keys are skipped using `ON CONFLICT DO NOTHING`.
- Rejected records are reported separately from valid records.
- The pipeline can be run repeatedly, but this implementation does not update existing records when their source values change.

## Future Improvements

- Add incremental ETL processing.
- Add database upsert logic for changed records.
- Introduce schema validation and stronger data-quality checks.
- Add integration tests for PostgreSQL loading.
- Add CI automation with GitHub Actions.
- Add pipeline metrics and monitoring.
- Containerize the application using Docker.

## Author

**83Maverick**

GitHub: https://github.com/83Maverick

---

*Built as a hands-on data engineering portfolio project to demonstrate ETL development, data validation, relational database integration, logging, and automated testing.*
