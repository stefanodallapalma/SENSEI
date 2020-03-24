import mysql.connector
from database.db.DB import DB
from database.db.structure.DBType import DBType
from database.utils.DBUtils import get_db_parameters
from database.exception.DBException import DBException


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
                database=self.parameters.database_name,
                charset='utf8'
            )

        return db

    def search(self, query, values=None):
        """Run a query to retrieve data from the database"""
        if values is None:
            header, results = self.__execute__(query)
        else:
            header, results = self.__execute_with_escape__(query, values)

        return header, results

    def insert(self, query, value=None):
        if value is None:
            return self.__execute__(query, fetch_header=False, fetch_content=False)
        else:
            return self.__execute_with_escape__(query, value, fetch_header=False, fetch_content=False)

    def update(self, query, value=None):
        if value is None:
            return self.__execute__(query, fetch_header=False, fetch_content=False)
        else:
            return self.__execute_with_escape__(query, value, fetch_header=False, fetch_content=False)

    def delete(self, query, value=None):
        if value is None:
            return self.__execute__(query, fetch_header=False, fetch_content=False)
        else:
            return self.__execute_with_escape__(query, value, fetch_header=False, fetch_content=False)

    def __execute__(self, query, fetch_header=True, fetch_content=True):
        header = None
        try:
            db = self.connect()
            cursor = db.cursor(buffered=True)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return None

        try:
            cursor.execute(query)

            if fetch_header:
                header = [desc[0] for desc in cursor.description]

            if fetch_content:
                results = cursor.fetchall()
            else:
                results = True

            db.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return None
        finally:
            if db.is_connected():
                cursor.close()
                db.close()

        if fetch_header:
            return header, results
        else:
            return results

    def __execute_with_escape__(self, query, values, fetch_header=True, fetch_content=True):
        header = None
        try:
            db = self.connect()
            cursor = db.cursor(buffered=True)
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            raise DBException("Something went wrong: {}".format(err))

        try:
            if type(values) is list:
                for val in values:
                    cursor.execute(query, val)
            else:
                if type(values) is not tuple:
                    values = tuple(values)

                cursor.execute(query, values)

            if fetch_header:
                header = [desc[0] for desc in cursor.description]

            if fetch_content:
                results = cursor.fetchall()
            else:
                results = True

            db.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            raise DBException("Something went wrong: {}".format(err))
        finally:
            if db.is_connected():
                cursor.close()
                db.close()

        if fetch_header:
            return header, results
        else:
            return results
