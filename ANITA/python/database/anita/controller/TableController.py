import json
from abc import ABC, abstractmethod
from database.utils.DBUtils import get_db_name
from database.anita.AnitaDB import AnitaDB
from database.db.structure.ColumnDB import ColumnDB
from database.db.MySqlDB import MySqlDB
from database.db.structure.DBType import DBType
from database.exception import DBException


class TableController(ABC):
    def __init__(self, name):
        self._table_name = name
        self._database_name = get_db_name(DBType.MYSQL)

        # Actual db implementation
        self._mysql_db = MySqlDB(self._database_name)

    # Properties
    @property
    def table_name(self):
        return self._table_name

    @table_name.setter
    def table_name(self, value):
        self._table_name = value

    @property
    def attributes(self):
        """Name of controller attributes"""
        return [column.name for column in self._columns]

    @property
    def columns(self):
        """Name of controller attributes"""
        return self._columns

    @columns.setter
    def columns(self, value):
        self._columns = value

    # Abstract methods
    @abstractmethod
    def init_columns(self):
        """Init columns of a dataset"""
        pass

    # Table methods
    def exist(self):
        query = "SELECT * FROM information_schema.tables WHERE table_schema = \"" + self._database_name + \
                "\" AND table_name = \"" + self.table_name + "\""

        fields, res = self._mysql_db.search(query)

        if len(res) == 0:
            return False

        return True

    def create(self):
        """Create the controller"""
        pk_attribute_names = ["`" + attribute.name + "`" for attribute in self.attributes if attribute.pk is True]
        pk_query = "PRIMARY KEY (" + ", ".join(pk_attribute_names) + ")"
        query = "CREATE TABLE `" + self._database_name + "`.`" + self.table_name + "` ("

        for attribute in self.attributes:
            # Datatype
            datatype = attribute.type
            str_type = datatype.type.name
            if datatype.param is not None:
                str_type += "(" + str(datatype.param) + ")"

            query += "`" + attribute.name + "` " + str_type
            if attribute.not_null:
                query += " NOT NULL"
            query += ", "

        query += pk_query + ")"

        # TEST
        print("CREATE TABLE QUERY: " + query)

        fields, res = self._mysql_db.search(query)

        return res

    def drop(self):
        """Delete the controller from the database"""
        query = "DROP TABLE `" + self._database_name + "`.`" + self.table_name
        self._mysql_db.search(query)

    # Operation with parameter dictionaries
    def select_by_params(self, dict_parameters):
        select_query = self.__generate_select_query(dict_parameters)
        value = tuple(dict_parameters.values())

        header, results = self.select(select_query, value)

        results_dict = []
        for result in results:
            result_dict = {}
            for i in range(len(header)):
                result_dict[header[i]] = result[i]
            results_dict.append(result_dict)

        return results_dict

    # Operations with beans
    def insert_beans(self, beans):
        if type(beans) is not list:
            beans = [beans]

        """Insert a set of beans passed in input"""
        insert_query_map = self.__generate_insert_query_map(beans)
        for query in insert_query_map:
            values = insert_query_map[query]
            self._mysql_db.insert(query, values)

    def delete_beans(self, beans):
        if type(beans) is not list:
            beans = [beans]

        """Delete a set of beans passed in input"""
        delete_query_map = self.__generate_delete_query_map(beans)
        for query in delete_query_map:
            print(query)
            values = delete_query_map[query]
            print(str(values))
            self._mysql_db.delete(query, values)

    # Table content methods - used to bypass the controls done by the concrete classes
    def select(self, query, values=None):
        """Method used to directly executed a select query"""
        return self._mysql_db.search(query, values)

    def insert(self, query, value):
        """Method used to directly executed an insert query"""
        self._mysql_db.insert(query, value)

    def delete(self, query, values=None):
        """Delete rows that satisfied all parameter passed as input (and)"""
        return self._mysql_db.delete(query, values)

    # Private methods
    def __generate_select_query(self, param_dict):
        select_query = "SELECT * FROM `" + self._database_name + "`.`" + self.table_name + "` WHERE "

        where_list = [("`" + attribute + "` = %s") for attribute in param_dict if attribute in self.attributes]
        where_query = " AND ".join(where_list)
        return select_query + where_query

    def __generate_insert_query_map(self, beans):
        return self.__generate_query_map("INSERT", beans)

    def __generate_delete_query_map(self, beans):
        return self.__generate_query_map("DELETE", beans)

    def __generate_query_map(self, query_type, beans):
        """Supports only INSERT and DELETE"""
        map = {}

        if query_type.upper() == "INSERT":
            start_query = "INSERT INTO `" + self._database_name + "`.`" + self.table_name + "` "
        elif query_type.upper() == "DELETE":
            start_query = "DELETE FROM `" + self._database_name + "`.`" + self.table_name + "` WHERE "
        else:
            return None

        for bean in beans:
            bean_attributes = [attribute for attribute in self.attributes if hasattr(bean, attribute)
                               and getattr(bean, attribute) is not None]
            quote_bean_attributes = [("`" + attribute + "`") for attribute in bean_attributes]

            # Query
            if query_type.upper() == "INSERT":
                attribute_query = "(" + ", ".join(quote_bean_attributes) + ")"
                value_query = "VALUES (" + ", ".join(["%s"] * len(quote_bean_attributes)) + ")"
                query = start_query + attribute_query + " " + value_query
            elif query_type.upper() == "DELETE":
                where_list = [(quote_bean_attribute + " = %s") for quote_bean_attribute in quote_bean_attributes
                              if quote_bean_attribute is not None]
                where_query = " AND ".join(where_list)
                query = start_query + where_query
            else:
                return None

            values = []
            if query in map:
                values = map[query]

            # Get the actual list of values
            value = [getattr(bean, attribute) for attribute in bean_attributes if getattr(bean, attribute) is not None]
            values.append(tuple(value))
            map[query] = values

        return map
