from database.db.MySqlDB import MySqlDB
from database.utils import DBUtils as db_utils
from database.db.DBType import DBType

database_name = "anita"


class AnitaDB:
    def __init__(self, database_name=None):
        self._mysqlDB = MySqlDB(database_name)

    def create_db(self):
        if self.exist():
            raise Exception("Database \"anita\" already created")

        create_query = "CREATE SCHEMA " + database_name
        self._mysqlDB.search(create_query)

        db_utils.add_database_name(DBType.MYSQL, database_name)

    def exist(self):
        query = "SHOW DATABASES"

        databases = self._mysqlDB.search(query)
        for database in databases:
            if database_name == database[0]:
                return True

        return False

