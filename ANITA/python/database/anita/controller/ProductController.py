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
        pk_attribute_names = ["timestamp", "market", "name", "vendor"]
        double_attribute_names = ["price", "price_eur"]

        for attribute_name in attribute_names:
            if attribute_name in pk_attribute_names:
                datatype = DataType(Type.VARCHAR, 200)
                column = ColumnDB(attribute_name, datatype, pk=True, not_null=True)
            elif attribute_name in double_attribute_names:
                datatype = DataType(Type.VARCHAR, 200) # BEFORE DOUBLE
                column = ColumnDB(attribute_name, datatype)
            else:
                if attribute_name == "info":
                    datatype = DataType(Type.LONGTEXT)
                elif attribute_name == "ships_from" or attribute_name == "ships_to":
                    datatype = DataType(Type.VARCHAR, 2000)
                else:
                    datatype = DataType(Type.VARCHAR, 200)

                column = ColumnDB(attribute_name, datatype)
            columns.append(column)

        self.columns = columns

    def insert_beans(self, beans):
        attributes = ["timestamp", "market", "name", "vendor", "ships_from", "ships_to", "price", "price_eur", "info", "feedback"]

        new_beans = []
        for bean in beans:
            for attr in attributes:
                val = getattr(bean, attr)
                if isinstance(val, list):
                    val = ", ".join(val)
                    setattr(bean, attr, val)
            new_beans.append(bean)

        super(ProductController, self).insert_beans(new_beans)

