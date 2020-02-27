from database.anita.table.AnitaTable import AnitaTable
from database.anita.bean.SonarqubeBean import SonarqubeBean
from database.anita.controller.SonarqubeController import get_beans_from_db
from database.db.structure.ColumnDB import ColumnDB
from database.db.structure.DataType import DataType
from database.db.structure.Type import Type
from sonarqube.anita.SonarqubeAnitaAPI import SonarqubeAnitaAPI

TABLE_NAME = "sonarqube"


class SonarqubeTable(AnitaTable):
    def __init__(self):
        super().__init__(TABLE_NAME)
        self.init_attributes()

    def init_attributes(self):
        # Attributes
        attribute_names = SonarqubeBean.__prop__()
        attribute_names.remove("metrics")
        pk_attribute_names = list(attribute_names)

        anita_sq_api = SonarqubeAnitaAPI()
        metrics = anita_sq_api.metrics()
        attribute_names += metrics

        attributes = []
        for attribute_name in attribute_names:
            if attribute_name in pk_attribute_names:
                datatype = DataType(Type.VARCHAR, 50)
                attribute = ColumnDB(attribute_name, datatype, pk=True, not_null=True)
            else:
                datatype = DataType(Type.DOUBLE)
                attribute = ColumnDB(attribute_name, datatype)
            attributes.append(attribute)

        self.attributes = attributes

    def insert_values(self, values):
        attribute_names = [attribute.name for attribute in self.attributes]

        # Query generation
        insert_query = self.generate_insert_query(attribute_names)

        if type(values) is not list:
            values = [values]

        elements = []
        for value in values:
            elem = []
            for attribute_name in attribute_names:
                if attribute_name == "timestamp":
                    elem.append(value.timestamp)
                elif attribute_name == "project_name":
                    elem.append(value.project_name)
                elif attribute_name == "page":
                    elem.append(value.page)
                else:
                    metrics = value.metrics
                    key = attribute_name
                    if key in metrics:
                        elem.append(metrics[key])
                    else:
                        elem.append(None)
            elem = tuple(elem)
            elements.append(elem)

        self.mysql_db.insert(insert_query, elements)

    def delete_values(self, values):
        pass

    def select_by_project_name(self, project_name):
        select_query = "SELECT * FROM `" + self._database_name + "`.`" + self.table_name \
                + "` WHERE `project_name` = %s"

        value = (project_name,)

        header, results = self.select(select_query, value)
        return get_beans_from_db(header, results)

    def delete_by_project_name(self, project_name):
        delete_query = "DELETE FROM `" + self._database_name + "`.`" + self.table_name \
                       + "` WHERE `project_name` = %s"

        value = (project_name,)

        self.mysql_db.delete(delete_query, value)
