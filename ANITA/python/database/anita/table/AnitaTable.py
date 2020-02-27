from abc import ABC, abstractmethod
from database.utils.DBUtils import get_db_name
from database.anita.AnitaDB import AnitaDB
from database.db.structure.ColumnDB import ColumnDB
from database.db.MySqlDB import MySqlDB
from database.db.structure.DBType import DBType
from database.exception import DBException


class AnitaTable(ABC):
    def __init__(self, name):
        self._table_name = name
        self._database_name = get_db_name(DBType.MYSQL)
        print("Database name: " + self._database_name)
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
        return self._attributes

    @attributes.setter
    def attributes(self, value):
        self._attributes = value

    @property
    def mysql_db(self):
        return self._mysql_db

    @mysql_db.setter
    def mysql_db(self, value):
        self._mysql_db = value

    # Abstract methods
    @abstractmethod
    def init_attributes(self):
        pass

    @abstractmethod
    def insert_values(self, values):
        """Insert a set of beans passed in input"""
        pass

    @abstractmethod
    def delete_values(self, values):
        """Delete a set of beans passed in input"""
        pass

    # Table methods
    def exist(self):
        query = "SELECT * FROM information_schema.tables WHERE table_schema = \"" + self._database_name + \
                "\" AND table_name = \"" + self.table_name + "\""

        fields, res = self.mysql_db.search(query)

        if len(res) == 0:
            return False

        return True

    def create(self):
        """Create the table"""
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

        fields, res = self.mysql_db.search(query)

        return res

    def delete(self):
        """Delete the table from the database"""
        query = "DROP TABLE `" + self._database_name + "`.`" + self.table_name
        self.mysql_db.search(query)

    # Table content methods - used to bypass the controls done by the concrete classes
    def insert(self, query, value):
        """Method used to directly executed an insert query"""
        self.mysql_db.insert(query, value)

    def select(self, query, values=None):
        """Method used to directly executed a select query"""
        return self.mysql_db.search(query, values)

    def delete_rows(self, parameters_dict):
        """Delete rows that satisfied all parameter passed as input (and)"""
        attribute_names = [key for key in parameters_dict]
        values = [parameters_dict[key] for key in parameters_dict]
        values = tuple(values)

        delete_query = self.generate_delete_query(attribute_names)

        self.mysql_db.delete(delete_query, values)

    def generate_insert_query(self, attribute_names):
        quote_attribute_names = [("`" + attribute + "`") for attribute in attribute_names]

        insert_query = "INSERT INTO `" + self._database_name + "`.`" + self.table_name + "` "
        attribute_query = "(" + ", ".join(quote_attribute_names) + ")"
        value_query = "VALUES (" + ", ".join(["%s"] * len(quote_attribute_names)) + ")"
        insert_query += attribute_query + " " + value_query

        return insert_query

    def generate_delete_query(self, attribute_names):
        quote_attribute_names = [("`" + attribute + "`") for attribute in attribute_names]

        delete_query = "DELETE FROM `" + self._database_name + "`.`" + self.table_name + "` WHERE "

        where_list = [(quote_attribute_name + " = %s") for quote_attribute_name in quote_attribute_names]
        where_query = " AND ".join(where_list)

        delete_query += where_query

        return delete_query
