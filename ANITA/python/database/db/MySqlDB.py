import mysql.connecto
from database.db.DB import DB
from database.db.DBType import DBType
from utils.FileUtils import get_dict_from_file as get_parameters_dict


class MySqlDB(DB):
    def __init__(self, database_name=None):
        super().__init__(DBType.MYSQL, database_name)

    def connect(self):
        if self._db_name is None:
            db = mysql.connector.connect(
                host=self._parameter["host"],
                user=self._parameter["user"],
                passwd=self._parameter["password"],
                charset='utf8'
            )
        else:
            db = mysql.connector.connect(
                host=self._parameter["host"],
                user=self._parameter["user"],
                passwd=self._parameter["password"],
                database=self._parameter["database"],
                charset='utf8'
            )

        return db

    def search(self, query):
        try:
            db = self.connect()
            cursor = db.cursor()

            cursor.execute(query)

            result = cursor.fetchall()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return None
        finally:
            if db.is_connected():
                cursor.close()
                db.close()

        return result

    def insert(self, query, value):
        try:
            db = self.init_connection()
            cursor = db.cursor()

            if type(value) is list:
                for val in value:
                    cursor.execute(query, val)
            else:
                cursor.execute(query, value)

            db.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return False
        finally:
            if db.is_connected():
                cursor.close()
                db.close()

        return True

    def delete(self, query):
        pass
