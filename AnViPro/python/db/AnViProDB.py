from db.MySqlDB import MySqlDB
from scraper.bean.Product import Product
from scraper.bean.Vendor import Vendor

class AnViProDB:


    def __init__(self, db_parameters_path):
        self._mysqlDB = MySqlDB(db_parameters_path)

    def getProduct(self):
        pass

    def getVendor(self):
        pass

    def getProducts(self):
        products = []

        sql = "SELECT * FROM product"
        results = self._mysqlDB.select(sql)

        for result in results:
            product = Product()

            product.timestamp = result[0]
            product.market = result[1]
            product.name = result[3]
            product.category = result[4]
            product.subcategory = result[5]
            product.vendor = result[6]
            product.price_eur = result[7]
            product.price_btc = result[8]
            product.stock = result[9]

            product.shipping_options = []
            shipping_options = [x for x in result[10].split(',')]
            for shipping_option in shipping_options:
                product.shipping_options.append(shipping_option.lstrip())

            product.product_class = result[11]
            product.escrow_type = result[12]
            product.ships_from = result[13]

            product.ships_to = []
            ships_to = [x for x in result[14].split(',')]
            for ship_to in ships_to:
                product.ships_to.append(ship_to.lstrip())

            product.items_sold = result[15]
            product.orders_sold_since = result[16]
            product.details = result[17]
            product.terms_and_conditions = result[18]

            products.append(product)

        return products

    def getVendors(self):
        vendors = []

        sql = "SELECT * FROM vendor"
        results = self._mysqlDB.select(sql)

        for result in results:
            vendor = Vendor()

            vendor.timestamp = result[0]
            vendor.market = result[1]
            vendor.name = result[2]

            dream_market_positive_rating = result[3]
            dream_market_negative_rating = result[4]
            vendor.dream_market_rating = [dream_market_positive_rating, dream_market_negative_rating]

            vendor.last_seen = result[5]
            vendor.since = result[6]
            vendor.ships_from = result[7]

            positive_rating = result[8]
            neutral_rating = result[9]
            negative_rating = result[10]
            vendor.rating = [positive_rating, neutral_rating, negative_rating]

            vendor.orders_finalized = result[11]
            vendor.finalized_early = result[12]
            vendor.profile = result[13]
            vendor.terms_conditions = result[14]
            vendor.pgp = result[15]

            vendors.append(vendor)

        return vendors

    def insertProduct(self, product):
        sql = "INSERT INTO product (name, category, subcategory, idVendor, price_eur, price_btc, stock, " \
              "shipping_options, product_class, escrow_type, ships_from, ships_to, items_sold, orders_sold_since, " \
              "details, terms_and_conditions, idFeedback) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
              "%s, %s, %s, %s, %s)"

        val = (product.name, product.category, product.subcategory, 1, product.price_eur, product.price_btc,
               product.stock, self.list_to_string(product.shipping_options), product.product_class,
               product.escrow_type, product.ships_from, self.list_to_string(product.ships_to),
               product.items_sold, product.orders_sold_since, product.details, product.terms_and_conditions, 1)

        self._mysqlDB.insert(sql, val)

    def insertProducts(self, products):
        sql = "INSERT INTO product (timestamp, market, name, category, subcategory, vendor_name, price_eur, price_btc, stock, " \
              "shipping_options, product_class, escrow_type, ships_from, ships_to, items_sold, orders_sold_since, " \
              "details, terms_and_conditions) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
              "%s, %s, %s, %s, %s, %s)"

        values = []
        for product in products:
            val = (product.timestamp, product.market, product.name, product.category, product.subcategory, product.vendor,
                   product.price_eur, product.price_btc, product.stock, self.list_to_string(product.shipping_options),
                   product.product_class, product.escrow_type, product.ships_from, self.list_to_string(product.ships_to),
                   product.items_sold, product.orders_sold_since, product.details, product.terms_and_conditions)

            values.append(val)

        self._mysqlDB.insert_many(sql, values)

    def insertVendor(self, vendor):
        sql = "INSERT INTO vendor (name, dream_market_positive_rating, dream_market_negative_rating, last_seen, " \
              "since, ships_from, positive_rating, neutral_rating, negative_rating, orders_finalized, " \
              "finalized_early, profile, terms_conditions, pgp, idFeedback) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        val = (vendor.name, vendor.dream_market_rating[0], vendor.dream_market_rating[1], vendor.last_seen,
               vendor.since, vendor.ships_from, vendor.rating[0], vendor.rating[1], vendor.rating[2],
               vendor.orders_finalized, vendor.finalized_early, vendor.profile, vendor.terms_conditions, vendor.pgp, 1)

        self._mysqlDB.insert(sql, val)

    def insertVendors(self, vendors):
        sql = "INSERT INTO vendor (timestamp, market, name, dream_market_positive_rating, dream_market_negative_rating, last_seen, " \
              "since, ships_from, positive_rating, neutral_rating, negative_rating, orders_finalized, " \
              "finalized_early, profile, terms_conditions, pgp) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        values = []
        for vendor in vendors:
            val = (vendor.timestamp, vendor.market, vendor.name, vendor.dream_market_rating[0], vendor.dream_market_rating[1],
                   vendor.last_seen, vendor.since, vendor.ships_from, vendor.rating[0], vendor.rating[1], vendor.rating[2],
                   vendor.orders_finalized, vendor.finalized_early, vendor.profile, vendor.terms_conditions, vendor.pgp)

            values.append(val)

        self._mysqlDB.insert_many(sql, values)


    def list_to_string(self, elements):
        to_string = ""
        i = 1
        for element in elements:
            to_string += element
            if i < len(elements):
                to_string += ", "
            i += 1

        return to_string