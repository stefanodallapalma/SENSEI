from ..controller.TableController import TableController
from ...db.structure.ColumnDB import ColumnDB
from ...db.structure.DataType import DataType
from ...db.structure.Type import Type

TABLE_NAME = "feedback"


class FeedbackController(TableController):
    def __init__(self):
        super().__init__(TABLE_NAME)

        # Init attributes
        self.init_columns()

    def init_columns(self):
        columns = []

        # Type
        datatype = DataType(Type.VARCHAR, 10)
        columns.append(ColumnDB("type", datatype, pk=True, not_null=True))

        # Timestamp
        datatype = DataType(Type.VARCHAR, 50)
        columns.append(ColumnDB("timestamp", datatype, pk=True, not_null=True))

        # Market
        datatype = DataType(Type.VARCHAR, 50)
        columns.append(ColumnDB("market", datatype, pk=True, not_null=True))

        # Feedback
        datatype = DataType(Type.VARCHAR, 10)
        columns.append(ColumnDB("feedback", datatype))

        self.columns = columns


