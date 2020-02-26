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

