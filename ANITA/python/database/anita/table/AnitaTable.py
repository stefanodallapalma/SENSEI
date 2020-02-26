from abc import ABC, abstractmethod
from database.utils.DBUtils import get_db_name
from database.anita.AnitaDB import AnitaDB
from database.db.structure.ColumnDB import ColumnDB
from database.db.MySqlDB import MySqlDB
from database.db.structure.DBType import DBType


class AnitaTable(ABC):
    def __init__(self, name):
        self._table_name = name
        self._mysql_db = MySqlDB(get_db_name(DBType.MYSQL))

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

    @abstractmethod
    def init_attributes(self):
        pass

    def exist(self):
        query = "SELECT * FROM information_schema.tables WHERE table_schema = " + self.database_name + \
                " AND table_name = " + self.table_name

        res = self.mysql_db.search(query)

        if len(res) == 0:
            return False

        return True

    def create(self):
        pk_query = "PRIMARY KEY ("
        for attribute in self.attributes:
            if attribute.pk:
                pk_query += attribute.name + ", "

        pk_query = pk_query[:-2]
        pk_query += ")"

        query = "CREATE TABLE " + self.table_name + "("

        for attribute in self.attributes:
            # Datatype
            datatype = attribute.type
            str_type = datatype.type.name
            if datatype.param is not None:
                str_type += "(" + datatype.param + ")"

            query += attribute.name + " " + str_type
            if attribute.not_null:
                query += " NOT NULL"
            query += ", "

        query += pk_query + ")"

        # TEST
        print("CREATE TABLE QUERY: " + query)

        res = self.mysql_db.search(query)

        return res

    @abstractmethod
    def insert_values(self, values):
        pass

    @abstractmethod
    def delete_values(self, values):
        pass

    def delete(self):
        """Delete the table from the database"""
        pass

    def generate_insert_query(self, attribute_names):
        insert_query = "INSERT INTO " + self.table_name + " "
        attribute_query = "(" + ", ".join(attribute_names) + ")"
        value_query = "VALUES (" + ", ".join(["%s"] * len(attribute_names)) + ")"
        insert_query += attribute_query + " " + value_query

        return insert_query
