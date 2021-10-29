import mysql.connector
import os
from database.db.structure.DBType import DBType
from database.utils.DBUtils import get_db_parameters
from database.exception.DBException import DBException


class MySqlDB:
    def __init__(self, database_name=None):
        super().__init__(DBType.MYSQL, database_name)
        self._db_name = database_name

    def connect(self):
        db = mysql.connector.connect(
            host="mysql",
            user=os.environ["MYSQL_USER"],
            passwd=os.environ["MYSQL_PASSWORD"],
            database=os.environ["MYSQL_DATABASE"],
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

    def exist_table(self, table_name):
        query = "SELECT * FROM information_schema.tables WHERE table_schema = \"" + self._db_name + \
                "\" AND table_name = \"" + table_name + "\""

        fields, res = self.search(query)

        if len(res) == 0:
            return False

        return True

    def create_table(self, query):
        """Create the table"""
        result = self.insert(query())
        return result

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

    def generate_dict(self, header, results):
        row_list = []

        for result in results:
            row_dict = {}
            for i in range(len(result)):
                row_dict[header[i]] = result[i]

            row_list.append(row_dict)

        return row_list