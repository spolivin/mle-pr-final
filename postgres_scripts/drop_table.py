import argparse
import os

import psycopg2 as psycopg
from psycopg2.errors import UndefinedTable


# Creating script args
parser = argparse.ArgumentParser()
parser.add_argument(
    "-tn",
    "--table-name",
    help="Name of the table to be deleted",
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


def drop_table(table_name: str, connection: dict[str, str] = connection) -> None:
    """Drops a table from Postgres DB."""
    with psycopg.connect(**connection) as conn:
        with conn.cursor() as cur:
            cur.execute(f"DROP TABLE {table_name}")


if __name__ == "__main__":
    try:
        drop_table(table_name=args.table_name)
    except UndefinedTable:
        print(f"Table '{args.table_name}' does not exist")
    else:
        print(f"Table '{args.table_name}' has been dropped successfully")
