from database.anita import AnitaDB
from markets.bean.Vendor import Vendor


class VendorController(AnitaDB):
    def get_vendors(self):
        vendors = []

        sql = "SELECT * FROM vendor"
        results = self._mysqlDB.search(sql)

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

    def insert_vendor(self, vendor):
        sql = "INSERT INTO vendor (timestamp, market, name, dream_market_positive_rating, " \
              "dream_market_negative_rating, last_seen, since, ships_from, positive_rating, neutral_rating, " \
              "negative_rating, orders_finalized, finalized_early, profile, terms_conditions, pgp) VALUES (%s, %s, " \
              "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        val = (vendor.timestamp, vendor.market, vendor.name, vendor.dream_market_rating[0], vendor.dream_market_rating[1],
               vendor.last_seen, vendor.since, vendor.ships_from, vendor.rating[0], vendor.rating[1], vendor.rating[2],
               vendor.orders_finalized, vendor.finalized_early, vendor.profile, vendor.terms_conditions, vendor.pgp)

        self._mysqlDB.insert(sql, val)

    def insertVendors(self, vendors):
        sql = "INSERT INTO vendor (timestamp, market, name, dream_market_positive_rating, " \
              "dream_market_negative_rating, last_seen, since, ships_from, positive_rating, neutral_rating, " \
              "negative_rating, orders_finalized, finalized_early, profile, terms_conditions, pgp) VALUES (%s, %s, " \
              "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        values = []
        for vendor in vendors:
            val = (vendor.timestamp, vendor.market, vendor.name, vendor.dream_market_rating[0], vendor.dream_market_rating[1],
                   vendor.last_seen, vendor.since, vendor.ships_from, vendor.rating[0], vendor.rating[1], vendor.rating[2],
                   vendor.orders_finalized, vendor.finalized_early, vendor.profile, vendor.terms_conditions, vendor.pgp)

            values.append(val)

        self._mysqlDB.insert(sql, values)