# Modeling experiments

This directory is dedicated to conducting Exploratory Data Analysis (EDA) with a subsequent launch of a number of experiments in *MLflow* environment with artifact store.

## Directory structure

| Element | Description |
| :---   | :--- |
| [`recommendation_system.ipynb`](./recommendation_system.ipynb)| Jupyter notebook with the EDA and launched experiments |
| [`assets`](./assets/)| Folder with artifacts logged in *MLflow* |
| [`model_comparison`](./model_comparison/)| Visualizations of different ranking models comparisons |
| [`run_jupyter_server.sh`](./run_jupyter_server.sh)| Script for launching *Jupyter* server |
| [`run_mlflow_server.sh`](./run_mlflow_server.sh)| Script for launching *Mlflow* service with the artifact store |

A part of the artifacts is saved in [assets](./assets/) directory, while the other one represents data in `parquet` format that are not tracked by *Git* for saving up on the space taken up by the repository.

## Virtual environment

Before running the code in the Jupyter Notebook, one needs to create a virtual environment with the following commands from the root directory:

```bash
# Preparing virtual env
sudo apt-get update
sudo apt-get install python3.10-venv
python3.10 -m venv .venv_recsys
source .venv_recsys/bin/activate
pip install -r requirements.txt
```

## Launching *Mlflow* service

```bash
cd recsys
sh run_mlflow_server.sh
```

>Note: Upon successful launch, the service will be accessible at http://localhost:5000

## Launching *Jupyter* server

```bash
cd recsys
sh run_jupyter_server.sh
```

>Note: Upon successful launch, the server will be accessible at http://localhost:8888

## Saving recommendations and candidates for modeling

During the code execution from the notebook, the following data files will be created:

* `top_popular.parquet` => Top-100 items (default recommendations)
* `similar.parquet` => Similar items (online recommendations)
* `candidates_train.parquet` => Candidates (recommendations) for training a ranking model
* `candidates_inference.parquet` => Candidates for ranking
* `catboost_model.cmb` => The best catboost model according to metrics

> Note: These files are not tracked and thus are not visible in the repository

Files will be saved in [postgres_data](../airflow_service/postgres_data/) directory from where they will be loaded to Postgres database via executing *DAG*s and then be used either for re-training of a ranking model or for the web service. This step is introduced for the purpose of not only storing the data in *S3* but also in the database from where the data will be loaded for other tasks.
