# FastAPI Web-Service

Данная директория посвящена созданию и развертыванию приложения *FastAPI* и интеграции в него наших рекомендаций для возможности делать к нему запросы и получать рекомендации.

## Загрузка/обновление рекомендаций

Для работы сервиса необходимо для начала загрузить файлы с рекомендациями. Это можно сделать при помощи следующих команд из корневой директории (чтобы иметь доступ к последним версиям рекомендаций):

```bash
# Loading default recommendations from DB
python postgres_scripts load_table.py --table-name=default_recs

# Loading online recommendations from DB
python postgres_scripts load_table.py --table-name=online_recs

# Loading personal ranked recommendations from DB
python postgres_scripts load_table.py --table-name=candidates_ranked
```

Конфигурационный файл [`docker-compose.yaml`](./docker-compose.yaml) устроен так, что директория `recommendations` примонтирована к соответствующим контейнерам, таким образом файлы можно обновлять без необходимости пересборки образов. Тем не менее, в том случае, что файлы обновляются следует перезапустить сервисы, поскольку старые версии файлов уже загружены на сервер:

```bash
cd fastapi_service
docker compose restart
```

## Запуск сервисов

Приложение рекомендаций можно запустить следующим образом:

```bash
cd fastapi_service
docker compose up --build
```

После успешного запуска наши сервисы будут доступны на следующим портах:

* Main application => http://localhost:8000
* Offline recommendations service => http://localhost:8001
* Events service => http://localhost:8002
* Features service => http://localhost:8003
* Grafana => http://localhost:3000
* Prometheus => http://localhost:9090

Запуск каждого из первых четырех сервисов приложения был перенесен в свой *Dockerfile*, каждый из которых собирается после запуска команды выше. Дополнительные контейнеры Grafana и Prometheus здесь же используются и создаются в целях мониторинга метрик приложения.

## Тестирование сервиса

Мы можем также проверить работоспособность сервисов, запустив [следующий скрипт](./test_service.py) с основными тестами приложения:

```bash
python test_service.py
```

Результаты тестирования логируются в файл [`test_service.log`](./test_service.log). Дополнительно был создан скрипт [`simulate_service_load.py`](./simulate_service_load.py), который посылает ряд запросов в API с некоторой задержкой для проверки функционирования дашборда и метрик. Запускается так же:

```bash
python simulate_service_load.py
```

## Мониторинг приложения

Как уже упоминалось выше, для мониторинга используются Grafana и Prometheus. 

*Json*-файл дашборда можно посмотреть [тут](./dashboard.json), а для того чтобы увидеть сами визуализации метрик, необходимо сделать следующие шаги:

1. Запустить приложение через `docker compose up` (или `docker compose up --build`, если оно еще не собрано)
2. Идти на http://localhost:3000 для доступа к UI Grafana, где в Datasources нам нужно указать Prometheus и URL сервиса http://prometheus:9090
3. Запустить `python fix_datasource_uid.py`, что позволит использовать содержимое файла `dashboard.json` для показа
4. На вкладке Dashboards выбрать Import->New, где вставить содержимое файла для доступа к дашборду и всем отслеживаемым метрикам.

### Метрики мониторинга

Метрики, которые были выбраны для трэкинга работы приложения, разделяются на несколько групп:

* *Инфраструктурный слой*

    * **RAM Usage (MB)**
    * **CPU Usage change (%/min)**

* *Бизнес слой*

    * **Number of successful connections to online/offline recommendation services**
    * **Number of requests to personal recommendations**
    * **Number of requests to default recommendations**


* *Прикладной слой*

    * **Request duration change (%/min)**
    * **Scraping duration (seconds)**


## Остановка приложения

Для прекращения работы с приложением и сервисом, нужно остановить и удалить все контейнеры:

```bash
cd fastapi_service
docker compose down
```
