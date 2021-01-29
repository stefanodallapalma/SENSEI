import logging

from ..controller.TableController import TableController
from ...db.structure.DataType import DataType
from ...db.structure.Type import Type
from ...db.structure.ColumnDB import ColumnDB
from ..model.market_models import Vendor

logger = logging.getLogger("Vendor Controller")

TABLE_NAME = "vendor"


class VendorController(TableController):
    def __init__(self):
        super().__init__(TABLE_NAME)

        # Init attributes
        self.init_columns()

    def init_columns(self):
        columns = []
        attribute_names = Vendor.__prop__()
        pk_attribute_names = ["timestamp", "market", "name"]
        double_attribute_names = ["score", "score_normalized"]

        for attribute_name in attribute_names:
            if attribute_name in pk_attribute_names:
                datatype = DataType(Type.VARCHAR, 200)
                column = ColumnDB(attribute_name, datatype, pk=True, not_null=True)
            elif attribute_name in double_attribute_names:
                datatype = DataType(Type.VARCHAR, 200) # BEFORE IT WAS DOUBLE
                column = ColumnDB(attribute_name, datatype)
            else:
                if attribute_name == "info":
                    datatype = DataType(Type.LONGTEXT)
                elif attribute_name == "feedback":
                    datatype = DataType(Type.INT)
                elif attribute_name == "pgp":
                    datatype = DataType(Type.VARCHAR, 5000)
                else:
                    datatype = DataType(Type.VARCHAR, 200)
                column = ColumnDB(attribute_name, datatype)
            columns.append(column)

        self.columns = columns

    def insert_beans(self, beans):
        attributes = ["timestamp", "market", "name", "score", "score_normalized", "registration",
                      "registration_deviation", "last_login", "last_login_deviation", "sales", "info",
                      "feedback", "pgp"]

        # Retrieve the greatest feedback id

        new_beans = []
        for bean in beans:
            for attr in attributes:
                val = getattr(bean, attr)
                if isinstance(val, list):
                    val = ", ".join(str(elem) for elem in val)
                    setattr(bean, attr, val)
            new_beans.append(bean)

        super(VendorController, self).insert_beans(new_beans)

    def retrieve_markets(self):
        query = "SELECT {0}.market from {1}.{0} GROUP BY {0}.market".format(TABLE_NAME, self.db_name)
        header, results = self.mysql_db.search(query)

        markets = []
        for result in results:
            markets.append(result[0].lower())

        return markets

    def retrieve_vendors(self):
        query = "SELECT DISTINCT {0}.timestamp, {0}.market, {0}.name FROM {1}.{0} ORDER BY {0}.timestamp DESC"\
            .format(TABLE_NAME, self.db_name)

        header, results = self.mysql_db.search(query)

        markets = {}

        for result in results:
            timestamp = result[0]
            market = result[1]
            name = result[2]

            if market not in markets:
                markets[market] = {}

            if str(timestamp) not in markets[market]:
                markets[market][timestamp] = []

            markets[market][timestamp].append(name)

        return markets

    def retrieve_vendor(self, vendor):
        query = "SELECT * FROM {1}.{0} WHERE {0}.name = %s ORDER BY {0}.timestamp DESC" \
            .format(TABLE_NAME, self.db_name)

        values = (vendor,)

        header, results = self.mysql_db.search(query, values)

        markets = {}

        for result in results:
            vendor = {}
            for i in range(len(header)):
                attribute = header[i]
                value = result[i]
                vendor[attribute] = value

            timestamp = vendor["timestamp"]
            market = vendor["market"]
            del vendor["timestamp"]
            del vendor["market"]

            if market not in markets:
                markets[market] = {}

            #if timestamp not in markets[market]:
            #    markets[market][timestamp] = []

            # Get a single vendor for each timestamp
            # MULTIPLE VENDOR: markets[market][timestamp].append(vendor)
            markets[market][timestamp] = vendor


        return markets

    def retrieve_vendor_by_pgp(self, pgp):
        query = "SELECT {0}.name, {0}.market, {0}.pgp FROM {1}.{0} WHERE {0}.pgp = %s".format(TABLE_NAME, self.db_name)
        values = (pgp,)

        header, results = self.mysql_db.search(query, values)

        pgp_graph = {}

        for result in results:
            vendor_name = result[0]
            market = result[1]

            pgp_graph[market] = vendor_name

        return pgp_graph