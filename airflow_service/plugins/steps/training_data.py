import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook
from sqlalchemy import (
    Column,
    Float,
    BigInteger,
    MetaData,
    Table,
    UniqueConstraint,
    inspect,
    Integer,
)

CANDIDATES_TRAIN_PATH = "./tmp/postgres_data/candidates_train.parquet"


def create_table():
    """Initializes the table in the database."""

    # Instantiating a PostgreSQL hook
    postgres_hook = PostgresHook("destination_db")

    # Retrieving the connection object
    db_conn = postgres_hook.get_sqlalchemy_engine()

    # Instantiating metadata object
    metadata = MetaData()

    # Creating the table
    candidates_train_table = Table(
        "candidates_train",
        metadata,
        Column("id", BigInteger, primary_key=True, autoincrement=True),
        Column("rec_id", BigInteger),
        Column("user_id", BigInteger),
        Column("item_id", BigInteger),
        Column("als_score", Float),
        Column("target", Integer),
        Column("category_id", Integer),
        Column("parent_id", Integer),
        Column("available", Integer),
        UniqueConstraint("rec_id", name="unique_rec_id_5_constraint"),
    )

    # Checking the existence of table in DB and adding a new table (if needed)
    if not inspect(db_conn).has_table(candidates_train_table.name):
        metadata.create_all(db_conn)


def extract(**kwargs):
    """Loads training data from file."""

    data = pd.read_parquet(CANDIDATES_TRAIN_PATH)

    # Pushing the extracted data to the next task
    ti = kwargs["ti"]
    ti.xcom_push("extracted_data", data)


def load(**kwargs):
    """Loads the extracted data to the database."""

    postgres_hook = PostgresHook("destination_db")

    # Pulling the data from the previous task
    ti = kwargs["ti"]
    data = ti.xcom_pull(task_ids="extract", key="extracted_data")

    # Inserting data into a new table
    postgres_hook.insert_rows(
        table="candidates_train",
        replace=True,
        target_fields=data.columns.tolist(),
        replace_index=["rec_id"],
        rows=data.values.tolist(),
    )
