import argparse
import os

import pandas as pd
import psycopg2 as psycopg
from psycopg2.errors import UndefinedTable


# Creating script args
parser = argparse.ArgumentParser()
parser.add_argument(
    "-tn",
    "--table-name",
    help="Name of the table to be shown",
)
args = parser.parse_args()

# Setting DB connection parameters
connection = {"sslmode": "require", "target_session_attrs": "read-write"}
postgres_credentials = {
    "host": os.getenv("DB_DESTINATION_HOST"),
    "port": os.getenv("DB_DESTINATION_PORT"),
    "dbname": os.getenv("DB_DESTINATION_NAME"),
    "user": os.getenv("DB_DESTINATION_USER"),
    "password": os.getenv("DB_DESTINATION_PASSWORD"),
}
connection.update(postgres_credentials)


def extract_table(
    table_name: str, connection: dict[str, str] = connection
) -> pd.DataFrame:
    """Loads a table from Postgres and saves it as a DataFrame."""
    with psycopg.connect(**connection) as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {table_name}")
            data = cur.fetchall()
            columns = [col[0] for col in cur.description]

    # Transforming extracted data to DataFrame
    extracted_table = pd.DataFrame(data, columns=columns)

    return extracted_table


if __name__ == "__main__":
    try:
        # Loading table from the DB
        data = extract_table(table_name=args.table_name)
    except UndefinedTable:
        print(f"Table '{args.table_name}' does not exist")
    else:
        # Showing the table contents
        print(data)
