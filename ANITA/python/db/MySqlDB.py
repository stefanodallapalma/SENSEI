import mysql.connector
from utils.FileUtils import get_dict_from_file as get_parameters_dict

class MySqlDB:
    def __init__(self, db_parameters_path):
        self._connection_parameter = get_parameters_dict(db_parameters_path)

    def init_connection(self):
        db = mysql.connector.connect(
            host=self._connection_parameter["host"],
            user = self._connection_parameter["user"],
            passwd=self._connection_parameter["psw"],
            database=self._connection_parameter["database"],
            charset='utf8'
        )

        return db

    def select(self, query):
        try:
            db = self.init_connection()
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

    def insert_many(self, query, values):
        try:
            db = self.init_connection()
            cursor = db.cursor()

            for val in values:
                cursor.execute(query, val)

            db.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return False
        finally:
            if db.is_connected():
                cursor.close()
                db.close()

        return True

    def insert(self, query, val):
        values = []
        values.append(val)
        self.insert_many(query, values)