from flask import Response, json
from sonarqube.api.SonarqubeAPI import SonarqubeAPI
import sonarqube.utils.SonarqubeUtils as sq_utils

html_pages_path = "../resources/html_pages/"


class SonarqubeAPIExtended(SonarqubeAPI):
    def create_project(self, name, project_key):
        project = sq_utils.get_project("Name", name)

        static_dict = {"name": name, "key": project_key}

        total_files = project["TotalFiles"]
        project_size = project["ProjectSize"]
        project_numbers = total_files // project_size
        if (total_files % project_size) > 0:
            project_numbers += 1

        final_response = None
        for i in range(project_numbers):
            new_name = name + "_" + str(i + 1)
            new_project_key = project_key + "_" + str(i + 1)

            response = super().create_project(new_name, new_project_key)

            if response.status_code >= 300:
                return Response(SonarqubeAPI.get_json_content(response), status=response.status_code,
                                mimetype="application/json")

            final_response = response

        response_dict = SonarqubeAPI.get_json_content(final_response)
        response_dict["project"].update(static_dict)

        return Response(json.dumps(response_dict), status=final_response.status_code, mimetype="application/json")

    def delete_project(self, project_key):
        project = sq_utils.get_project("Key", project_key)

        total_files = project["TotalFiles"]
        project_size = project["ProjectSize"]
        project_numbers = (total_files // project_size) + 1

        error_msg_list = []
        for i in range(project_numbers):
            new_project_key = project_key + "_" + str(i + 1)
            response = super().delete_project(new_project_key)

            if response.status_code >= 400:
                error_msg_list.append(SonarqubeAPI.get_json_content(response)["errors"])

        if not error_msg_list:
            content = "Successfull"
            status_code = 200
        else:
            content = error_msg_list
            status_code = 400

        return Response(json.dumps(content), status=status_code, mimetype="application/json")

    def measures(self, project_key, metric_normalized, page_number=1):
        project = sq_utils.get_project("Key", project_key)

        total_files = project["TotalFiles"]
        project_size = project["ProjectSize"]
        project_numbers = (total_files // project_size) + 1

        total_files_analyzed = 0

        final_response_json = {}
        component_list = []

        missed_projects = []
        for i in range(project_numbers):
            new_project_key = project_key + "_" + str(i+1)
            response = super().measures(new_project_key, metric_normalized, page_number)
            response_json = SonarqubeAPI.get_json_content(response)

            if not response_json["components"]:
                actual_key_split = response_json["baseComponent"]["key"].split("_")
                missed_project = "".join(actual_key_split[len(actual_key_split) - 1:])
                missed_projects.append(missed_project)

            total_files_analyzed += response_json["paging"]["total"]
            final_response_json.update(response_json)

            component_list += response_json["components"]

        # Update
        final_response_json["paging"]["total"] = total_files_analyzed
        final_response_json["baseComponent"]["key"] = project_key
        final_response_json["baseComponent"]["name"] = project["Name"]
        final_response_json["components"] = component_list

        # Retrive the pages not analyzed
        missed_pages = []
        project_name = sq_utils.get_name(project_key)
        buffers = sq_utils.get_bufferlist(project_name)

        for missed_project in missed_projects:
            html_pages = buffers[str(missed_project)]
            missed_pages += html_pages

        final_response_json["projectNotAnalysed"] = missed_pages

        return Response(json.dumps(final_response_json), status=200, mimetype="application/json")

    def task_list(self, project_key):
        project = sq_utils.get_project("Key", project_key)

        total_files = project["TotalFiles"]
        project_size = project["ProjectSize"]

        project_numbers = total_files // project_size
        if (total_files % project_size) > 0:
            project_numbers += 1

        queues = []
        currents = []
        final_content = {}
        for i in range(project_numbers):
            new_project_key = project_key + "_" + str(i + 1)
            response = super().task_list(new_project_key)
            content = SonarqubeAPI.get_json_content(response)

            if "queue" in content:
                queues += content["queue"]
            if "current" in content:
                currents.append(content["current"])
            final_content = content

        final_content["queue"] = queues
        final_content["current"] = currents

        return Response(json.dumps(final_content), status=200, mimetype="application/json")
