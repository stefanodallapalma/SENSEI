from ..controller.TableController import TableController
from ..model.market_models import Product
from ...db.structure.ColumnDB import ColumnDB
from ...db.structure.DataType import DataType
from ...db.structure.Type import Type

TABLE_NAME = "product"


class ProductController(TableController):
    def __init__(self):
        super().__init__(TABLE_NAME)

        # Init attributes
        self.init_columns()

    def init_columns(self):
        columns = []
        attribute_names = Product.__prop__()
        pk_attribute_names = ["timestamp", "market", "name"]
        double_attribute_names = ["price", "price_eur"]

        for attribute_name in attribute_names:
            if attribute_name in pk_attribute_names:
                datatype = DataType(Type.VARCHAR, 200)
                column = ColumnDB(attribute_name, datatype, pk=True, not_null=True)
            elif attribute_name in double_attribute_names:
                datatype = DataType(Type.VARCHAR, 200) # BEFORE DOUBLE
                column = ColumnDB(attribute_name, datatype)
            else:
                datatype = DataType(Type.VARCHAR, 200)
                column = ColumnDB(attribute_name, datatype)
            columns.append(column)

        self.columns = columns
