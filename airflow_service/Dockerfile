FROM apache/airflow:2.7.3-python3.10

COPY requirements-airflow.txt ./tmp/requirements-airflow.txt
COPY ./postgres_data ./tmp/postgres_data

RUN pip install -U pip
RUN pip install -r ./tmp/requirements-airflow.txt