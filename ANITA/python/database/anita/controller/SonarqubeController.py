from database.anita.controller.TableController import TableController
from database.anita.model.SonarqubeBean import SonarqubeBean
from database.db.structure.ColumnDB import ColumnDB
from database.db.structure.DataType import DataType
from database.db.structure.Type import Type
from sonarqube.anita.SonarqubeAnitaAPI import SonarqubeAnitaAPI

TABLE_NAME = "sonarqube"


class SonarqubeController(TableController):
    def __init__(self):
        super().__init__(TABLE_NAME)

        # Init attributes
        self.init_columns()

    def init_columns(self):
        # Attributes
        attribute_names = SonarqubeBean.__prop__()
        pk_attribute_names = ["timestamp", "project_name", "page"]
        label_attributes = ["label", "label_three"]
        bool_attributes = ["bitcoin", "deep_web"]

        anita_sq_api = SonarqubeAnitaAPI()
        metrics = anita_sq_api.metrics()
        attribute_names += metrics

        columns = []
        for attribute_name in attribute_names:
            if attribute_name in pk_attribute_names:
                datatype = DataType(Type.VARCHAR, 50)
                column = ColumnDB(attribute_name, datatype, pk=True, not_null=True)
            elif attribute_name in bool_attributes:
                datatype = DataType(Type.BIT, 1)
                column = ColumnDB(attribute_name, datatype)
            elif attribute_name in label_attributes:
                datatype = DataType(Type.VARCHAR, 50)
                column = ColumnDB(attribute_name, datatype)
            else:
                datatype = DataType(Type.DOUBLE)
                column = ColumnDB(attribute_name, datatype)
            columns.append(column)

        self.columns = columns

    def select_by_project_name(self, project_name):
        param_dict = {"project_name": project_name}
        return self.select_by_params(param_dict)

    def select_by_project_name_and_timestamp(self, project_name, timestamp):
        param_dict = {"project_name": project_name, "timestamp": timestamp}
        return self.select_by_params(param_dict)

    def select_last_inserted(self, project_name):
        param_dict = {"project_name": project_name}
        results = self.select_by_params(param_dict)

        last = []
        last_timestamp = 0
        for result in results:
            if result["timestamp"] >= last_timestamp:
                if result["timestamp"] > last_timestamp:
                    last_timestamp = results["timestamp"]
                    last.clear()
                last.append(result)

        return last

    def select_all_labelled(self):
        query = "SELECT * FROM `" + self._database_name + "`.`" + self.table_name + "` WHERE `label` IS NOT NULL"
        header, results = self.select(query)

        results_dict = []
        for result in results:
            result_dict = {}
            for i in range(len(header)):
                result_dict[header[i]] = result[i]
            results_dict.append(result_dict)

        return results_dict

    def select_all_not_labelled(self):
        query = "SELECT * FROM `" + self._database_name + "`.`" + self.table_name + "` WHERE `label` IS NULL"
        header, results = self.select(query)

        results_dict = []
        for result in results:
            result_dict = {}
            for i in range(len(header)):
                result_dict[header[i]] = result[i]
            results_dict.append(result_dict)

        return results_dict

    def add_labels(self, project_name, labels_dict):
        query = "UPDATE `" + self._database_name + "`.`" + self.table_name + \
                "` SET `label` = %s, `label_three` = %s WHERE `project_name` = %s AND `page` = %s"

        values = []
        for label_dict in labels_dict:
            value = (label_dict["label"], label_dict["label_three"], project_name, label_dict["page"])
            values.append(value)

        self.update(query, values)

    def delete_by_project_name(self, project_name):
        bean = SonarqubeBean(project_name=project_name)
        return self.delete_beans(bean)

