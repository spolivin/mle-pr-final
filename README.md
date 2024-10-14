# Recommendation system in e-commerce

## Objective

The purpose of this repository is to build a recommendation system of goods for users as well as deploy it in the production environment and support it via various frameworks and services.


## Metrics

The task which we are going to solve for fulfilling the project objective is optimizing the system of recommendations for users' actions of adding the goods to the cart via maximization of the following metrics:

* `precision@10`
* `recall@10`

The choice of such metrics can be explained by their popularity of usage for evaluating the quality of recommendation systems as well as by the fact that in this case our focus will be upon relevance of recommendations for users and such metrics enable mathematically calculating it. It is logical that users will only see a part of the recommendations we generate for them so in this project we are going to consider the first 10 recommendations while computing metric values and hence making a decision about the quality of the recommendation system.

`precision@10` metric will allow us to say whether a recommended item is liked by a user, whilst by `recall@10` metric we will be able to judge about the ability of the system to detect and anticipate users' preferences.

## Project structure

Project is divided into several blocks where each one is described in the table below:

| Component | Description | Frameworks | Link    |
| :---   | :--- | :---: | :---: |
| **Modeling experiments** | Deploying *Mlflow* service with the artifact store and building/optimization of the goods recommendation system | `mlflow` `catboost` `implicit` `sklearn`| [recsys](./recsys/) |
| **Pipelines** | Deploying multi-container *Airflow* service in *Docker* environment and creating pipelines of data loading and re-training of the model | `docker` `docker-compose` `airflow` `catboost` | [airflow_service](./airflow_service/) |
| **Web-service deployment** | Deploying *FastAPI* service of recommendations in the *Docker* environment with an additonal monitoring system via *Prometheus* and *Grafana* | `docker` `docker-compose` `fastapi` `prometheus` `grafana` `requests`| [fastapi_service](./fastapi_service/) |

By accessing each link in the last column of the table, one can access the respective directory with a detailed description in the respective `README`.

## Additional toolbox

This repository is also equipped with additional tools for working with *S3* cloud storage and *PostgreSQL* database where each has a dedicated folder with useful scripts:

| Component | Description | Frameworks | Link    |
| :---   | :--- | :---: | :---: |
| **S3 Object Storage** | Compilation of scripts for pushing files to cloud as well as checking the contents/space in *S3*-bucket | `boto3` | [s3_scripts](./s3_scripts/) |
| **PostgreSQL** | Compilation of scripts for dropping, loading and inspecting tables from *Postgres* | `psycopg2` | [postgres_scripts](./postgres_scripts/) |

### Interacting with S3

Folder [s3_scripts](./s3_scripts/) contains scripts for convenient interaction with cloud storage. The present version contains the most basic ones:

1. **Inspecting *S3*-bucket contents/space**

```bash
python s3_scripts/check_storage.py --option=contents
```

```bash
python s3_scripts/check_storage.py --option=space
```

2. **Pushing files to S3**

```bash
python s3_scripts/push_file.py --local-file-path=data/test.parquet --s3-file-path=recsys/test/test.parquet
```

>Note: In this case one needs to specify the full path to a file in the local directory and the desired path to this file in the cloud storage

### Interacting with Postgres

1. **Inspecting table**

```bash
python postgres_scripts/show_table.py --table-name=<table_name>
```

2. **Loading/saving Postgres table locally**

```bash
python postgres_scripts/load_table.py --save-dir=<save_dir> --table-name=<table_name>
```

>Note: Upon running the script from the root directory there is no need to specify `--save-dir`, as the required table will be loaded to the needed folder in accordance with the default path

3. **Dropping Postgres table**

```bash
python postgres_scripts/drop_table.py --table-name=<table_name>
```
