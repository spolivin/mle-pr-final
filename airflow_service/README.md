# Pipelines

This directory is dedicated to running *Airflow* service and execution of *DAG*s. 

## Directory structure

| Element | Description |
| :---   | :--- |
| [`config`](./config/)| *Airflow* configuration files|
| [`dags`](./dags/)| Scripts for launching *Airflow* graphs |
| [`logs`](./logs/)| Logs with *DAG* launches results |
| [`plugins`](./plugins/)| Additional modules for running graphs |
| [`Dockerfile`](./Dockerfile)| Custom *Dockerfile* |
| [`docker-compose.yaml`](./docker-compose.yaml)| File with instructions on launching services in containers |
| [`requirements-airflow.txt`](./requirements-airflow.txt)| Dependencies for launching *Airflow* services |
| [`postgres_data`](./postgres_data/)| Data to be loaded into the database, obtained during experiments/modeling stage |

## Airflow service

We have created several folders for launching *Airflow* services:

* `config` => Storing custom configs
* `dags` => Storing graphs
* `logs` => Storing service logs
* `plugins` => Storing additional modules for running *DAG*s

*Airflow* developers have prepared a set of instructions for launching the services, one of which is [`docker-compose.yaml`](./docker-compose.yaml) file which has been downloaded via the following command:

```bash
curl -LfO https://airflow.apache.org/docs/apache-airflow/2.7.3/docker-compose.yaml
```

Since we are going to extend the image from `docker-compose.yaml`, we have also added our custom [`Dockerfile`](./Dockerfile) which is used for building the image.

>Note: For the adequate functioning of the service, one needs to comment out line 53 and remove comment from line 54 in [`docker-compose.yaml`](./docker-compose.yaml) for extending the image

### Launching services

1. **Saving VM's ID**

```bash
echo -e "\nAIRFLOW_UID=$(id -u)" >> .env
```
2. **Creating the account with a login and password**

```bash
cd airflow_service
docker compose up airflow-init
```

3. **Cleaning cache after Step 2**

```bash
docker compose down --volumes --remove-orphans
```

4. **Launch**

```bash
docker compose up --build
```

### DAGs

[`dags`](./dags/) folder contains different graphs with the set periods of runs:

| DAG | Purpose | Schedule (CRON) | Schedule (Periodicity) |
| :---   | :--- | :--- | :--- |
| [`load_default_recs.py`](./dags/load_default_recs.py)| Loading default recommendations to Postgres | *5 21 * * 6* | Every Saturday at 21:05 |
| [`load_online_recs.py`](./dags/load_online_recs.py)| Loading online recommendations to Postgres | *5 21 * * 6* | Every Saturday at 21:05 |
| [`load_candidates_train.py`](./dags/load_candidates_train.py)| Loading training recommendations to Postgres | *10 21 * * 6* | Every Saturday at 21:10 |
| [`load_candidates_inference.py`](./dags/load_candidates_inference.py)| Loading test recommendations to Postgres | *10 21 * * 6* | Every Saturday at 21:10 |
| [`load_candidates_ranked.py`](./dags/load_candidates_ranked.py)| Training the model on training recommendations and ranking test recommendations | *15 21 * * 6* | Every Saturday at 21:15 |

In other words, we have come up with a weekly schedule of *DAG*-runs:

* **Saturday 21:05** => New default and online recommendations are loaded to the database;
* **Saturday 21:10** => Loading of recommendations for training a ranking model as well as test recommendations which are to be ranked;
* **Saturday 21:15** => Model is re-trained on new training recommendations and then this information is used for ranking test recommendations where are then also loaded to Postgres.

### Plugins 

There is an additional`plugins` directory with [`steps`](./plugins/steps) folder containing modules describing pipelines steps:

| DAG | Purpose |
| :---   | :--- |
| [`default_recs.py`](./plugins/steps/default_recs.py)| Loading default recommendations to Postgres |
| [`online_recs.py`](./plugins/steps/online_recs.py)| Loading online recommendations to Postgres |
| [`training_data.py`](./plugins/steps/training_data.py)| Loading training recommendations to Postgres |
| [`inference_data.py`](./plugins/steps/inference_data.py)| Loading test recommendations to Postgres |
| [`ranked_data.py`](./plugins/steps/ranked_data.py)| Training the model on training recommendations and ranking test recommendations |
| [`messages.py`](./plugins/steps/messages.py)| Callbacks for sending messages about the execution process of *DAG*s to *Telegram* in case of success or failure |

Thus, as a result of running the graphs, the data loaded after executing the code in [notebook](../recsys/recommendation_system.ipynb) are sent to Postgres database where after successfully running `load_candidates_ranked.py` graph, we receive personal recommendations to be used in web service.

The next step is to load the recommendations data from the database to [web service folder](../fastapi_service/), where all 3 types of recommendations will be used during sending requests to the API.

## Stopping services

```bash
cd airflow_service
docker compose down
```
