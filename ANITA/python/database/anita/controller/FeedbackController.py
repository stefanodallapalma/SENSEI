from ..controller.TableController import TableController
from ...db.structure.ColumnDB import ColumnDB
from ...db.structure.DataType import DataType
from ...db.structure.Type import Type
from ..model.market_models import Feedback

TABLE_NAME = "feedback"


class FeedbackController(TableController):
    def __init__(self):
        super().__init__(TABLE_NAME)

        # Init attributes
        self.init_columns()

    def init_columns(self):
        columns = []

        # ID Feebback
        datatype = DataType(Type.INT)
        columns.append(ColumnDB("id_feedback", datatype, pk=True, not_null=True, auto_increment=True))

        # ID content (vendor / product)
        datatype = DataType(Type.INT)
        columns.append(ColumnDB("id", datatype, not_null=True))

        # Score
        datatype = DataType(Type.VARCHAR, 100)
        columns.append(ColumnDB("score", datatype))

        # Message
        datatype = DataType(Type.VARCHAR, 5000)
        columns.append(ColumnDB("message", datatype))

        # Date
        datatype = DataType(Type.VARCHAR, 100)
        columns.append(ColumnDB("date", datatype))

        # Product
        datatype = DataType(Type.VARCHAR, 200)
        columns.append(ColumnDB("product", datatype))

        # User
        datatype = DataType(Type.VARCHAR, 100)
        columns.append(ColumnDB("user", datatype))

        # Deals
        datatype = DataType(Type.VARCHAR, 100)
        columns.append(ColumnDB("deals", datatype))

        self.columns = columns

    def get_feedback_list(self):
        query = "SELECT * FROM {1}.{0}" \
            .format(TABLE_NAME, self.db_name)

        header, results = self.mysql_db.search(query)

        feedback_list = []
        for result in results:
            feedback = Feedback()
            for i in range(len(header)):
                attribute = header[i]
                value = result[i]

                setattr(feedback, attribute, value)
            feedback_list.append(feedback)

        return feedback_list

    def get_feedback(self, id):
        query = "SELECT * FROM {0}.{1} WHERE {1}.id = %s".format(self.db_name, TABLE_NAME)
        values = (id,)

        header, results = self.mysql_db.search(query, values)

        feedback_list = []
        for result in results:
            feedback = {}
            for i in range(len(header)):
                attribute = header[i]
                value = result[i]
                if attribute != "id" and attribute != "id_feedback":
                    feedback[attribute] = value
            feedback_list.append(feedback)

        return feedback_list

    def get_last_feedback_id(self):
        query = "SELECT DISTINCT {0}.id FROM {1}.{0} ORDER BY {0}.id DESC" \
            .format(TABLE_NAME, self.db_name)

        header, results = self.mysql_db.search(query)

        if not results:
            return None
        else:
            return results[0][0]

    def insert_beans(self, beans):
        attributes = ["id", "score", "message", "date", "product", "user", "deals"]

        # Preprocessing
        new_beans = []
        for bean in beans:
            for attr in attributes:
                val = getattr(bean, attr)
                if isinstance(val, list):
                    val = ", ".join(str(elem) for elem in val)
                    setattr(bean, attr, val)
            new_beans.append(bean)

        super(FeedbackController, self).insert_beans(new_beans)