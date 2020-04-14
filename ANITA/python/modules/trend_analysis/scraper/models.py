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
    """Parse the soup and extracts the features for the product"""

    def __init__(self, soup, scraper, file_date):
        self.scraper = scraper
        self.name = self.get_name(soup)
        self.vendor = self.get_vendor(soup)
        self.ships_from = self.get_ships_from(soup)
        self.ships_to = self.get_ships_to(soup)
        self.price = self.get_price(soup)
        self.price_eur = Product.get_price_eur(self.price, file_date)
        self.info = self.get_info(soup)
        self.feedback = self.get_feedback(soup, file_date)

    def get_name(self, soup):
        """Returns the name of the product"""
        try:
            return self.scraper.p_product_name(soup)
        except:
            return None

    def get_vendor(self, soup):
        """Returns the name of the vendor"""
        try:
            return self.scraper.p_vendor(soup)
        except:
            return None

    def get_ships_from(self, soup):
        """Returns the country/area where is shipped from"""
        try:
            return self.scraper.p_ships_from(soup)
        except:
            return None

    def get_ships_to(self, soup):
        """Returns a list of countries where shipped to"""
        try:
            ship_to = self.scraper.p_ships_to(soup)
            # return in a list if only one country is known
            if type(ship_to) == str:
                ship_to = [ship_to]

            # Change abbreviations of countries into country names
            for n, country in enumerate(ship_to):
                if len(country) == 2:
                    ship_to[n] = Product.get_country(country)
            return ship_to

        except:
            return None

    def get_price(self, soup):
        """Returns the price in dict or str/float/int"""
        try:
            return self.scraper.p_price(soup)
        except:
            return None

    @staticmethod
    def get_price_eur(price, file_date):
        """This function handles to conversion into euro's, this happens in three different ways:
        1. The price is already in euros, keep it that way
        2. The price is in dollars, will be converted to euro's via API (function: convert_usd_to_eur)
        3. The price is in bitcoin, bitcoin will be converted to dollars and dollars to euro's.
        The conversion rates of the given dates of the files are used for the conversion"""

        # Conversion for the pages that contain only one price
        if type(price) == str or type(price) == float or type(price) == int:
            if 'usd' in price.lower():
                price_dollar = float(''.join(c for c in price if c.isdigit() or c == '.'))
                return round(Product.convert_usd_to_eur(price_dollar, file_date), 2)
            if 'eur' in price.lower():
                price_euro = float(''.join(c for c in price if c.isdigit() or c == '.'))
                return round(price_euro, 2)
            if '฿' in price:
                price_bitcoin = float(''.join(c for c in price if c.isdigit() or c == '.'))
                price_dollar = round(Product.convert_btc_to_usd(price_bitcoin, file_date), 2)
                return round(Product.convert_usd_to_eur(price_dollar, file_date), 2)

        # Conversion for the pages that contain multiple prices and are given in a dict
        if type(price) == dict:
            new_price_dict = {}
            for item in price:
                if 'usd' in price[item].lower():
                    price_dollar = float(''.join(c for c in price[item] if c.isdigit() or c == '.'))
                    price_eur = Product.convert_usd_to_eur(price_dollar, file_date)
                    new_price_dict[item] = round(price_eur, 2)
                elif 'eur' in price[item].lower():
                    price_eur = float(''.join(c for c in price[item] if c.isdigit() or c == '.'))
                    new_price_dict[item] = round(price_eur, 2)
                elif '฿' in price:
                    price_bitcoin = float(''.join(c for c in price[item] if c.isdigit() or c == '.'))
                    price_dollar = round(Product.convert_btc_to_usd(price_bitcoin, file_date), 2)
                    price_eur = round(Product.convert_usd_to_eur(price_dollar, file_date), 2)
                    new_price_dict[item] = price_eur
                else:
                    new_price_dict[item] = None
            return new_price_dict

    def get_info(self, soup):
        """Returns the info as str"""
        try:
            return self.scraper.p_info(soup)
        except:
            return None

    def get_feedback(self, soup, file_date):
        """Returns the feedback on the product
        uses the feedback_handles to handle all feedback"""
        try:
            feedback_list = self.scraper.p_feedback(soup)
            return Product.feedback_handler(feedback_list, file_date)
        except:
            return None

    @staticmethod
    def feedback_handler(feedback_list, file_date):
        """Static method to export all the feedback
        Feedback_list is the list of given feedback.
        Returns the feedback list with appropriate formatted time"""
        for p, feedback in enumerate(feedback_list):
            if type(feedback['date']) == datetime.datetime:
                date = feedback['date'].date()
                # calculate the precision of the given time, this the possible deviation there is
                feedback_list[p]['date_deviation'] = Vendor.determine_date_deviation(feedback['date'])
                # Give the date in appropriate time format
                feedback_list[p]['date'] = time.mktime(date.timetuple())
            elif type(feedback['date']) == str:
                date = Vendor.calculate_time_since(feedback['date'], file_date)
                # calculate the precision of the given time, this the possible deviation there is
                feedback_list[p]['date_deviation'] = Vendor.determine_date_deviation(feedback['date'])
                # Give the date in appropriate time format
                feedback_list[p]['date'] = time.mktime(date.timetuple())
            else:
                # calculate the precision of the given time, this the possible deviation there is
                feedback_list[p]['date_deviation'] = None
                # Give the date in appropriate time format
                feedback_list[p]['date'] = None

        return feedback_list

    @staticmethod
    def get_country(abbreviation):
        """Return the right country when abbreviations were used. Returns the country as a string"""
        try:
            if abbreviation == 'ZZ':
                return 'Unspecified'
            else:
                return pycountry.countries.get(alpha_2=abbreviation).name
        except:
            return 'Country_naming_error'

    @staticmethod
    def convert_usd_to_eur(price, date):
        """Converts the price of dollar to eur on a specific date using an API"""
        date = datetime.datetime.fromtimestamp(date).date()  # convert unix to datetime
        if type(date) == datetime.date and (type(price) == float or type(price) == int):
            # two dates needed to find the exchange (USD/EUR) rate in that period
            date_2 = date - datetime.timedelta(days=-1)
            date_1 = date.strftime('%Y-%m-%d')
            date_2 = date_2.strftime('%Y-%m-%d')

            # Use the exchangeratesapi to find the right exchange rate
            response = requests.get(
                'https://api.exchangeratesapi.io/history?start_at=' + date_1 + '&end_at=' + date_2 + '&symbols=USD')
            assert response.status_code == 200
            if response.status_code == 200:
                conversion_rate = response.json()['rates'][date_1]['USD']
                return price / conversion_rate
            else:
                print('error: Request went wrong, exchangerates api status code: ' + str(response.status_code))
                return None
        else:
            if type(date) != datetime.date:
                print('error: Wrong format of date, no datetime object')
            if type(price) != float:
                print('error: Wrong format of price, no float')

        return None

    @staticmethod
    def convert_btc_to_usd(price, date):
        """Converts the price of dollar to eur on a specific date using an API"""
        date = datetime.datetime.fromtimestamp(date).date()  # convert unix to datetime

        if type(date) == datetime.date and (type(price) == float or type(price) == int):
            # two dates needed to find the exchange (USD/EUR) rate in that period
            date = date.strftime('%Y-%m-%d')

            # Use the coindesk to find the right exchange rate
            response = requests.get(
                'https://api.coindesk.com/v1/bpi/historical/close.json?start=' + date + '&end=' + date)
            assert response.status_code == 200
            if response.status_code == 200:
                conversion_rate = response.json()['bpi'][date]
                return price * conversion_rate
            else:
                print('error: Request went wrong, coindesk status code: ' + str(response.status_code))
                return None
        else:
            if type(date) != datetime.date:
                print('error: Wrong format of date, no datetime object')
            if type(price) != float:
                print('error: Wrong format of price, no float')

        return None


