import datetime
import time
import logging
from pypika import Query, Table, Field

from db.mysql_connection import MySqlDB
from utils import first_day_timestamp, convert_numerical_month_to_str

DB_NAME = "anita"

logger = logging.getLogger("Controller")


class PseudonymizedVendorController:
    def __init__(self):
        self.db = MySqlDB()
        self.table_name = "pseudonymized_vendors"

    def get_vendors_alias(self):
        """
        Search for the alias-real_name key-value
        :return: Dict containing all alias-name of a vendor
        """

        query = f'SELECT * FROM {DB_NAME}.{self.table_name};'
        header, results = self.db.search(query)

        # Dict alias - vendor name
        vendor_alias = {}
        for row in results:
            alias = row[0]
            name = row[1]
            vendor_alias[alias] = name

        return vendor_alias


class ReviewController:
    def __init__(self):
        self.db = MySqlDB()
        self.table_name = "reviews"

    def get_reviews(self):
        """
        Get the content of the review table
        :return: Review list
        """

        query = f'SELECT * FROM {DB_NAME}.{self.table_name};'
        header, results = self.db.search(query)

        reviews = []
        for line in results:
            reviews.append(dict(zip(header, line)))

        return reviews

    def get_pseudonymized_reviews(self):
        """
        Get the content of the review table, with pseudonyms instead of real names
        :return: Pseudonyms review list
        """

        reviews_table = "reviews"
        pseudonymized_vendors_table = "pseudonymized_vendors"

        query = "SELECT {0}.feedback_id, {0}.id, {1}.pseudonym AS `name`, {0}.message, {0}.product, {0}.deals, " \
                "{0}.market, {0}.timestamp, {0}.macro_category FROM {2}.{0} JOIN {2}.{1} ON {0}.name = {1}.alias;"\
            .format(reviews_table, pseudonymized_vendors_table, DB_NAME)

        header, results = self.db.search(query)

        reviews = []
        for line in results:
            reviews.append(dict(zip(header, line)))

        return reviews

    def n_reviews_per_country(self):
        query = "SELECT ships_from, count(message) as n_reviews " \
                f"FROM {DB_NAME}.{self.table_name} JOIN {DB_NAME}.products_cleaned ON {self.table_name}.product = " \
                f"products_cleaned.name " \
                "WHERE ships_from is not NULL " \
                "GROUP BY ships_from;"

        header, results = self.db.search(query)

        countries = {}
        for row in results:
            countries[row[0]] = row[1]

        return countries

    def n_sales_per_vendor(self):
        query = "SELECT reviews.name, COUNT(reviews.name) as n_sales " \
                f"FROM {DB_NAME}.{self.table_name} JOIN {DB_NAME}.`vendor-analysis` " \
                f"ON {self.table_name}.name = `vendor-analysis`.name " \
                f"GROUP BY {self.table_name}.name;"

        header, results = self.db.search(query)

        n_sales = {}
        for row in results:
            n_sales[row[0]] = row[1]

        return n_sales

    def n_review_foreach_market(self):
        query = f"SELECT market, COUNT(DISTINCT(message)) FROM {DB_NAME}.{self.table_name} GROUP BY market;"

        header, results = self.db.search(query)

        market_reviews = {}
        for row in results:
            market_reviews[row[0]] = row[1]

        return market_reviews

    def n_review(self):
        market_reviews = self.n_review_foreach_market()

        tot_reviews = 0
        for market in market_reviews:
            tot_reviews += market_reviews[market]

        return tot_reviews


