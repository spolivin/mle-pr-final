import json
import os
from typing import Any, Dict, Union, List

import requests
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("GRAFANA_USER")
password = os.getenv("GRAFANA_PASS")
path_dashboard_json = "dashboard.json"

print(f"grafana user: {username}")
print(f"grafana password: {password}")
# URL for Grafana API with user-password authorization
url = "http://{username}:{password}@localhost:3000/api/datasources/1"

# Getting data about prometheus datasource
auth_response = requests.get(url.format(username=username, password=password))
# Response example:
# {"id":1,"uid":"edn9q01pibn5sd","orgId":1,"name":"prometheus","type":"prometheus","typeLogoUrl":"public/app/plugins/datasource/prometheus/img/prometheus_logo.svg","access":"proxy","url":"http://prometheus:9090/","user":"","database":"","basicAuth":false,"basicAuthUser":"","withCredentials":false,"isDefault":true,"jsonData":{"httpMethod":"POST"},"secureJsonFields":{},"version":4,"readOnly":false}
prom_datasource = auth_response.json()
# Getting uid from the connected datasource
current_uid = prom_datasource["uid"]

# Loading dashboard as a dict
with open(path_dashboard_json, "r") as fd:
    dashboard = json.load(fd)
print("current uid: {}".format(current_uid))


def substitution_datasource_uid(
    dashboard: Union[List[Any], Dict[str, Any], Any], current_uid
) -> None:
    """
    Recusively replaces uid datasource prometheus in a dict.
    """

    if isinstance(dashboard, dict):
        for k, v in dashboard.items():
            if k == "datasource":
                if v["type"] == "prometheus":
                    v["uid"] = current_uid
            else:
                substitution_datasource_uid(v, current_uid)
    elif isinstance(dashboard, list):
        for elem in dashboard:
            substitution_datasource_uid(elem, current_uid)
    else:
        return


# Replacing uid
substitution_datasource_uid(dashboard, current_uid)
print("Fix uid done")

# Rewriting dashboard file
with open(path_dashboard_json, "w") as fd:
    json.dump(dashboard, fd, indent=2)
