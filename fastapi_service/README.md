# FastAPI Web-Service

The current directory is dedicated to creating and deploying *FastAPI* application with an integration of the recommendations generated for being able to send requests to the API and obtain recommendations for a user.

## Loading/updating recommendations

For the web service to work, one needs to firstly load files with recommendations. This can be done by running the following commands from the root directory (in order to be able to have access to the latest versions of recommendations):

```bash
# Loading default recommendations from DB
python postgres_scripts/load_table.py --table-name=default_recs

# Loading online recommendations from DB
python postgres_scripts/load_table.py --table-name=online_recs

# Loading personal ranked recommendations from DB
python postgres_scripts/load_table.py --table-name=candidates_ranked
```

Configuration [`docker-compose.yaml`](./docker-compose.yaml) is created in such a way that `recommendations/` directory is mounted to the respective containers so that files could be updated without the necessity to re-build the images. Neverthless, in case of recommendations getting updated, one needs to restart the services, since the old recommendations have already been loaded to the server:

```bash
cd fastapi_service
docker compose restart
```

## Launching services

Recommendations application can be built in the following way:

```bash
cd fastapi_service
docker compose up --build
```

After successfully launching the applications, services will be accessible on the following ports:

* Main application => http://localhost:8000
* Offline recommendations service => http://localhost:8001
* Events service => http://localhost:8002
* Features service => http://localhost:8003
* Grafana => http://localhost:3000
* Prometheus => http://localhost:9090

Instructions for the launch of each of the first 4 services have been specified in their own *Dockerfile* where each service is built after running the above command, Additional containers (Grafana and Prometheus) are built here for monitoring the application metrics.

## Testing recommendation service

We can test the functionality of the application by running the [following script](./test_service.py) with basic tests:

```bash
python test_service.py
```

Testing results are logged to [`test_service.log`](./test_service.log). We have also additionally created [`simulate_service_load.py`](./simulate_service_load.py) script which sends a series of requests to the API with some delay for testing monitoring of metrics and dashboard:

```bash
python simulate_service_load.py
```

## Monitoring system

Grafana and Prometheus are used for the monitoring of the application's metrics. 

*Json*-file of the dashboard can be seen [here](./dashboard.json), while actually using the prepared dashboard is done in the following way: 

1. Launch application via `docker compose up` (or `docker compose up --build`, if the images have not been built yet)
2. Go to http://localhost:3000 for accessing Grafana UI, where in Datasources we specify Prometheus и its URL: http://prometheus:9090
3. Run `python fix_datasource_uid.py` in order to be able to use the contents of `dashboard.json` for importing the dashboard
4. Go to Dashboards->Import->New, where after pasting the contents of the dashboard file one gets access to the ready dashboard.

### Monitoring metrics

* *Infrastructure layer*

    * **RAM Usage (MB)**
    * **CPU Usage change (%/min)**

* *Business layer*

    * **Number of successful connections to online/offline recommendation services**
    * **Number of requests to personal recommendations**
    * **Number of requests to default recommendations**


* *Service layer*

    * **Request duration change (%/min)**
    * **Scraping duration (seconds)**


## Stopping the application

```bash
cd fastapi_service
docker compose down
```