class ProductCleanedController:
    def __init__(self):
        self.db = MySqlDB()
        self.table_name = "products_cleaned"

    def last_timestamp(self):
        timestamp_skip = 1612264332

        query = f"SELECT MAX(timestamp) from {DB_NAME}.{self.table_name} WHERE timestamp != %s;"

        value = (timestamp_skip,)
        header, results = self.db.search(query, value)

        if not results:
            return None

        return results[0][0]

    def get_distinct_timestamps(self):
        query = f"SELECT distinct products_cleaned.timestamp FROM {DB_NAME}.{self.table_name};"

        header, results = self.db.search(query)

        return [row[0] for row in results]

    def get_product_cleaned(self):
        query = f'SELECT * FROM {DB_NAME}.{self.table_name};'

        header, results = self.db.search(query)

        products = []
        for line in results:
            products.append(dict(zip(header, line)))

        return products

    def n_products_per_country(self):
        query = "SELECT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(ships_from,',',i+1),',',-1)) as country, " \
                "count(name) as n_products " \
                f"FROM {DB_NAME}.ints, {DB_NAME}.`products_cleaned` " \
                "WHERE ships_from is not NULL " \
                "GROUP BY country;"

        query = f"SELECT DISTINCT(ships_from), COUNT(name) as n_products FROM {DB_NAME}.`products_cleaned` " \
                f"WHERE ships_from is not NULL GROUP BY ships_from ORDER BY n_products DESC;"

        header, results = self.db.search(query)

        countries = {}
        for row in results:
            countries[row[0]] = row[1]

        return countries

    def best_vendor(self, country=None):
        """
        Takes the vendor with the higher number of product on the market
        """

        if not country:
            query = "SELECT vendor, COUNT(vendor) as n_products " \
                    f"FROM {DB_NAME}.products_cleaned " \
                    "GROUP BY vendor " \
                    "ORDER BY n_products DESC;"
            header, results = self.db.search(query)
        else:
            query = "SELECT vendor, COUNT(vendor) as n_products " \
                    f"FROM {DB_NAME}.products_cleaned " \
                    "WHERE ships_from = %s " \
                    "GROUP BY vendor " \
                    "ORDER BY n_products DESC;"
            value = (country,)
            header, results = self.db.search(query, value)

        if not results:
            return None

        best_vendor = results[0][0]
        return best_vendor

    def n_sales_per_country(self):
        query = f"SELECT ships_from, ROUND(SUM(price),2) FROM {DB_NAME}.products_cleaned GROUP BY ships_from;"

        header, results = self.db.search(query)

        countries_price = {}
        for row in results:
            countries_price[row[0]] = row[1]

        return countries_price

    def sum_price(self):
        last_ts = self.last_timestamp()

        if not last_ts:
            return None

        first_day_ts = first_day_timestamp(last_ts)

        query = "SELECT ROUND(SUM(tot_price),2) FROM " \
                "(SELECT DISTINCT(vendor), count(name) as qty, round(sum(price),2) as tot_price " \
                "FROM anita.products_cleaned " \
                "WHERE timestamp >= %s AND timestamp <= %s " \
                "GROUP BY vendor " \
                "ORDER BY tot_price DESC) as top_vendors;"

        value = (first_day_ts, last_ts)

        header, results = self.db.search(query, value)

        return results[0][0]

    def n_products_for_each_market(self):
        query = f"SELECT DISTINCT(market), COUNT(name) FROM {DB_NAME}.products_cleaned GROUP BY market;"

        header, results = self.db.search(query)

        market_products = {}
        for row in results:
            market_products[row[0]] = row[1]

        return market_products

    def n_products(self):
        market_products = self.n_products_for_each_market()

        tot_products = 0
        for market in market_products:
            tot_products += market_products[market]

        return tot_products

    def get_top_vendors(self, limit=None):
        """
        Retrieve the top n vendors based on the number of products in the marketplace
        """

        last_ts = self.last_timestamp()

        if not last_ts:
            return None

        first_day_ts = first_day_timestamp(last_ts)

        query = "SELECT DISTINCT(vendor), count(name) as qty, round(sum(price),2) as tot_price " \
                f"FROM {DB_NAME}.{self.table_name} " \
                f"WHERE timestamp >= %s AND timestamp <= %s " \
                f"GROUP BY vendor " \
                f"ORDER BY tot_price DESC"

        if limit and isinstance(limit, int) and limit > 0:
            query += " LIMIT %s"
            value = (str(first_day_ts), str(last_ts), limit)
        else:
            value = (str(first_day_ts), str(last_ts))

        header, results = self.db.search(query, value)

        top_vendors = [{"vendor": row[0], "qty": row[1], "tot_price": row[2]} for row in results]

        return top_vendors

    def latest_monthly_sales(self):
        """
        Return the number of sales for each day of the last month, starting from the 1st up to the last day recorder
        """

        latest_ts = self.last_timestamp()
        first_day_ts = first_day_timestamp(latest_ts)

        last_day = datetime.datetime.fromtimestamp(int(latest_ts)).day

        current_date = datetime.datetime.fromtimestamp(int(first_day_ts))
        current_date_ts = int(
            time.mktime(datetime.datetime.strptime(str(current_date), "%Y-%m-%d %H:%M:%S").timetuple()))

        sales = {}
        for i in range(1, last_day+1):
            # Generate timestamp with the next day
            current_date += datetime.timedelta(days=1)

            prev_current_date_ts = current_date_ts
            current_date_ts = int(
                time.mktime(datetime.datetime.strptime(str(current_date), "%Y-%m-%d %H:%M:%S").timetuple()))

            query = f"SELECT COUNT(name) as qty FROM {DB_NAME}.{self.table_name} " \
                    f"WHERE timestamp >= %s AND timestamp < %s;"

            value = (prev_current_date_ts, current_date_ts)

            header, results = self.db.search(query, value)
            if results[0][0] > 0:
                sales[str(i)] = int(results[0][0])



        return sales

    def ta_by_price(self, dataset, country=None, drug=None, market=None, year=None, month=None):
        # Preconditions
        if dataset.lower() == 'drug':
            dataset = 'macro_category'
        if dataset.lower() == 'country':
            dataset = 'ships_from'
        logger.debug(dataset)

        if dataset != 'market' and dataset != 'macro_category' and dataset != 'ships_from':
            raise Exception("Invalid dataset for the trend analysis")

        if dataset == 'market' and market:
            raise Exception("Market must be None, if the ta is applied on the markets")

        if dataset == 'macro_category' and drug:
            raise Exception("Drug must be None, if the ta is applied on the drugs")

        if dataset == 'ships_from' and country:
            raise Exception("Country must be None, if the ta is applied on the countries")

        if not year and not month:
            x_format = '%Y'
            ts_format = '%Y'
            ts = None
        elif year and not month:
            x_format = '%m'
            ts_format = '%Y'
            ts = str(year)
        else:
            x_format = '%d'
            ts_format = '%Y/%m'
            ts = year + "/" + month

        value = [x_format, ts_format]

        # Query build
        attr = ""
        if dataset.lower() == 'market':
            if country and drug:
                attr = "ships_from, macro_category, "
            elif country and not drug:
                attr = "ships_from, "
            elif not country and drug:
                attr = "macro_category, "
        elif dataset.lower() == 'macro_category':
            if country and market:
                attr = "ships_from, market, "
            elif country and not market:
                attr = "ships_from, "
            elif not country and market:
                attr = "market, "
        else:
            logger.debug(market)
            logger.debug(drug)
            if market and drug:
                attr = "market, macro_category, "
            elif market and not drug:
                attr = "market, "
            elif not market and drug:
                attr = "macro_category, "

        # WHERE STATEMENT
        where = ""
        if ts or country or drug or market:
            where = "WHERE"
            clauses = []

            if ts:
                # clauses.append("(dt is null OR dt = %s)")
                clauses.append("dt = %s")
                value.append(ts)
            if country:
                # clauses.append("(ships_from is null OR ships_from = %s)")
                clauses.append("ships_from = %s")
                value.append(country)
            if drug:
                # clauses.append("(macro_category is null OR macro_category = %s)")
                clauses.append("macro_category = %s")
                value.append(drug)
            if market:
                # clauses.append("(market is null OR market = %s)")
                clauses.append("market = %s")
                value.append(market)

            clauses = " AND ".join(clauses)
            where += " " + clauses

        value = tuple(value)

        logger.debug(f"SELECT + GROUP BY Additional attr: {attr}")
        logger.debug(f"WHERE statement: {where}")

        query = f"""
        SELECT * FROM
        (SELECT {dataset}, {attr}DATE_FORMAT(from_unixtime(timestamp), %s) as time_x, DATE_FORMAT(from_unixtime(timestamp),
        %s) as dt, ROUND(SUM(price),2) as tot_price 
        FROM anita.products_cleaned 
        WHERE {dataset} is not null GROUP BY {dataset}, {attr}time_x, dt) as ta_market 
        {where} 
        ORDER BY time_x ASC;
        """

        header, results = self.db.search(query, value)

        logger.debug(query)
        # logger.debug(results)

        time = []
        markets = {}

        for row in results:
            market = row[0]
            date = row[len(row)-3]
            price = row[len(row)-1]

            if date:
                # Change the numerical month into month name
                if year and not month:
                    date = convert_numerical_month_to_str(date)

                if date not in time:
                    time.append(date)

            if market not in markets:
                markets[market] = {}

            if not date:
                markets[market] = None
            else:
                markets[market][date] = price

        return time, markets

    def ta_by_n_products(self, dataset, country=None, drug=None, market=None, year=None, month=None):
        # Preconditions
        if dataset.lower() == 'drug':
            dataset = 'macro_category'
        if dataset.lower() == 'country':
            dataset = 'ships_from'
        logger.debug(f'Dataset: {dataset}')
        logger.debug(f'Country: {country}')
        logger.debug(f'Market: {market}')
        logger.debug(f'Drug: {drug}')

        if dataset != 'market' and dataset != 'macro_category' and dataset != 'ships_from':
            raise Exception("Invalid dataset for the trend analysis")

        if dataset == 'market' and market:
            raise Exception("Market must be None, if the ta is applied on the markets")

        if dataset == 'macro_category' and drug:
            raise Exception("Drug must be None, if the ta is applied on the drugs")

        if dataset == 'ships_from' and country:
            raise Exception("Country must be None, if the ta is applied on the countries")

        if not year and not month:
            x_format = '%Y'
            ts_format = '%Y'
            ts = None
        elif year and not month:
            x_format = '%m'
            ts_format = '%Y'
            ts = str(year)
        else:
            x_format = '%d'
            ts_format = '%Y/%m'
            ts = year + "/" + month

        value = [x_format, ts_format]

        # Query build
        attr = ""
        if dataset.lower() == 'market':
            if country and drug:
                attr = "ships_from, macro_category, "
            elif country and not drug:
                attr = "ships_from, "
            elif not country and drug:
                attr = "macro_category, "
        elif dataset.lower() == 'macro_category':
            if country and market:
                attr = "ships_from, market, "
            elif country and not market:
                attr = "ships_from, "
            elif not country and market:
                attr = "market, "
        else:
            logger.debug(market)
            logger.debug(drug)
            if market and drug:
                attr = "market, macro_category, "
            elif market and not drug:
                attr = "market, "
            elif not market and drug:
                attr = "macro_category, "

        # WHERE STATEMENT
        where = ""
        if ts or country or drug or market:
            where = "WHERE"
            clauses = []

            if ts:
                # clauses.append("(dt is null OR dt = %s)")
                clauses.append("dt = %s")
                value.append(ts)
            if country:
                # clauses.append("(ships_from is null OR ships_from = %s)")
                clauses.append("ships_from = %s")
                value.append(country)
            if drug:
                # clauses.append("(macro_category is null OR macro_category = %s)")
                clauses.append("macro_category = %s")
                value.append(drug)
            if market:
                # clauses.append("(market is null OR market = %s)")
                clauses.append("market = %s")
                value.append(market)

            clauses = " AND ".join(clauses)
            where += " " + clauses

        value = tuple(value)

        logger.debug(f"SELECT + GROUP BY Additional attr: {attr}")
        logger.debug(f"WHERE statement: {where}")

        query = f"""
        SELECT * FROM
        (SELECT {dataset}, {attr}DATE_FORMAT(from_unixtime(timestamp), %s) as time_x, DATE_FORMAT(from_unixtime(timestamp),
        %s) as dt, COUNT(name) as n_price 
        FROM anita.products_cleaned 
        WHERE {dataset} is not null GROUP BY {dataset}, {attr}time_x, dt) as ta_market 
        {where} 
        ORDER BY time_x ASC;
        """

        header, results = self.db.search(query, value)

        logger.debug(query)
        # logger.debug(results)

        time = []
        markets = {}

        for row in results:
            market = row[0]
            date = row[len(row) - 3]
            price = row[len(row) - 1]

            if date:
                # Change the numerical month into month name
                if year and not month:
                    date = convert_numerical_month_to_str(date)

                if date not in time:
                    time.append(date)

            if market not in markets:
                markets[market] = {}

            if not date:
                markets[market] = None
            else:
                markets[market][date] = price

        return time, markets


