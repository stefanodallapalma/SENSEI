from database.anita import AnitaDB
from markets.bean.Product import Product


class ProductTable(AnitaDB):
    def get_products(self):
        products = []

        sql = "SELECT * FROM product"
        results = self._mysqlDB.search(sql)

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

    def insert_product(self, product):
        sql = "INSERT INTO product (timestamp, market, name, category, subcategory, vendor_name, price_eur, " \
              "price_btc, stock, shipping_options, product_class, escrow_type, ships_from, ships_to, items_sold, " \
              "orders_sold_since, details, terms_and_conditions) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
              "%s, %s, %s, %s, %s, %s, %s)"

        val = (product.timestamp, product.market, product.name, product.category, product.subcategory, product.vendor,
               product.price_eur, product.price_btc, product.stock, self.list_to_string(product.shipping_options),
               product.product_class, product.escrow_type, product.ships_from, self.list_to_string(product.ships_to),
               product.items_sold, product.orders_sold_since, product.details, product.terms_and_conditions)

        self._mysqlDB.insert(sql, val)

    def insert_products(self, products):
        sql = "INSERT INTO product (timestamp, market, name, category, subcategory, vendor_name, price_eur, " \
              "price_btc, stock, shipping_options, product_class, escrow_type, ships_from, ships_to, items_sold, " \
              "orders_sold_since, details, terms_and_conditions) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
              "%s, %s, %s, %s, %s, %s, %s)"

        values = []
        for product in products:
            val = (product.timestamp, product.market, product.name, product.category, product.subcategory, product.vendor,
                   product.price_eur, product.price_btc, product.stock, self.list_to_string(product.shipping_options),
                   product.product_class, product.escrow_type, product.ships_from, self.list_to_string(product.ships_to),
                   product.items_sold, product.orders_sold_since, product.details, product.terms_and_conditions)

            values.append(val)

        self._mysqlDB.insert(sql, values)