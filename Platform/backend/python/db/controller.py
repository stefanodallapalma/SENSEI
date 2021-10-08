import datetime
import time
import logging
import requests
from pypika import Query, Table, Field

from db.mysql_connection import MySqlDB
from utils import first_day_timestamp, convert_numerical_month_to_str

DB_NAME = "anita"
RESTCOUNTRIES_API_URL = "https://restcountries.com/v3.1/name/"
logger = logging.getLogger("Controller")


class CountryController:
    def __init__(self):
        self.db = MySqlDB()
        self.table_name = "country"

    def get_countries_alpha2code(self):
        query = f"SELECT country, alpha2code FROM {DB_NAME}.{self.table_name};"
        header, results = self.db.search(query)

        countries = {}
        for row in results:
            countries[row[0]] = row[1]

        return countries

    def get_alpha2code(self, country):
        query = f"SELECT alpha2code FROM {DB_NAME}.{self.table_name} WHERE country = %s;"
        value = (country,)
        header, results = self.db.search(query, value)

        if not results:
            return None

        return results[0][0]

    def add_country(self, country):
        # Restcountry api used to retrieve the country info
        url = RESTCOUNTRIES_API_URL + country + "?fullText=true"
        response = requests.get(url)

        if isinstance(response.json(), dict) and response.json()["status"] == 404:
            raise Exception("RESTCOUNTRY API: Invalid country.")

        alpha2code = None
        alpha3code = None

        for country_json in response.json():
            name = country_json["name"]["common"].lower()
            native_names = [country_json["name"]["nativeName"][key]["common"].lower()
                            for key in country_json["name"]["nativeName"]
                            if country_json["name"]["nativeName"][key]["common"].lower() == "india"]

            if name == country.lower() or native_names or country.lower() in name:
                alpha2code = country_json["cca2"]
                alpha3code = country_json["cca3"]

        # Database INSERT
        query = f"INSERT INTO {DB_NAME}.{self.table_name} (`country`, `alpha2code`, `alpha3code`) " \
                f"VALUES (%s, %s, %s);"
        values = (country, alpha2code, alpha3code)

        status = self.db.insert(query, values)

        if not status:
            return None

        return alpha2code


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

    def n_products_foreach_market(self):
        query = f"SELECT DISTINCT(market), COUNT(name) as n_products " \
                f"FROM {DB_NAME}.products_cleaned GROUP BY market;"

        header, results = self.db.search(query)

        markets = {}
        for row in results:
            if row[0] not in markets:
                markets[row[0]] = {}

            markets[row[0]] = row[1]

        return markets

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

    def n_products_for_each_vendor(self, market=None):
        if not market:
            query = f"SELECT DISTINCT(vendor), COUNT(DISTINCT(name)) as n_products FROM {DB_NAME}.products_cleaned " \
                    f"GROUP BY vendor ORDER BY n_products DESC;"

            # query = f"SELECT DISTINCT(market), vendor, COUNT(DISTINCT(name)) FROM {DB_NAME}.products_cleaned " \
            #         f"GROUP BY market, vendor;"

            header, results = self.db.search(query)

            vendors = {}
            for row in results:
                vendors[row[0]] = row[1]
        else:
            query = f"SELECT DISTINCT(market), vendor, COUNT(DISTINCT(name)) as n_products FROM {DB_NAME}.products_cleaned " \
                    f"WHERE market = %s GROUP BY market, vendor ORDER BY n_products DESC;"
            value = (market,)

            header, results = self.db.search(query, value)

            vendors = {}

            for row in results:
                vendors[row[1]] = row[2]

        return vendors

    def n_drugs(self, vendor):
        query = "SELECT vendor, macro_category, COUNT(macro_category) FROM " \
                f"(SELECT DISTINCT(vendor), name, macro_category FROM {DB_NAME}.products_cleaned " \
                "GROUP BY vendor, name, macro_category) as vendor_drugs " \
                "WHERE vendor = %s GROUP BY vendor, macro_category;"
        value = (vendor,)

        header, results = self.db.search(query, value)

        drugs = {}
        for row in results:
            drugs[row[1]] = row[2]

        return drugs

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

    def get_markets(self):
        query = f"SELECT DISTINCT(market) from {DB_NAME}.products_cleaned WHERE market is not null;"
        header, results = self.db.search(query)
        return [row[0] for row in results]

    def get_countries(self):
        query = f"SELECT DISTINCT(ships_from) from {DB_NAME}.products_cleaned WHERE ships_from is not null;"
        header, results = self.db.search(query)
        return [row[0] for row in results]

    def get_drugs(self):
        query = f"SELECT DISTINCT(macro_category) from {DB_NAME}.products_cleaned WHERE macro_category is not null;"
        header, results = self.db.search(query)
        return [row[0] for row in results]

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

        query, value = _ta_query_builder(dataset, 'price', x_format, ts_format, country, drug, market, ts)

        logger.debug("QUERY")
        logger.debug(query)
        logger.debug("VALUES")
        logger.debug(value)

        header, results = self.db.search(query, value)

        logger.debug("RESULTS")
        logger.debug(results)

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

        query, value = _ta_query_builder(dataset, 'price', x_format, ts_format, country, drug, market, ts)

        logger.debug("QUERY")
        logger.debug(query)
        logger.debug("VALUES")
        logger.debug(value)

        header, results = self.db.search(query, value)

        logger.debug("HEADER")
        logger.debug(header)
        logger.debug("RESULTS")
        logger.debug(results)

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

    def search_vendors(self, vendor_query, limit=None):
        query = f"SELECT DISTINCT(name) FROM {DB_NAME}.`vendor-analysis` WHERE name LIKE %s ORDER BY name"
        value = (vendor_query + "%",)

        if limit:
            query += " LIMIT " + str(limit)

        header, results = self.db.search(query, value)

        return [row[0] for row in results]

    def get_vendor(self, name, market):
        query = 'SELECT name, market, normalized_score as "Score (normalized)", email, "phone number", wickr, ' \
                'ships_from as "Ships from", ships_to as "Ships to", COUNT(timestamp) as snapshots FROM ' \
                f'{DB_NAME}.`vendor-analysis` WHERE name = %s AND market = %s ' \
                f'GROUP BY name, market, normalized_score, email, wickr, ships_from, ships_to;'

        values = (name, market)

        header, results = self.db.search(query, values)

        if not results:
            return None

        return dict(zip(header, results[0]))

    def get_general_vendors(self, vendor_query):
        """
        Function used to retrieve the following vendor's information: vendor's name, marketplace(s), country
        """

        query = f"SELECT DISTINCT(name), market, ships_from FROM {DB_NAME}.`vendor-analysis` WHERE name LIKE %s " \
                "GROUP BY name, market, ships_from;"
        value = (vendor_query + "%",)

        header, results = self.db.search(query, value)

        vendors = []
        for row in results:
            name = row[0]
            market = row[1]
            country = [val.strip() for val in row[2].split(",")] if row[2] else None

            vendors.append({"name": name, "market": market, "country": country})

        return vendors

    def get_distinct_vendor_names(self):
        query = f"SELECT DISTINCT(name) FROM {DB_NAME}.`vendor-analysis` WHERE name is not null;"
        header, results = self.db.search(query)

        return [row[0] for row in results]

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

    def get_vendors_foreach_market(self):
        query = f"SELECT DISTINCT(market), name FROM {DB_NAME}.`vendor-analysis`;"
        header, results = self.db.search(query)

        markets = {}
        for row in results:
            if row[0] not in markets:
                markets[row[0]] = [row[1]]
            else:
                markets[row[0]].append(row[1])

        return markets

    def n_market_product_foreach_vendor(self):
        query = "SELECT vendor_markets.name, n_markets, COUNT(products_cleaned.name) as n_products FROM " \
                "(SELECT name, COUNT(market) as n_markets FROM " \
                f"(SELECT DISTINCT(name), market FROM {DB_NAME}.`vendor-analysis`) as vendor_market " \
                "GROUP BY name) as vendor_markets " \
                f"JOIN {DB_NAME}.products_cleaned ON vendor_markets.name = products_cleaned.vendor " \
                "GROUP BY vendor_markets.name, n_markets;"

        header, results = self.db.search(query)

        vendors = {}
        for row in results:
            vendors[row[0]] = {"N. Markets": row[1], "N. Products": row[2]}

        return vendors

    def n_products_foreach_market_vendor(self):
        query = f"SELECT DISTINCT(vendor), market, COUNT(name) as n_products " \
                f"FROM {DB_NAME}.products_cleaned GROUP BY vendor, market;"

        header, results = self.db.search(query)

        vendors = {}
        for row in results:
            if row[0] not in vendors:
                vendors[row[0]] = {}

            vendors[row[0]][row[1]] = row[2]

        return vendors

    def n_markets_foreach_vendor(self):
        query = "SELECT name, COUNT(market) as n_markets FROM (SELECT DISTINCT(name), market " \
                f"FROM {DB_NAME}.`vendor-analysis`) as vendor_market GROUP BY name;"
        header, results = self.db.search(query)

        vendors = {}
        for row in results:
            vendors[row[0]] = row[1]

        return vendors


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
        if country and drug:
            query = f"""
            SELECT * FROM
            (SELECT market, ships_from, macro_category, DATE_FORMAT(from_unixtime(timestamp), %s) as time_x, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as dt, ROUND(SUM(price),2) as tot_price 
            FROM anita.products_cleaned 
            WHERE market is not null GROUP BY market, ships_from, macro_category, time_x, dt) as ta_market 
            WHERE {date_attr}ships_from = %s AND macro_category = %s 
            ORDER BY time_x ASC;
            """
            if date:
                value = (time_x, dt, date, country, drug)
            else:
                value = (time_x, dt, country, drug)
        elif country and not drug:
            query = f"""
            SELECT * FROM
            (SELECT market, ships_from, DATE_FORMAT(from_unixtime(timestamp), %s) as time_x, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as dt, ROUND(SUM(price),2) as tot_price 
            FROM anita.products_cleaned 
            WHERE market is not null GROUP BY market, ships_from, time_x, dt) as ta_market 
            WHERE {date_attr}ships_from = %s 
            ORDER BY time_x ASC;
            """
            if date:
                value = (time_x, dt, date, country)
            else:
                value = (time_x, dt, country)
        elif not country and drug:
            query = f"""
            SELECT * FROM
            (SELECT market, macro_category, DATE_FORMAT(from_unixtime(timestamp), %s) as time_x, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as dt, ROUND(SUM(price),2) as tot_price 
            FROM anita.products_cleaned 
            WHERE market is not null GROUP BY market, macro_category, time_x, dt) as ta_market 
            WHERE {date_attr}macro_category = %s 
            ORDER BY time_x ASC;
            """
            if date:
                value = (time_x, dt, date, drug)
            else:
                value = (time_x, dt, drug)
        else:
            query = f"""
            SELECT * FROM
            (SELECT market, DATE_FORMAT(from_unixtime(timestamp), %s) as time_x, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as dt, ROUND(SUM(price),2) as tot_price 
            FROM anita.products_cleaned 
            WHERE market is not null GROUP BY market, time_x, dt) as ta_market 
            {date_attr} 
            ORDER BY time_x ASC;
            """
            if date:
                value = (time_x, dt, date)
            else:
                value = (time_x, dt)
    elif dataset.lower() == 'market' and y.lower() == 'n. products':
        if country and drug:
            query = f"""
            SELECT * FROM
            (SELECT market, ships_from, macro_category, DATE_FORMAT(from_unixtime(timestamp), %s) as time_x, DATE_FORMAT(from_unixtime(timestamp),
            %s) as dt, COUNT(name) as n_price 
            FROM anita.products_cleaned 
            WHERE market is not null GROUP BY market, ships_from, macro_category, time_x, dt) as ta_market 
            WHERE {date_attr}country = %s AND macro_category = %s 
            ORDER BY time_x ASC;
            """
            if date:
                value = (time_x, dt, date, country, drug)
            else:
                value = (time_x, dt, country, drug)
        elif country and not drug:
            query = f"""
            SELECT * FROM
            (SELECT market, ships_from, DATE_FORMAT(from_unixtime(timestamp), %s) as time_x, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as dt, COUNT(name) as n_price 
            FROM anita.products_cleaned 
            WHERE market is not null GROUP BY market, ships_from, time_x, dt) as ta_market 
            WHERE {date_attr}country = %s 
            ORDER BY time_x ASC;
            """
            if date:
                value = (time_x, dt, date, country)
            else:
                value = (time_x, dt, country)
        elif not country and drug:
            query = f"""
            SELECT * FROM
            (SELECT market, macro_category, DATE_FORMAT(from_unixtime(timestamp), %s) as time_x, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as dt, COUNT(name) as n_price 
            FROM anita.products_cleaned 
            WHERE market is not null GROUP BY market, macro_category, time_x, dt) as ta_market 
            WHERE {date_attr}macro_category = %s 
            ORDER BY time_x ASC;
            """
            if date:
                value = (time_x, dt, date, drug)
            else:
                value = (time_x, dt, drug)
        else:
            query = f"""
            SELECT * FROM
            (SELECT market, DATE_FORMAT(from_unixtime(timestamp), %s) as time_x, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as dt, COUNT(name) as n_price 
            FROM anita.products_cleaned 
            WHERE market is not null GROUP BY market, time_x, dt) as ta_market 
            {date_attr} 
            ORDER BY time_x ASC;
            """
            if date:
                value = (time_x, dt, date)
            else:
                value = (time_x, dt)
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
        if country and drug:
            query = f"""
            """
            if date:
                value = (time_x, dt, date, country, drug)
            else:
                value = (time_x, dt, country, drug)
        elif country and not drug:
            query = f"""
            """
            if date:
                value = (time_x, dt, date, country)
            else:
                value = (time_x, dt, country)
        elif not country and drug:
            query = f"""
            """
            if date:
                value = (time_x, dt, date, drug)
            else:
                value = (time_x, dt, drug)
        else:
            query = f"""
            """
            if date:
                value = (time_x, dt, date)
            else:
                value = (time_x, dt)
    elif dataset.lower() == 'macro_category' and y.lower() == 'price':
        if market and country:
            query = f"""
            SELECT * FROM
            (SELECT macro_category, market, ships_from, DATE_FORMAT(from_unixtime(timestamp), %s) as time_x, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as dt, ROUND(SUM(price),2) as tot_price 
            FROM anita.products_cleaned 
            WHERE macro_category is not null GROUP BY macro_category, market, ships_from, time_x, dt) as ta_market 
            WHERE {date_attr}market = %s AND ships_from = %s 
            ORDER BY time_x ASC;
            """
            if date:
                value = (time_x, dt, date, market, country)
            else:
                value = (time_x, dt, market, country)
        elif market and not country:
            query = f"""
            SELECT * FROM
            (SELECT macro_category, market, DATE_FORMAT(from_unixtime(timestamp), %s) as time_x, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as dt, ROUND(SUM(price),2) as tot_price 
            FROM anita.products_cleaned 
            WHERE macro_category is not null GROUP BY macro_category, market, time_x, dt) as ta_market 
            WHERE {date_attr}market = %s 
            ORDER BY time_x ASC;
            """
            if date:
                value = (time_x, dt, date, market)
            else:
                value = (time_x, dt, market)
        elif not market and country:
            query = f"""
            SELECT * FROM
            (SELECT macro_category, ships_from, DATE_FORMAT(from_unixtime(timestamp), %s) as time_x, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as dt, ROUND(SUM(price),2) as tot_price 
            FROM anita.products_cleaned 
            WHERE macro_category is not null GROUP BY macro_category, ships_from, time_x, dt) as ta_market 
            WHERE {date_attr}ships_from = %s 
            ORDER BY time_x ASC;
            """
            if date:
                value = (time_x, dt, date, country)
            else:
                value = (time_x, dt, country)
        else:
            query = f"""
            SELECT * FROM
            (SELECT macro_category, DATE_FORMAT(from_unixtime(timestamp), %s) as time_x, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as dt, ROUND(SUM(price),2) as tot_price 
            FROM anita.products_cleaned 
            WHERE macro_category is not null GROUP BY macro_category, time_x, dt) as ta_market 
            {date_attr} 
            ORDER BY time_x ASC;
            """
            if date:
                value = (time_x, dt, date)
            else:
                value = (time_x, dt)
    elif dataset.lower() == 'macro_category' and y.lower() == 'n. products':
        if market and country:
            query = f"""
            SELECT * FROM
            (SELECT macro_category, market, ships_from, DATE_FORMAT(from_unixtime(timestamp), %s) as time_x, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as dt, COUNT(name) as n_price 
            FROM anita.products_cleaned 
            WHERE macro_category is not null GROUP BY macro_category, market, ships_from, time_x, dt) as ta_market 
            WHERE {date_attr}market = %s AND country = %s 
            ORDER BY time_x ASC;
            """
            if date:
                value = (time_x, dt, date, market, country)
            else:
                value = (time_x, dt, market, country)
        elif market and not country:
            query = f"""
            SELECT * FROM
            (SELECT macro_category, market, DATE_FORMAT(from_unixtime(timestamp), %s) as time_x, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as dt, COUNT(name) as n_price 
            FROM anita.products_cleaned 
            WHERE macro_category is not null GROUP BY macro_category, market, time_x, dt) as ta_market 
            WHERE {date_attr}market = %s 
            ORDER BY time_x ASC;
            """
            if date:
                value = (time_x, dt, date, market)
            else:
                value = (time_x, dt, market)
        elif not market and country:
            query = f"""
            SELECT * FROM
            (SELECT macro_category, ships_from, DATE_FORMAT(from_unixtime(timestamp), %s) as time_x, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as dt, COUNT(name) as n_price 
            FROM anita.products_cleaned 
            WHERE macro_category is not null GROUP BY macro_category, ships_from, time_x, dt) as ta_market 
            WHERE {date_attr}country = %s 
            ORDER BY time_x ASC;
            """
            if date:
                value = (time_x, dt, date, country)
            else:
                value = (time_x, dt, country)
        else:
            query = f"""
            SELECT * FROM
            (SELECT macro_category, DATE_FORMAT(from_unixtime(timestamp), %s) as time_x, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as dt, COUNT(name) as n_price 
            FROM anita.products_cleaned 
            WHERE macro_category is not null GROUP BY macro_category, time_x, dt) as ta_market 
            {date_attr} 
            ORDER BY time_x ASC;
            """
            if date:
                value = (time_x, dt, date)
            else:
                value = (time_x, dt)
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
        if market and country:
            query = f"""
            """
            if date:
                value = (time_x, dt, date, market, country)
            else:
                value = (time_x, dt, market, country)
        elif market and not country:
            query = f"""
            """
            if date:
                value = (time_x, dt, date, market)
            else:
                value = (time_x, dt, market)
        elif not market and country:
            query = f"""
            """
            if date:
                value = (time_x, dt, date, country)
            else:
                value = (time_x, dt, country)
        else:
            query = f"""
            """
            if date:
                value = (time_x, dt, date)
            else:
                value = (time_x, dt)
    elif dataset.lower() == 'ships_from' and y.lower() == 'price':
        if market and drug:
            query = f"""
            SELECT * FROM 
            (SELECT ships_from, market, macro_category, DATE_FORMAT(from_unixtime(timestamp), %s) as time_x, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as dt, ROUND(SUM(price),2) as tot_price 
            FROM anita.products_cleaned 
            WHERE ships_from is not null GROUP BY ships_from, market, macro_category, time_x, dt) as ta_market 
            WHERE {date_attr}market = %s AND macro_category = %s 
            ORDER BY time_x ASC;
            """
            if date:
                value = (time_x, dt, date, market, drug)
            else:
                value = (time_x, dt, market, drug)
        elif market and not drug:
            query = f"""
            SELECT * FROM
            (SELECT ships_from, market, DATE_FORMAT(from_unixtime(timestamp), %s) as time_x, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as dt, ROUND(SUM(price),2) as tot_price 
            FROM anita.products_cleaned 
            WHERE ships_from is not null GROUP BY ships_from, market, time_x, dt) as ta_market 
            WHERE {date_attr}market = %s 
            ORDER BY time_x ASC;
            """
            if date:
                value = (time_x, dt, date, market)
            else:
                value = (time_x, dt, market)
        elif not market and drug:
            query = f"""
            SELECT * FROM 
            (SELECT ships_from, macro_category, DATE_FORMAT(from_unixtime(timestamp), %s) as time_x, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as dt, ROUND(SUM(price),2) as tot_price 
            FROM anita.products_cleaned 
            WHERE ships_from is not null GROUP BY ships_from, macro_category, time_x, dt) as ta_market 
            WHERE {date_attr}macro_category = %s 
            ORDER BY time_x ASC;
            """
            if date:
                value = (time_x, dt, date, drug)
            else:
                value = (time_x, dt, drug)
        else:
            query = f"""
            SELECT * FROM
            (SELECT ships_from, DATE_FORMAT(from_unixtime(timestamp), %s) as time_x, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as dt, ROUND(SUM(price),2) as tot_price 
            FROM anita.products_cleaned 
            WHERE ships_from is not null GROUP BY ships_from, time_x, dt) as ta_market 
            {date_attr} 
            ORDER BY time_x ASC;
            """
            if date:
                value = (time_x, dt, date)
            else:
                value = (time_x, dt)
    elif dataset.lower() == 'ships_from' and y.lower() == 'n. products':
        if market and drug:
            query = f"""
            SELECT * FROM
            (SELECT ships_from, market, macro_category, DATE_FORMAT(from_unixtime(timestamp), %s) as time_x, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as dt, COUNT(name) as n_price 
            FROM anita.products_cleaned 
            WHERE ships_from is not null GROUP BY ships_from, market, macro_category, time_x, dt) as ta_market 
            WHERE {date_attr}market = %s AND macro_category = %s 
            ORDER BY time_x ASC;
            """
            if date:
                value = (time_x, dt, date, market, drug)
            else:
                value = (time_x, dt, market, drug)
        elif market and not drug:
            query = f"""
            SELECT * FROM
            (SELECT ships_from, market, DATE_FORMAT(from_unixtime(timestamp), %s) as time_x, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as dt, COUNT(name) as n_price 
            FROM anita.products_cleaned 
            WHERE ships_from is not null GROUP BY ships_from, market, time_x, dt) as ta_market 
            WHERE {date_attr}market = %s 
            ORDER BY time_x ASC;
            """
            if date:
                value = (time_x, dt, date, market)
            else:
                value = (time_x, dt, market)
        elif not market and drug:
            query = f"""
            SELECT * FROM
            (SELECT ships_from, macro_category, DATE_FORMAT(from_unixtime(timestamp), %s) as time_x, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as dt, COUNT(name) as n_price 
            FROM anita.products_cleaned 
            WHERE ships_from is not null GROUP BY ships_from, macro_category, time_x, dt) as ta_market 
            WHERE {date_attr}market = %s AND macro_category = %s 
            ORDER BY time_x ASC;
            """
            if date:
                value = (time_x, dt, date, drug)
            else:
                value = (time_x, dt, drug)
        else:
            query = f"""
            SELECT * FROM
            (SELECT ships_from, DATE_FORMAT(from_unixtime(timestamp), %s) as time_x, 
            DATE_FORMAT(from_unixtime(timestamp),%s) as dt, COUNT(name) as n_price 
            FROM anita.products_cleaned 
            WHERE ships_from is not null GROUP BY ships_from, time_x, dt) as ta_market 
            {date_attr} 
            ORDER BY time_x ASC;
            """
            if date:
                value = (time_x, dt, date)
            else:
                value = (time_x, dt)
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
        if market and drug:
            query = f"""
            """
            if date:
                value = (time_x, dt, date, market, drug)
            else:
                value = (time_x, dt, market, drug)
        elif market and not drug:
            query = f"""
            """
            if date:
                value = (time_x, dt, date, market)
            else:
                value = (time_x, dt, market)
        elif not market and drug:
            query = f"""
            """
            if date:
                value = (time_x, dt, date, drug)
            else:
                value = (time_x, dt, drug)
        else:
            query = f"""
            """
            if date:
                value = (time_x, dt, date)
            else:
                value = (time_x, dt)

    return query, value

