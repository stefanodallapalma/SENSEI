class WebPage:
    """Contains general information about the specific file"""

    def __init__(self, file_name, market, page_type, date, soup):
        self.file_name = file_name
        self.market = market
        self.page_type = page_type
        self.soup = soup
        self.date = date

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        self._file_name = value

    @property
    def market(self):
        return self._market

    @market.setter
    def market(self, value):
        self._market = value

    @property
    def page_type(self):
        return self._page_type

    @page_type.setter
    def page_type(self, value):
        self._page_type = value

    @property
    def soup(self):
        return self._soup

    @soup.setter
    def soup(self, value):
        self._soup = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value


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

    @property
    def product_name(self):
        return self._product_name

    @product_name.setter
    def product_name(self, value):
        self._product_name = value

    @property
    def vendor(self):
        return self._vendor

    @vendor.setter
    def vendor(self, value):
        self._vendor = value

    @property
    def ships_from(self):
        return self._ships_from

    @ships_from.setter
    def ships_from(self, value):
        self._ships_from = value

    @property
    def ships_to(self):
        return self._ships_to

    @ships_to.setter
    def ships_to(self, value):
        self._ships_to = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    @property
    def price_eur(self):
        return self._price_eur

    @price_eur.setter
    def price_eur(self, value):
        self._price_eur = value

    @property
    def info(self):
        return self._info

    @info.setter
    def info(self, value):
        self._info = value

    @property
    def feedback(self):
        return self._feedback

    @feedback.setter
    def feedback(self, value):
        self._feedback = value


class Vendor:
    """Scrape the soup for product"""

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

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

    @property
    def score_normalized(self):
        return self._score_normalized

    @score_normalized.setter
    def score_normalized(self, value):
        self._score_normalized = value

    @property
    def registration(self):
        return self._registration

    @registration.setter
    def registration(self, value):
        self._registration = value

    @property
    def registration_deviation(self):
        return self._registration_deviation

    @registration_deviation.setter
    def registration_deviation(self, value):
        self._registration_deviation = value

    @property
    def last_login(self):
        return self._last_login

    @last_login.setter
    def last_login(self, value):
        self._last_login = value

    @property
    def last_login_deviation(self):
        return self._last_login_deviation

    @last_login_deviation.setter
    def last_login_deviation(self, value):
        self._last_login_deviation = value

    @property
    def sales(self):
        return self._sales

    @sales.setter
    def sales(self, value):
        self._sales = value

    @property
    def info(self):
        return self._info

    @info.setter
    def info(self, value):
        self._info = value

    @property
    def feedback(self):
        return self._feedback

    @feedback.setter
    def feedback(self, value):
        self._feedback = value


    def get_feedback(self, soup, file_date):
        """Returns the feedback"""
        try:
            feedback_list = self.scraper.v_feedback(soup)
            # use the Product.feedback_handler to adapt the time
            return Product.feedback_handler(feedback_list, file_date)
        except:
            return None

    @staticmethod
    def calculate_time_since(since, file_date):
        """Calculates the date in a timestamp
        since is the string with the relative date, mostly in this format: '2 months ago'
        file_date is the date of the file itself"""
        since = since.lower().split()
        timestamp = file_date
        time_since_unix = 0

        # add the time mentioned in the string to the unix time
        for p, item in enumerate(since):
            if 'today' in item:
                return file_date

            if 'years' in item:
                years = since[p - 1]
                time_since_unix += 31556926 * int(years)
            elif 'year' in item:
                time_since_unix += 31556926
            if 'months' in item:
                months = since[p - 1]
                time_since_unix += 2629743.83 * int(months)
            elif 'month' in item:
                time_since_unix += 2629743.83
            if 'weeks' in item:
                weeks = since[p - 1]
                time_since_unix += 604800 * int(weeks)
            elif 'week' in item:
                time_since_unix += 604800
            if 'days' in item:
                days = since[p - 1]
                time_since_unix += 86400 * int(days)
            elif 'day' in item:
                time_since_unix += 86400
        # calculate the relative time
        time_since = timestamp - time_since_unix
        return datetime.datetime.fromtimestamp(time_since).date()