class VendorAnalysisController:
    def __init__(self):
        self.db = MySqlDB()

    def get_distinct_ships_from(self):
        query = "(SELECT DISTINCT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(ships_from,',',i+1),',',-1)) as country " \
                f"FROM {DB_NAME}.`ints`, {DB_NAME}.`vendor-analysis` " \
                "WHERE ships_from is not NULL) " \
                "UNION " \
                "(SELECT DISTINCT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(ships_from,',',i+1),',',-1)) as country " \
                f"FROM {DB_NAME}.`ints`, {DB_NAME}.`products_cleaned` " \
                "WHERE ships_from is not NULL) " \
                "ORDER BY country;"

        header, results = self.db.search(query)

        countries = [row[0] for row in results]

        return countries

    def n_vendors_per_country(self):
        query = "SELECT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(ships_from,',',i+1),',',-1)) as country, " \
                "count(name) as n_vendors " \
                f"FROM {DB_NAME}.ints, {DB_NAME}.`vendor-analysis` " \
                f"WHERE ships_from is not NULL " \
                f"GROUP BY country"

        header, results = self.db.search(query)

        countries = {}
        for row in results:
            countries[row[0]] = row[1]

        return countries

    def n_vendors_foreach_market(self):
        """
        Number of vendors for each market
        """

        query = f"SELECT market, COUNT(DISTINCT(name)) as n_vendors FROM {DB_NAME}.`vendor-analysis` GROUP BY market;"

        header, results = self.db.search(query)

        market_vendors = {}
        for row in results:
            market_vendors[row[0]] = row[1]

        return market_vendors

    def n_vendors(self):
        market_vendors = self.n_vendors_foreach_market()

        tot_vendors = 0
        for market in market_vendors:
            tot_vendors += market_vendors[market]

        return tot_vendors

    def ta_by_n_vendors(self, dataset, country=None, drug=None, market=None, year=None, month=None):
        # Preconditions
        if dataset.lower() == 'drug':
            dataset = 'macro_category'
        if dataset.lower() == 'country':
            dataset = 'ships_from'
        logger.debug(f'Dataset: {dataset}')
        logger.debug(f'Country: {country}')
        logger.debug(f'Market: {market}')
        logger.debug(f'Drug: {drug}')

        if dataset != 'market' and dataset != 'macro_category' and dataset != 'ships_from':
            raise Exception("Invalid dataset for the trend analysis")

        if dataset == 'market' and market:
            raise Exception("Market must be None, if the ta is applied on the markets")

        if dataset == 'macro_category' and drug:
            raise Exception("Drug must be None, if the ta is applied on the drugs")

        if dataset == 'ships_from' and country:
            raise Exception("Country must be None, if the ta is applied on the countries")

        if not year and not month:
            x_format = '%Y'
            ts_format = '%Y'
            ts = None
        elif year and not month:
            x_format = '%m'
            ts_format = '%Y'
            ts = str(year)
        else:
            x_format = '%d'
            ts_format = '%Y/%m'
            ts = year + "/" + month

        query, value = _ta_query_builder(dataset, 'n. vendors', x_format, ts_format, country, drug, market, ts)

        logger.debug("QUERY")
        logger.debug(query)
        logger.debug("VALUES")
        logger.debug(value)

        header, results = self.db.search(query, value)

        time = []
        datasets = {}

        for row in results:
            dataset_sql = row[0]
            date = row[len(row) - 3]
            n_vendors = row[len(row) - 1]

            if date:
                # Change the numerical month into month name
                if year and not month:
                    date = convert_numerical_month_to_str(date)

                if date not in time:
                    time.append(date)

            if dataset_sql not in datasets:
                datasets[dataset_sql] = {}

            if not date:
                datasets[dataset_sql] = None
            else:
                datasets[dataset_sql][date] = n_vendors

        return time, datasets


