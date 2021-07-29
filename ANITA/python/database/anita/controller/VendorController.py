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

        # Timestamp
        datatype = DataType(Type.VARCHAR, 20)
        columns.append(ColumnDB("timestamp", datatype, pk=True, not_null=True))

        # Market
        datatype = DataType(Type.VARCHAR, 100)
        columns.append(ColumnDB("market", datatype, pk=True, not_null=True))

        # Name
        datatype = DataType(Type.VARCHAR, 200)
        columns.append(ColumnDB("name", datatype, pk=True, not_null=True))

        # Score
        datatype = DataType(Type.VARCHAR, 200)
        columns.append(ColumnDB("score", datatype))

        # Score normalized
        datatype = DataType(Type.VARCHAR, 200)
        columns.append(ColumnDB("score_normalized", datatype))

        # Registration
        datatype = DataType(Type.VARCHAR, 200)
        columns.append(ColumnDB("registration", datatype))

        # Registration deviation
        datatype = DataType(Type.VARCHAR, 200)
        columns.append(ColumnDB("registration_deviation", datatype))

        # Last login
        datatype = DataType(Type.VARCHAR, 200)
        columns.append(ColumnDB("last_login", datatype))

        # Last login deviation
        datatype = DataType(Type.VARCHAR, 200)
        columns.append(ColumnDB("last_login_deviation", datatype))

        # Sales
        datatype = DataType(Type.VARCHAR, 200)
        columns.append(ColumnDB("sales", datatype))

        # Info
        datatype = DataType(Type.LONGTEXT)
        columns.append(ColumnDB("info", datatype))

        # Feedback
        datatype = DataType(Type.INT)
        columns.append(ColumnDB("feedback", datatype))

        # PGP
        datatype = DataType(Type.VARCHAR, 5000)
        columns.append(ColumnDB("pgp", datatype))

        """attribute_names = Vendor.__prop__()
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
            columns.append(column)"""

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

    def delete_dumps(self, market, timestamps):
        query = "DELETE FROM `{0}`.`{1}` WHERE (`market` = %s) AND (`timestamp` = %s)".format(self.db_name, TABLE_NAME)

        values = []
        for timestamp in timestamps:
            values.append((market, timestamp))

        self.mysql_db.delete(query, values)

    def get_vendor_filtered(self):
        """
        This function retrieves vendor data from MySql DB, based on the following attributes:
        timestamp, market, name, info,registration,score_normalized
        """
        query = f"SELECT timestamp, market, name, info, registration, score_normalized FROM {self.db_name}.{TABLE_NAME}"
        header, results = self.mysql_db.search(query)

        final_data = []
        for vendor_info in results:
            if vendor_info[3] == None:
                vendor_info_list = list(vendor_info)
                vendor_info_list[3] = ''
                vendor_info_tuple = tuple(vendor_info_list)
                final_data.append(vendor_info_tuple)
            else:
                final_data.append(vendor_info)

        return final_data

    def get_vendor_country(self):
        query = 'SELECT vendor.name, vendor.market, product.ships_from, product.ships_to FROM anita.vendor INNER JOIN' \
                ' anita.product ON vendor.name = product.vendor;'

        header, results = self.mysql_db.search(query)

        vendor_country = []
        for line in results:
            vendor_country.append(dict(zip(header, line)))

        return vendor_country