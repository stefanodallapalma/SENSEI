from database.anita.controller.TableController import TableController
from database.anita.bean.SonarqubeBean import SonarqubeBean
from database.db.structure.ColumnDB import ColumnDB
from database.db.structure.DataType import DataType
from database.db.structure.Type import Type
from sonarqube.anita.SonarqubeAnitaAPI import SonarqubeAnitaAPI

TABLE_NAME = "sonarqube"


class SonarqubeController(TableController):
    def __init__(self):
        super().__init__(TABLE_NAME)

    def __init_columns(self):
        # Attributes
        attribute_names = SonarqubeBean.__prop__()
        pk_attribute_names = list(attribute_names)

        anita_sq_api = SonarqubeAnitaAPI()
        metrics = anita_sq_api.metrics()
        attribute_names += metrics

        columns = []
        for attribute_name in attribute_names:
            if attribute_name in pk_attribute_names:
                datatype = DataType(Type.VARCHAR, 50)
                column = ColumnDB(attribute_name, datatype, pk=True, not_null=True)
            else:
                datatype = DataType(Type.DOUBLE)
                column = ColumnDB(attribute_name, datatype)
            columns.append(column)

        self.columns = columns

    def select_by_project_name(self, project_name):
        param_dict = {"project_name": project_name}
        return self.select_by_params(param_dict)

    def delete_by_project_name(self, project_name):
        bean = SonarqubeBean(project_name=project_name)
        return self.delete_beans(bean)
