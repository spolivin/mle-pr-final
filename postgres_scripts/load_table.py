import argparse
import os

from psycopg2.errors import UndefinedTable

from show_table import extract_table


# Creating script args
parser = argparse.ArgumentParser()
parser.add_argument(
    "-tn",
    "--table-name",
    help="Name of the table to be loaded",
)
parser.add_argument(
    "-sd",
    "--save-dir",
    help="Name of the directory where table will be saved",
    default="./fastapi_service/recommendations",
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


if __name__ == "__main__":

    try:
        extracted_table = extract_table(table_name=args.table_name)
    except UndefinedTable:
        print(f"Table '{args.table_name}' does not exist")
    else:
        load_path = f"{args.save_dir}/{args.table_name}.parquet"
        extracted_table.to_parquet(load_path)
        print(f"Table '{args.table_name}' is successfully loaded to '{load_path}'")
