from database.anita.AnitaDB import AnitaDB
from database.db.structure.ColumnDB import ColumnDB

class QualityTable(AnitaDB):
    name = "quality"

    def exist(self):
        query = "SELECT * FROM information_schema.tables WHERE table_schema = " + self.database_name +\
                " AND table_name = " + self.name

        res = self.mysql_db.search(query)

        if len(res) == 0:
            return False

        return True

    def create_quality_table(self, metric_list):
        columns = []

        # Timestamp column
        timestamp_column = ColumnDB("timestamp", "VARCHAR(50)", pk=True, not_null=True)
        columns.append(timestamp_column)

        # Name column
        name_column = ColumnDB("name", "VARCHAR(500)", pk=True, not_null=True)
        columns.append(name_column)

        for metric in metric_list:
            metric_column = ColumnDB(metric, "DOUBLE")
            columns.append(metric_column)

        return self.mysql_db.create_table(self.name, columns)

    def insert_quality(self, metric_list, quality):
        # Insert query
        sql = self.build_insert_query(metric_list)

        val_list = []
        for metric in metric_list:
            if metric in quality.metrics:
                val_list.append(quality.metrics[metric])
            else:
                val_list.append(None)

        val = (quality.timestamp, quality.name)
        val += tuple(val_list)

        self.mysql_db.insert(sql, val)

    def insert_qualities(self, metric_list, qualities):
        # Insert query
        sql = self.build_insert_query(metric_list)

        values = []
        for quality in qualities:
            val_list = []
            for metric in metric_list:
                if metric in quality.metrics:
                    val_list.append(quality.metrics[metric])
                else:
                    val_list.append(None)

            val = (quality.timestamp, quality.name)
            val += tuple(val_list)

            values.append(val)

        self.mysql_db.insert(sql, values)

    def build_insert_query(self, metrics):
        # Insert query
        sql = "INSERT INTO " + self.name + " (timestamp, name, "
        values_sql = "VALUES (%s, %s, "

        for metric in metrics:
            sql += metric + ", "
            values_sql += "%s, "

        sql = sql[:-2]
        sql += ") "

        values_sql = values_sql[:-2]
        values_sql += ")"

        sql += values_sql

        return sql