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

        # Timestamp
        datatype = DataType(Type.VARCHAR, 20)
        columns.append(ColumnDB("timestamp", datatype, pk=True, not_null=True))

        # Market
        datatype = DataType(Type.VARCHAR, 100)
        columns.append(ColumnDB("market", datatype, pk=True, not_null=True))

        # Name
        datatype = DataType(Type.VARCHAR, 200)
        columns.append(ColumnDB("name", datatype, pk=True, not_null=True))

        # Vendor
        datatype = DataType(Type.VARCHAR, 200)
        columns.append(ColumnDB("vendor", datatype, pk=True, not_null=True))

        # Ships from
        datatype = DataType(Type.VARCHAR, 2000)
        columns.append(ColumnDB("ships_from", datatype))

        # Ships from
        datatype = DataType(Type.VARCHAR, 2000)
        columns.append(ColumnDB("ships_to", datatype))

        # Price
        datatype = DataType(Type.VARCHAR, 50)
        columns.append(ColumnDB("price", datatype, pk=True, not_null=True))

        # Price eur
        datatype = DataType(Type.VARCHAR, 50)
        columns.append(ColumnDB("price_eur", datatype))

        # Category
        datatype = DataType(Type.VARCHAR, 100)
        columns.append(ColumnDB("category", datatype))

        # Info
        datatype = DataType(Type.LONGTEXT)
        columns.append(ColumnDB("info", datatype))

        # Feedback
        datatype = DataType(Type.INT)
        columns.append(ColumnDB("feedback", datatype))


        """attribute_names = Product.__prop__()
        pk_attribute_names = ["timestamp", "market", "name", "vendor", "price"]
        #double_attribute_names = ["price", "price_eur"]

        for attribute_name in attribute_names:
            if attribute_name in pk_attribute_names:
                if attribute_name == "timestamp":
                    datatype = DataType(Type.VARCHAR, 20)
                elif "price" in attribute_name:
                    datatype = DataType(Type.VARCHAR, 50)
                elif attribute_name == "market":
                    datatype = DataType(Type.VARCHAR, 100)
                else:
                    datatype = DataType(Type.VARCHAR, 200)

                column = ColumnDB(attribute_name, datatype, pk=True, not_null=True)
            else:
                if attribute_name == "info":
                    datatype = DataType(Type.LONGTEXT)
                elif attribute_name == "ships_from" or attribute_name == "ships_to":
                    datatype = DataType(Type.VARCHAR, 2000)
                elif attribute_name == "feedback":
                    datatype = DataType(Type.INT)
                else:
                    datatype = DataType(Type.VARCHAR, 200)

                column = ColumnDB(attribute_name, datatype)
            columns.append(column)"""

        self.columns = columns

    def insert_beans(self, beans):
        attributes = ["timestamp", "market", "name", "vendor", "ships_from", "ships_to", "price", "price_eur", "info",
                      "feedback"]

        # Preprocessing
        new_beans = []
        for bean in beans:
            for attr in attributes:
                val = getattr(bean, attr)
                if isinstance(val, list):
                    val = ", ".join(str(elem) for elem in val)
                    setattr(bean, attr, val)
            new_beans.append(bean)

        super(ProductController, self).insert_beans(new_beans)

    def retrieve_markets(self):
        query = "SELECT {0}.market from {1}.{0} GROUP BY {0}.market".format(TABLE_NAME, self.db_name)
        header, results = self.mysql_db.search(query)

        markets = []
        for result in results:
            markets.append(result[0].lower())

        return markets

    def retrieve_markets_timestamps(self):
        query = "SELECT DISTINCT {0}.timestamp, {0}.market FROM {1}.{0} ORDER BY {0}.timestamp DESC"\
            .format(TABLE_NAME, self.db_name)

        header, results = self.mysql_db.search(query)

        markets_timestamps = {}
        for result in results:
            market = result[1]
            timestamp = result[0]

            if market in markets_timestamps:
                markets_timestamps[market].append(timestamp)
            else:
                markets_timestamps[market] = [timestamp]

        return markets_timestamps

    def retrieve_markets_timestamps_products(self):
        query = "SELECT DISTINCT {0}.name, {0}.timestamp, {0}.market FROM {1}.{0} ORDER BY {0}.timestamp DESC"\
            .format(TABLE_NAME, self.db_name)

        header, results = self.mysql_db.search(query)

        markets_timestamps = {}
        for result in results:
            market = result[2]
            timestamp = result[1]
            name = result[0]

            if market in markets_timestamps:
                if timestamp in markets_timestamps[market]:
                    markets_timestamps[market][timestamp].append(name)
                else:
                    markets_timestamps[market][timestamp] = [name]
            else:
                markets_timestamps[market] = {timestamp: [name]}

        return markets_timestamps

    def retrieve_vendor_products(self, vendor):
        query = "SELECT DISTINCT {0}.name, {0}.vendor, {0}.timestamp, {0}.market from {1}.{0} WHERE {0}.vendor = %s " \
                "ORDER BY {0}.timestamp DESC".format(TABLE_NAME, self.db_name)

        values = (vendor,)
        header, results = self.mysql_db.search(query, values)

        markets = {}

        for result in results:
            product = {}
            for i in range(len(header)):
                attribute = header[i]
                value = result[i]
                product[attribute] = value

            timestamp = product["timestamp"]
            market = product["market"]
            name = product["name"]

            # Check if the market has already been saved in the dict
            if market not in markets:
                markets[market] = {}

            # Check if the timestamp has already been saved in the market value
            if timestamp not in markets[market]:
                markets[market][timestamp] = []

            markets[market][timestamp].append(name)

        return {vendor: markets}

    def retrieve_vendor_product(self, vendor, product_name):
        query = "SELECT * FROM {1}.{0} WHERE {0}.vendor = %s AND {0}.name = %s" \
                "ORDER BY {0}.timestamp DESC".format(TABLE_NAME, self.db_name)

        values = (vendor, product_name)
        header, results = self.mysql_db.search(query, values)

        markets = {}

        for result in results:
            product = {}
            for i in range(len(header)):
                attribute = header[i]
                value = result[i]
                product[attribute] = value

            timestamp = product["timestamp"]
            market = product["market"]
            del product["timestamp"]
            del product["market"]
            del product["vendor"]

            # Check if the market has already been saved in the dict
            if market not in markets:
                markets[market] = {}

            # Check if the timestamp has already been saved in the market value
            if timestamp not in markets[market]:
                markets[market][timestamp] = []

            markets[market][timestamp].append(product)

        return {vendor: markets}

    def get_product(self, market, name, last_timestamp=False):
        query = "SELECT * from {0}.{1} WHERE {1}.market = %s AND {1}.name = %s ORDER BY {1}.timestamp DESC".format(self.db_name, TABLE_NAME)

        values = (market, name)
        header, results = self.mysql_db.search(query, values)

        timestamps = {}
        max_timestamp = 0

        for result in results:
            product = {}
            for i in range(len(header)):
                attribute = header[i]
                value = result[i]
                product[attribute] = value

            timestamp = product["timestamp"]
            del product["timestamp"]

            # The first timestamp is the last inserted, because the query has been ordered by timestamp
            if max_timestamp is None:
                max_timestamp = timestamp

            if timestamp in timestamps:
                timestamps[timestamp].append(product)
            else:
                timestamps[timestamp] = [product]

        if last_timestamp and timestamps:
            timestamps = timestamps[max_timestamp]

        products = {market: timestamps}
        return products

    def delete_dumps(self, market, timestamps):
        query = "DELETE FROM `{0}`.`{1}` WHERE (`market` = %s) AND (`timestamp` = %s)".format(self.db_name, TABLE_NAME)

        values = []
        for timestamp in timestamps:
            values.append((market, timestamp))

        self.mysql_db.delete(query, values)

    def get_product_no_fdb(self):
        """
        Get products without feedback
        """

        query = f"SELECT timestamp, market, name, vendor, ships_from, ships_to, category, price " \
                f"FROM {self.db_name}.{TABLE_NAME};"

        header, results = self.mysql_db.search(query)

        json_data = []
        for line in results:
            json_data.append(dict(zip(header, line)))

        return json_data

    def check_table(self):
        sql = "DESCRIBE product;"
        return self._mysql_db.search(sql)