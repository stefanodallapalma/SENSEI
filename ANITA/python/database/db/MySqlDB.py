import mysql.connector
from database.db.DB import DB
from database.db.structure.DBType import DBType
from database.utils.DBUtils import get_db_parameters


class MySqlDB(DB):
    def __init__(self, database_name=None):
        super().__init__(DBType.MYSQL, database_name)
        self._parameters = get_db_parameters(DBType.MYSQL)
        self._db_name = database_name

    def connect(self):
        if self._db_name is None:
            db = mysql.connector.connect(
                host=self.parameters.host,
                user=self.parameters.user,
                passwd=self.parameters.password,
                charset='utf8'
            )
        else:
            db = mysql.connector.connect(
                host=self.parameters.host,
                user=self.parameters.user,
                passwd=self.parameters.password,
                database=self.parameters.database,
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

    def create_table(self, name, columns):
        pk_query = "PRIMARY KEY (`timestamp`, `name`)"
        for column in columns:
            if column.pk:
                pk_query += column.name + ", "

        pk_query = pk_query[:-2]
        pk_query += ")"

        query = "CREATE TABLE " + name + "("

        for column in columns:
            query += column.name + " " + column.type
            if column.not_null:
                query += " NOT NULL"
            query += ", "

        query += pk_query + ")"

        res = self.search(query)

        return res
