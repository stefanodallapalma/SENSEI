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
        """Create the table"""
        pk_attribute_names = ["`" + column.name + "`" for column in self.columns if column.pk is True]
        pk_query = "PRIMARY KEY (" + ", ".join(pk_attribute_names) + ")"
        query = "CREATE TABLE `" + self._database_name + "`.`" + self.table_name + "` ("

        for column in self.columns:
            # Datatype
            datatype = column.type
            str_type = datatype.type.name
            if datatype.param is not None:
                str_type += "(" + str(datatype.param) + ")"

            query += "`" + column.name + "` " + str_type
            if column.not_null:
                query += " NOT NULL"
            query += ", "

        query += pk_query + ")"

        self._mysql_db.insert(query)

        return True

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

    def update_beans(self, beans):
        if type(beans) is not list:
            beans = [beans]

        """Update a set of beans passed in input"""
        update_query_map = self.__generate_update_query_map(beans)
        for query in update_query_map:
            values = update_query_map[query]
            self._mysql_db.update(query, values)

    def delete_beans(self, beans):
        if type(beans) is not list:
            beans = [beans]

        """Delete a set of beans passed in input"""
        delete_query_map = self.__generate_delete_query_map(beans)
        for query in delete_query_map:
            values = delete_query_map[query]
            self._mysql_db.delete(query, values)

    # Table content methods - used to bypass the controls done by the concrete classes
    def select(self, query, values=None):
        """Method used to directly executed a select query"""
        return self._mysql_db.search(query, values)

    def insert(self, query, value):
        """Method used to directly executed an insert query"""
        self._mysql_db.insert(query, value)

    def update(self, query, value):
        """Method used to directly executed an insert query"""
        self._mysql_db.update(query, value)

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

    def __generate_update_query_map(self, beans):
        return self.__generate_query_map("UPDATE", beans)

    def __generate_query_map(self, query_type, beans):
        """Supports only INSERT and DELETE"""
        map = {}

        if query_type.upper() == "INSERT":
            start_query = "INSERT INTO `" + self._database_name + "`.`" + self.table_name + "` "
        elif query_type.upper() == "DELETE":
            start_query = "DELETE FROM `" + self._database_name + "`.`" + self.table_name + "` WHERE "
        elif query_type.upper() == "UPDATE":
            start_query = "UPDATE `" + self._database_name + "`.`" + self.table_name + "` "
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

                value = [getattr(bean, attribute) for attribute in bean_attributes if
                         getattr(bean, attribute) is not None]
            elif query_type.upper() == "DELETE":
                where_list = [(quote_bean_attribute + " = %s") for quote_bean_attribute in quote_bean_attributes
                              if quote_bean_attribute is not None]

                where_query = " AND ".join(where_list)
                query = start_query + where_query

                value = [getattr(bean, attribute) for attribute in bean_attributes if
                         getattr(bean, attribute) is not None]
            elif query_type.upper() == "UPDATE":
                pk_bean_attributes = [column.name for column in self.columns if column.pk is True and column.name in
                                      bean_attributes]
                not_pk_bean_attributes = [attribute for attribute in bean_attributes if attribute not in pk_bean_attributes]

                quote_pk_bean_attributes = ["`" + attribute + "`" for attribute in pk_bean_attributes]
                quote_not_pk_bean_attributes = ["`" + attribute + "`" for attribute in not_pk_bean_attributes]
                quote_pk_query = [(attribute + " = %s") for attribute in quote_pk_bean_attributes]
                quote_not_pk_query = [(attribute + " = %s") for attribute in quote_not_pk_bean_attributes]

                set_query = "SET " + ", ".join(quote_not_pk_query) + " "
                where_query = "WHERE " + " AND ".join(quote_pk_query)
                query = start_query + set_query + where_query

                not_pk_values = [getattr(bean, attribute) for attribute in not_pk_bean_attributes
                                 if getattr(bean, attribute) is not None]
                pk_values = [getattr(bean, attribute) for attribute in pk_bean_attributes if getattr(bean, attribute)
                             is not None]

                if len(not_pk_values) > 0 and len(pk_values) > 0:
                    value = not_pk_values + pk_values
                else:
                    value = None
            else:
                return None

            if value is not None:
                values = []
                if query in map:
                    values = map[query]

                values.append(tuple(value))
                map[query] = values

        return map
