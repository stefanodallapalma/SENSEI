from database.db.MySqlDB import MySqlDB
from database.utils import DBUtils as db_utils
from database.db.structure.DBType import DBType

name = "anita"


class AnitaDB:
    def __init__(self, anonymous=False):
        self.database_name = name
        if anonymous:
            self.mysql_db = MySqlDB()
        else:
            self.mysql_db = MySqlDB(self.database_name)

    @property
    def database_name(self):
        return self._database_name

    @database_name.setter
    def database_name(self, value):
        self._database_name = value

    @property
    def mysql_db(self):
        return self._mysql_db

    @mysql_db.setter
    def mysql_db(self, value):
        self._mysql_db = value

    def exist(self):
        query = "SHOW DATABASES"

        fields, databases = self.mysql_db.search(query)
        print("FIELDS: " + str(fields))
        print("VALUES: " + str(databases))
        for database in databases:
            if self.database_name == database[0]:
                return True

        return False

    def create(self):
        if self.exist():
            raise Exception("Database `anita` already created")

        create_query = "CREATE SCHEMA `" + self.database_name + "`"
        print("CREATE DB QUERY")
        print(create_query)

        self.mysql_db.insert(create_query)

        db_utils.add_database_name(DBType.MYSQL, self.database_name)



