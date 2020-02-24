import time, json
import sonar.SonarqubeAPIController as sq_api_controller
from utils.ListUtils import array_split
from database.anita.bean.QualityBean import QualityBean
from datetime import date

from exception import PendingTaskException

TIMEOUT = 600   # sec
LIMIT_METRICS_API = 15
MAX_ELEMENTS_FOR_PAGE = 100


def retrieve_metrics(project_key, metric_list=None, wait=False):
    if metric_list is None:
        metric_list = sq_api_controller.metric_list()

    print("Metric list")
    print(str(metric_list))

    # Check if there are some pending tasks
    pending = pending_tasks(project_key)
    if wait:
        start_time = time.time()
        while pending and (time.time() - start_time) < TIMEOUT:
            time.sleep(3)
            pending = pending_tasks(project_key)

    if pending:
        raise PendingTaskException()

    # The api accepts only 15 metrics for call
    sub_metric_lists = array_split(metric_list, LIMIT_METRICS_API)

    html_list = []

    # Retrieve 15 metrics at time and add to the list of dict
    for sub_metric_list in sub_metric_lists:
        metric_normalized = ",".join(sub_metric_list)
        response = sq_api_controller.measures(project_key, metric_normalized)

        number_html_pages = sq_api_controller.get_content(response)["paging"]["total"]
        max_pages = number_of_pages(number_html_pages, MAX_ELEMENTS_FOR_PAGE)

        print("Total html files: " + str(number_html_pages))
        print("Max pages: " + str(max_pages))

        for x in range(max_pages):
            response = sq_api_controller.measures(project_key, metric_normalized, (x + 1))
            components = sq_api_controller.get_content(response)["components"]

            for component in components:
                metric_dict = metrict_dict_template(metric_list)

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

    print("Dict size: " + str(len(html_list)))

    # Creation of QualityBean
    today = date.today()
    qualities = []
    for page in html_list:
        name = page["Name"]
        del page["Name"]
        quality = QualityBean(today, name, page)
        qualities.append(quality)

    return qualities


def pending_tasks(project_key):
    project_tasks = sq_api_controller.task_list(project_key)
    project_tasks_content = sq_api_controller.get_content(project_tasks)
    if "queue" in project_tasks_content:
        queues = project_tasks_content["queue"]
        for queue in queues:
            if queue["status"] != "SUCCESS":
                return True

    return False


def number_of_pages(number_html_pages, html_for_page):
    q = number_html_pages // html_for_page
    r = number_html_pages % html_for_page

    number_of_pages = q
    if r > 0:
        number_of_pages += 1

    return number_of_pages


def metrict_dict_template(metric_list):
    template = {}
    for metric in metric_list:
        template[metric] = None

    return template