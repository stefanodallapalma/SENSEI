import time, datetime
from sonarqube.api.SonarqubeAPIExtended import SonarqubeAPIExtended
from utils.ListUtils import array_split

from exception.ServerError import ServerError
from exception.PendingTaskException import PendingTaskException

TIMEOUT = 600  # sec
LIMIT_METRICS_API = 15
MAX_ELEMENTS_FOR_PAGE = 100


class SonarqubeAnitaAPI:
    def __init__(self):
        self._sq_api = SonarqubeAPIExtended()

    @property
    def sq_api(self):
        return self._sq_api

    @sq_api.setter
    def sq_api(self, value):
        self._sq_api = value

    def metrics(self):
        """Get the list of all metrics available on Sonarqube"""
        response = self._sq_api.metrics()

        if response.status_code >= 400:
            content = SonarqubeAPIExtended.get_json_content(response)
            status_code = response.status_code
            error = {"msg": content, "status": status_code}
            raise ServerError(error)

        metrics = []

        content = SonarqubeAPIExtended.get_json_content(response)
        metrics_content = content["metrics"]

        for metric in metrics_content:
            metrics.append(metric["key"])

        return metrics

    def measures(self, project_key, metrics=None, wait=False):
        """Get the list of all elements of a project with their metrics"""
        if metrics is None:
            metrics = self.metrics()

        # Check if there are some pending tasks
        pending = self.check_pending_tasks(project_key)
        if wait:
            start_time = time.time()
            while pending and (time.time() - start_time) < TIMEOUT:
                time.sleep(3)
                pending = self.check_pending_tasks(project_key)

        if pending:
            raise PendingTaskException("Pending tasks. Impossible to retrieve metrics")

        # Remove from the metric list all metrics that cannot be processed by sonarqube
        error_metrics = self.get_error_metrics(project_key, metrics)
        # print("Error metrics: " + str(error_metrics))
        # print("--------------------------------------------------")
        metrics = [x for x in metrics if x not in error_metrics]

        # The api accepts only 15 metrics for call
        metrics_split = array_split(metrics, LIMIT_METRICS_API)

        html_list = []

        # Retrieve 15 metrics at time and add to the list of dict
        for metrics_15 in metrics_split:
            metrics_normalized = ",".join(metrics_15)
            response = self.sq_api.measures(project_key, metrics_normalized)

            number_html_pages = SonarqubeAPIExtended.get_json_content(response)["paging"]["total"]
            max_pages = number_of_pages(number_html_pages, MAX_ELEMENTS_FOR_PAGE)

            for x in range(max_pages):
                response = self.sq_api.measures(project_key, metrics_normalized, (x + 1))
                components = self.sq_api.get_json_content(response)["components"]

                for component in components:
                    metric_dict = metric_dict_template(metrics_15)

                    file_name = "".join(component["key"].split(":")[1:])
                    metric_dict["Name"] = file_name

                    # If there is a filename in the list, use the dict already stored instead of a new template
                    for index in range(len(html_list)):
                        if html_list[index]["Name"] == file_name:
                            metric_dict = html_list.pop(index)
                            break

                    metrics = component["measures"]
                    for metric in metrics:
                        if "value" in metric:
                            metric_dict[metric["metric"]] = metric["value"]
                        elif "periods" in metric:
                            metric_dict[metric["metric"]] = metric["periods"][0]["value"]

                    html_list.append(metric_dict)

        return html_list

    def check_pending_tasks(self, project_key):
        project_tasks = self._sq_api.tasks(project_key)
        project_tasks_content = SonarqubeAPIExtended.get_json_content(project_tasks)
        if "queue" in project_tasks_content:
            queues = project_tasks_content["queue"]
            for queue in queues:
                if queue["status"] != "SUCCESS":
                    return True

        return False

    def get_error_metrics(self, project_key, metrics):
        error_metrics = []
        for metric in metrics:
            response = self.sq_api.measures(project_key, metric)
            content = SonarqubeAPIExtended.get_json_content(response)

            if "errors" in content:
                error_metrics.append(metric)

        return error_metrics


# General methods: future refactoring
def number_of_pages(number_html_pages, html_for_page):
    q = number_html_pages // html_for_page
    r = number_html_pages % html_for_page

    number_of_pages = q
    if r > 0:
        number_of_pages += 1

    return number_of_pages


def metric_dict_template(metric_list):
    template = {}
    for metric in metric_list:
        template[metric] = None

    return template
