from database.db.MySqlDB import MySqlDB

database_name = "anita"


class AnitaDB:
    def __init__(self):
        self._mysqlDB = MySqlDB(database_name)

