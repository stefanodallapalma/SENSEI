import requests

metrics_url = "/api/measures/component_tree"

def retrieve_metrics(url, metric_list, project_key):
    request_url = url + metrics_url
    params = {"metricKeys":metric_list, "baseComponentKey":project_key}

    response = requests.get()
