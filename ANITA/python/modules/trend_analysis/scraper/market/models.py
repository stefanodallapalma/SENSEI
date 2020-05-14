class WebPage:
    """Contains general information about the specific file"""

    def __init__(self, file_name, market, page_type, date, soup):
        self.file_name = file_name
        self.market = market
        self.page_type = page_type
        self.soup = soup
        self.date = date


class Product:
    """Product model"""

    def __init__(self, product_name, vendor, ships_from, ships_to, price, price_eur, info, feedback):
        self.product_name = product_name
        self.vendor = vendor
        self.ships_from = ships_from
        self.ships_to = ships_to
        self.ships_to = ships_to
        self.price = price
        self.price_eur = price_eur
        self.info = info
        self.feedback = feedback


class Vendor:
    """Scrape the soup for vendor"""

    def __init__(self, name, score, score_normalized, registration, registration_deviation, last_login,
                 last_login_deviation, sales, info, feedback):
        self.name = name
        self.score = score
        self.score_normalized = score_normalized
        self.registration = registration
        self.registration_deviation = registration_deviation
        self.last_login = last_login
        self.last_login_deviation = last_login_deviation
        self.sales = sales
        self.info = info
        self.feedback = feedback
