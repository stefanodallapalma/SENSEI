from datetime import datetime
from database.anita.bean.SonarqubeBean import SonarqubeBean


def get_beans(project_name, metrics):
    sonarqube_beans = []

    timestamp = int(datetime.now().timestamp())
    for metric in metrics:
        name = metric["Name"]

        tmp_metrics = metric
        del tmp_metrics["Name"]

        sonarqube_bean = SonarqubeBean(timestamp, project_name, name, tmp_metrics)
        sonarqube_beans.append(sonarqube_bean)

    return sonarqube_beans


def get_bean(project_name, metric):
    metrics = [metric]
    sonarqube_beans = get_beans(project_name, metrics)
    return sonarqube_beans[0]


def get_beans_from_db(parameters, values):
    sonarqube_pages = []

    for value in values:
        timestamp = None
        project_name = None
        page = None
        metrics = {}

        for i in range(len(parameters)):
            if parameters[i] == "timestamp":
                timestamp = value[i]
            elif parameters[i] == "project_name":
                project_name = value[i]
            elif parameters[i] == "page":
                page = value[i]
            else:
                metrics[parameters[i]] = value[i]

        sonarqube_page = SonarqubeBean(timestamp, project_name, page, metrics)
        sonarqube_pages.append(sonarqube_page)

    return sonarqube_pages


def get_bean_from_db(parameters, value):
    values = [value]
    sonarqube_beans = get_beans_from_db(parameters, values)
    return sonarqube_beans[0]