class Vendor:
    """Scrape the soup for product"""

    def __init__(self, soup, scraper, file_date):
        self.scraper = scraper
        self.name = self.get_name(soup)
        self.score = self.get_score(soup)
        self.score_normalized = Vendor.get_score_normalized(self.score)
        registration_extracted = self.get_registration(soup)
        self.registration = Vendor.normalize_date(registration_extracted, file_date)
        self.registration_deviation = self.determine_date_deviation(registration_extracted)
        last_login_extracted = self.get_last_login(soup)
        self.last_login = Vendor.normalize_date(last_login_extracted, file_date)
        self.last_login_deviation = self.determine_date_deviation(last_login_extracted)
        self.sales = self.get_sales(soup)
        self.info = self.get_info(soup)
        self.feedback = self.get_feedback(soup, file_date)

    def get_name(self, soup):
        """Returns the name of the vendor as a string"""
        try:
            return self.scraper.v_vendor_name(soup)
        except:
            return None

    def get_score(self, soup):
        """Returns the score of the Vendor"""
        try:
            return self.scraper.v_score(soup)
        except:
            return None

    @staticmethod
    def get_score_normalized(score):
        """Returns the normalized score of the vendor"""

        if type(score) == tuple:  # Example: (1,5) means 1 point on scale up to 5
            return round(float(score[0]) / float(score[1]), 2)
        if type(score) == list:  # Example: [1,2] means 1 positive and 2 negatives
            score_sum = float(score[0]) + float(score[1])
            if score_sum > 0:
                return round(float(score[0]) / score_sum, 2)
        return None

    def get_registration(self, soup):
        """Returns the registration date of the Vendor"""
        try:
            return self.scraper.v_registration(soup)
        except:
            return None

    # @staticmethod
    # def get_registration_normalized(registration, date):
    #     """ Returns the registration date in the right UNIX format"""
    #     try:
    #         if type(registration) == datetime.datetime:
    #             date = registration.date()
    #         # if the date is not given as a string, the date needs to converted to a datetime object
    #         # the Vendor.calculate_time_since function is used for this
    #         if type(registration) == str:
    #             date = Vendor.calculate_time_since(registration, date)
    #         return time.mktime(date.timetuple())
    #     except:
    #         return None

    def get_last_login(self, soup):
        """Returns the last login of the Vendor"""
        try:
            return self.scraper.v_last_login(soup)
        except:
            return None

    # @staticmethod
    # def get_last_login_normalized(last_login, date):
    #     try:
    #         if type(last_login) == datetime.datetime:
    #             date = last_login.date()
    #         if type(last_login) == str:
    #             date = Vendor.calculate_time_since(last_login, date)
    #         return time.mktime(date.timetuple())
    #     except:
    #         return None

    @staticmethod
    def normalize_date(date_to_normalize, file_creation_date):
        """Normalizes the date given the date to normalize and the file creation date"""
        try:
            # if the date is a datetime object, only keep the date
            if type(date_to_normalize) == datetime.datetime:
                date = date_to_normalize.date()
            # if the date is a string, the relative date needs to be calculated
            elif type(date_to_normalize) == str:
                date = Vendor.calculate_time_since(date_to_normalize, file_creation_date)
            else:
                date = None

            # return a unix time
            return time.mktime(date.timetuple())
        except:
            return None

    def get_sales(self, soup):
        """Returns the number of sales in int"""
        try:
            return int(self.scraper.v_sales(soup))
        except:
            return None

    def get_info(self, soup):
        """Returns the Vendor info as a string"""
        try:
            return self.scraper.v_info(soup)
        except:
            return None

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

    @staticmethod
    def determine_date_deviation(date):
        """Calculate the precision of the relative time.
        For example if the relative time was: 2 months ago, then the date is precise up to a month
        If it says 1 day ago, the precision is a day"""
        if type(date) == str:
            date = date.lower().split()
            length_idx = len(date) - 1
            while length_idx >= 0:
                if 'year' in date[length_idx]:
                    return 'year'
                if 'month' in date[length_idx]:
                    return 'month'
                if 'week' in date[length_idx]:
                    return 'week'
                if 'day' in date[length_idx]:
                    return 'day'
                if 'hour' in date[length_idx]:
                    return 'day'
                if 'minute' in date[length_idx]:
                    return 'day'
                if 'second' in date[length_idx]:
                    return 'day'

                length_idx -= 1
        if type(date) == datetime.date:

            return 'exact date'