def get_markets():
    db = MySqlDB()

    query = f"SELECT DISTINCT(market) from {DB_NAME}.products_cleaned " \
            "UNION " \
            f"SELECT DISTINCT(market) from {DB_NAME}.`vendor-analysis` " \
            "UNION " \
            f"SELECT DISTINCT(market) from {DB_NAME}.reviews;"

    header, results = db.search(query)

    return [row[0] for row in results]


# TO DO: Refactoring with a query builder
def _ta_query_builder(dataset, y, time_x, dt, country=None, drug=None, market=None, date=None):
    query = None
    value = None

    date_attr = ""
    if date:
        date_attr = "dt = %s "
        if country or drug or market:
            date_attr += "AND "
        else:
            date_attr = "WHERE " + date_attr

    if dataset.lower() == 'market' and y.lower() == 'price':
        pass
    elif dataset.lower() == 'market' and y.lower() == 'n. products':
        pass
    elif dataset.lower() == 'market' and y.lower() == 'n. vendors':
        if country and drug:
            query = f"""
            SELECT vendor_drug.market, vendor_drug.country, products_cleaned.macro_category, vendor_drug.time_x, 
            vendor_drug.dt, count(DISTINCT(vendor_drug.name)) as n_vendors 
            FROM (SELECT market, name, TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(ships_from,',',i+1),',',-1)) as country, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as time_x, DATE_FORMAT(from_unixtime(timestamp),%s) as dt
            FROM anita.`vendor-analysis`, anita.ints 
            WHERE name is not null) as vendor_drug
            JOIN anita.products_cleaned ON vendor_drug.name = products_cleaned.vendor
            WHERE {date_attr}country = %s and macro_category = %s
            GROUP BY market, country, macro_category, time_x, dt
            ORDER BY time_x;
            """
            if date:
                value = (time_x, dt, date, country, drug)
            else:
                value = (time_x, dt, country, drug)
        elif country and not drug:
            query = f"""
            SELECT * FROM
            (SELECT market, TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(ships_from,',',i+1),',',-1)) as country, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as time_x, DATE_FORMAT(from_unixtime(timestamp),%s) as dt, 
            COUNT(DISTINCT(name)) as n_vendors FROM anita.`vendor-analysis`, anita.ints 
            WHERE name is not null GROUP BY market, country, time_x, dt) as ta_market
            WHERE {date_attr}country = %s
            ORDER BY time_x;
            """
            if date:
                value = (time_x, dt, date, country)
            else:
                value = (time_x, dt, country)
        elif not country and drug:
            query = f"""
            SELECT ta_market.market, products_cleaned.macro_category, ta_market.time_x, ta_market.dt, 
            COUNT(DISTINCT(ta_market.name)) as n_vendors FROM
            (SELECT market, DATE_FORMAT(from_unixtime(timestamp),%s) as time_x, DATE_FORMAT(from_unixtime(timestamp),%s) 
            as dt, name FROM anita.`vendor-analysis` WHERE name is not null) as ta_market
            JOIN anita.products_cleaned ON ta_market.name = products_cleaned.vendor
            WHERE {date_attr}macro_category = %s
            GROUP BY market, macro_category, time_x, dt
            ORDER BY time_x;
            """
            if date:
                value = (time_x, dt, date, drug)
            else:
                value = (time_x, dt, drug)
        else:
            query = f"""
            SELECT * FROM
            (SELECT market, DATE_FORMAT(from_unixtime(timestamp),%s) as time_x, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as dt, COUNT(DISTINCT(name)) as n_vendors
            FROM anita.`vendor-analysis` WHERE name is not null GROUP BY market, time_x, dt) as ta_market
            {date_attr}
            ORDER BY time_x;
            """
            if date:
                value = (time_x, dt, date)
            else:
                value = (time_x, dt)
    elif dataset.lower() == 'market' and y.lower() == 'n. reviews':
        pass
    elif dataset.lower() == 'macro_category' and y.lower() == 'price':
        pass
    elif dataset.lower() == 'macro_category' and y.lower() == 'n. products':
        pass
    elif dataset.lower() == 'macro_category' and y.lower() == 'n. vendors':
        if country and market:
            query = f"""
            SELECT products_cleaned.macro_category, vendor_drug.country, vendor_drug.market, vendor_drug.time_x, 
            vendor_drug.dt, count(DISTINCT(vendor_drug.name)) as n_vendors FROM
            (SELECT market, name, TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(ships_from,',',i+1),',',-1)) as country, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as time_x, DATE_FORMAT(from_unixtime(timestamp),%s) as dt
            FROM anita.`vendor-analysis`, anita.ints WHERE name is not null AND ships_from is not null) as vendor_drug
            JOIN anita.products_cleaned ON vendor_drug.name = products_cleaned.vendor
            WHERE macro_category is not null AND {date_attr}country = %s AND vendor_drug.market = %s
            GROUP BY macro_category, country, market, time_x, dt
            ORDER BY time_x;
            """
            if date:
                value = (time_x, dt, date, country, market)
            else:
                value = (time_x, dt, country, market)
        elif country and not market:
            query = f"""
            SELECT products_cleaned.macro_category, vendor_drug.country, vendor_drug.time_x, vendor_drug.dt, 
            count(DISTINCT(vendor_drug.name)) as n_vendors FROM
            (SELECT name, TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(ships_from,',',i+1),',',-1)) as country, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as time_x, DATE_FORMAT(from_unixtime(timestamp),%s) as dt
            FROM anita.`vendor-analysis`, anita.ints WHERE name is not null) as vendor_drug
            JOIN anita.products_cleaned ON vendor_drug.name = products_cleaned.vendor
            WHERE macro_category is not null AND {date_attr}country = %s
            GROUP BY macro_category, country, time_x, dt
            ORDER BY time_x;
            """
            if date:
                value = (time_x, dt, date, country)
            else:
                value = (time_x, dt, country)
        elif not country and market:
            query = f"""
            SELECT products_cleaned.macro_category, ta_market.market, ta_market.time_x, ta_market.dt, 
            COUNT(DISTINCT(ta_market.name)) as n_vendors FROM
            (SELECT market, DATE_FORMAT(from_unixtime(timestamp),%s) as time_x, DATE_FORMAT(from_unixtime(timestamp),%s) 
            as dt, name FROM anita.`vendor-analysis` WHERE name is not null) as ta_market
            JOIN anita.products_cleaned ON ta_market.name = products_cleaned.vendor
            WHERE macro_category is not null AND {date_attr}ta_market.market = %s
            GROUP BY macro_category, market, time_x, dt
            ORDER BY time_x;
            """
            if date:
                value = (time_x, dt, date, market)
            else:
                value = (time_x, dt, market)
        else:
            query = f"""
            SELECT macro_category, time_x, dt, COUNT(DISTINCT(name)) as n_vendors FROM
            (SELECT macro_category, DATE_FORMAT(from_unixtime(`vendor-analysis`.timestamp),%s) as time_x, 
            DATE_FORMAT(from_unixtime(`vendor-analysis`.timestamp),%s) as dt, `vendor-analysis`.name
            FROM anita.`vendor-analysis` JOIN anita.products_cleaned ON `vendor-analysis`.name = products_cleaned.vendor 
            WHERE `vendor-analysis`.name is not null AND macro_category is not null) as ta_drug
            {date_attr}
            GROUP BY macro_category, time_x, dt
            ORDER BY time_x;
            """
            if date:
                value = (time_x, dt, date)
            else:
                value = (time_x, dt)
    elif dataset.lower() == 'macro_category' and y.lower() == 'n. reviews':
        pass
    elif dataset.lower() == 'ships_from' and y.lower() == 'price':
        pass
    elif dataset.lower() == 'ships_from' and y.lower() == 'n. products':
        pass
    elif dataset.lower() == 'ships_from' and y.lower() == 'n. vendors':
        if market and drug:
            query = f"""
            SELECT vendor_drug.country, vendor_drug.market, products_cleaned.macro_category, vendor_drug.time_x, 
            vendor_drug.dt, count(DISTINCT(vendor_drug.name)) as n_vendors FROM
            (SELECT market, name, TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(ships_from,',',i+1),',',-1)) as country, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as time_x, DATE_FORMAT(from_unixtime(timestamp),%s) as dt
            FROM anita.`vendor-analysis`, anita.ints 
            WHERE name is not null AND ships_from is not null) as vendor_drug
            JOIN anita.products_cleaned ON vendor_drug.name = products_cleaned.vendor
            WHERE {date_attr}vendor_drug.market = %s AND macro_category = %s
            GROUP BY country, market, macro_category, time_x, dt
            ORDER BY time_x;
            """
            if date:
                value = (time_x, dt, date, market, drug)
            else:
                value = (time_x, dt, market, drug)
        elif market and not drug:
            query = f"""
            SELECT * FROM
            (SELECT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(ships_from,',',i+1),',',-1)) as country, market, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as time_x, DATE_FORMAT(from_unixtime(timestamp),%s) as dt, 
            COUNT(distinct(name)) as n_vendors FROM anita.`vendor-analysis`, anita.ints
            WHERE name is not null AND ships_from is not null
            GROUP BY country, market, time_x, dt) as ta_market
            WHERE {date_attr}market = %s
            ORDER BY time_x;
            """

            if date:
                value = (time_x, dt, date, market)
            else:
                value = (time_x, dt, market)
        elif not market and drug:
            query = f"""
            SELECT vendor_drug.country, products_cleaned.macro_category, vendor_drug.time_x, vendor_drug.dt, 
            count(DISTINCT(vendor_drug.name)) as n_vendors FROM
            (SELECT name, TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(ships_from,',',i+1),',',-1)) as country, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as time_x, DATE_FORMAT(from_unixtime(timestamp),%s) as dt
            FROM anita.`vendor-analysis`, anita.ints 
            WHERE name is not null AND ships_from is not null) as vendor_drug
            JOIN anita.products_cleaned ON vendor_drug.name = products_cleaned.vendor
            WHERE {date_attr}macro_category = %s
            GROUP BY country, macro_category, time_x, dt
            ORDER BY time_x;
            """
            if date:
                value = (time_x, dt, date, drug)
            else:
                value = (time_x, dt, drug)
        else:
            query = f"""
            SELECT * FROM
            (SELECT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(ships_from,',',i+1),',',-1)) as country, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as time_x, DATE_FORMAT(from_unixtime(timestamp),%s) as dt, 
            COUNT(distinct(name)) as n_vendors FROM anita.`vendor-analysis`, anita.ints
            WHERE name is not null AND ships_from is not null GROUP BY country, time_x, dt) as ta_country
            {date_attr}
            ORDER BY time_x;
            """
            if date:
                value = (time_x, dt, date)
            else:
                value = (time_x, dt)
    elif dataset.lower() == 'ships_from' and y.lower() == 'n. reviews':
        pass

    return query, value

