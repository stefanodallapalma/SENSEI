import time
import pycountry
import requests
import datetime
import json
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod

# Local imports
from modules.trend_analysis.scraper.market.models import *
from modules.trend_analysis.scraper.market.enum import Market


class Scraper(ABC):
    @property
    def product_scraper(self):
        return self._product_scraper

    @product_scraper.setter
    def product_scraper(self, value):
        self._product_scraper = value

    @property
    def vendor_scraper(self):
        return self._vendor_scraper

    @vendor_scraper.setter
    def vendor_scraper(self, value):
        self._vendor_scraper = value

    @abstractmethod
    def pagetype(self, soup):
        """Define how to distinguish vendor pages from product pages"""
        pass

    def extract_data(self, html_path, timestamp, market):
        try:
            soup = BeautifulSoup(open(html_path), "html.parser")
        except:
            raise Exception("BS4 Problem!!!")

        # Check if the html refers to a product or a vendor page
        page_type = self.pagetype(soup)

        # Market detection
        market_name = market
        if isinstance(market, Market):
            market_name = market.name.lower()

        # Create overview object of the main information about the page
        web_page_information = WebPage(html_path, market_name, page_type, timestamp)

        # Page data for vendor or product pages
        if web_page_information.page_type == 'product':
            page_specific_data, irretrievable_info_json = self.product_scraper.scrape(timestamp, soup)
        elif web_page_information.page_type == 'vendor':
            page_specific_data, irretrievable_info_json = self.vendor_scraper.scrape(timestamp, soup)
        else:
            raise Exception("Invalid page type")

        return web_page_information, page_specific_data, irretrievable_info_json


class ProductScraper(ABC):
    @property
    def soup(self):
        return self._soup

    @abstractmethod
    def product_name(self):
        """ Return the name of the product as string """
        pass

    @abstractmethod
    def vendor(self):
        """Return the name of the vendor as string"""
        pass

    @abstractmethod
    def ships_from(self):
        """Return the place from where the package is delivered as string"""
        pass

    @abstractmethod
    def ships_to(self):
        """Return where the package can be delivered to as string
            If multiple; provide in a list"""
        pass

    @abstractmethod
    def price(self):
        """Return the price of the produc as string"""
        pass

    @abstractmethod
    def info(self):
        """Return the info as string"""
        pass

    @abstractmethod
    def feedback(self):
        """ Return the feedback for the product"""
        pass

    def scrape(self, timestamp, soup):
        self._soup = soup
        tot_params = 8
        irretrievable_params = 0
        exception_messages = {}

        try:
            product_name = self.product_name()
        except Exception as e:
            product_name = None
            irretrievable_params += 1
            exception_messages["product_name"] = str(e)
        
        try:
            vendor = self.vendor()
        except Exception as e:
            vendor = None
            irretrievable_params += 1
            exception_messages["vendor"] = str(e)
        
        try:
            ships_from = self.ships_from()
        except Exception as e:
            ships_from = None
            irretrievable_params += 1
            exception_messages["ships_from"] = str(e)
        
        try:
            ships_to = self.ships_to()
            ships_to = contry_list(ships_to)
        except Exception as e:
            ships_to = None
            irretrievable_params += 1
            exception_messages["ships_to"] = str(e)
        
        try:
            price = self.price()
            price_eur = ProductScraper.get_price_eur(price, timestamp)
        except Exception as e:
            price = None
            price_eur = None
            irretrievable_params += 2
            exception_messages["price/price_eur"] = str(e)
        
        try:
            info = self.info()
        except Exception as e:
            info = None
            irretrievable_params += 1
            exception_messages["info"] = str(e)

        try:
            feedback_list = self.feedback()
            feedback_list = feedback_handler(feedback_list, timestamp)
        except Exception as e:
            feedback_list = None
            irretrievable_params += 1
            exception_messages["feedback_list"] = str(e)

        page_specific_data = Product(product_name, vendor, ships_from, ships_to, price, price_eur, info,
                                     feedback_list)
        
        irretrievable_info_json = {"irretrievable_params": irretrievable_params, "tot_params": tot_params,
                                   "irretrievable_rate": (irretrievable_params/tot_params),
                                   "exception_params": exception_messages}
        
        return page_specific_data, irretrievable_info_json

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
                return round(ProductScraper.convert_usd_to_eur(price_dollar, file_date), 2)
            if 'eur' in price.lower():
                price_euro = float(''.join(c for c in price if c.isdigit() or c == '.'))
                return round(price_euro, 2)
            if '฿' in price:
                price_bitcoin = float(''.join(c for c in price if c.isdigit() or c == '.'))
                price_dollar = round(ProductScraper.convert_btc_to_usd(price_bitcoin, file_date), 2)
                return round(ProductScraper.convert_usd_to_eur(price_dollar, file_date), 2)

        # Conversion for the pages that contain multiple prices and are given in a dict
        if type(price) == dict:
            new_price_dict = {}
            for item in price:
                if 'usd' in price[item].lower():
                    price_dollar = float(''.join(c for c in price[item] if c.isdigit() or c == '.'))
                    price_eur = ProductScraper.convert_usd_to_eur(price_dollar, file_date)
                    new_price_dict[item] = round(price_eur, 2)
                elif 'eur' in price[item].lower():
                    price_eur = float(''.join(c for c in price[item] if c.isdigit() or c == '.'))
                    new_price_dict[item] = round(price_eur, 2)
                elif '฿' in price:
                    price_bitcoin = float(''.join(c for c in price[item] if c.isdigit() or c == '.'))
                    price_dollar = round(ProductScraper.convert_btc_to_usd(price_bitcoin, file_date), 2)
                    price_eur = round(ProductScraper.convert_usd_to_eur(price_dollar, file_date), 2)
                    new_price_dict[item] = price_eur
                else:
                    new_price_dict[item] = None
            return new_price_dict

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


class VendorScraper(ABC):
    @property
    def soup(self):
        return self._soup

    @abstractmethod
    def vendor_name(self):
        """ Return the name of the vendor as string """
        pass

    @abstractmethod
    def score(self):
        """ Return the score of the vendor as float, or if multiple as float in list """
        pass

    @abstractmethod
    def registration(self):
        """ Return the moment of registration as datetime object """
        pass

    @abstractmethod
    def last_login(self):
        """ Return the moment of last login as datetime object"""
        pass

    @abstractmethod
    def sales(self):
        """ Return the number of sales, also known as transactions or orders as int """
        pass

    @abstractmethod
    def info(self):
        """ Return the information as a string """
        pass

    @abstractmethod
    def feedback(self):
        """ Return the feedback for the vendors"""
        pass

    def scrape(self, timestamp, soup):
        self._soup = soup
        tot_params = 10
        irretrievable_params = 0
        exception_messages = {}

        try:
            vendor_name = self.vendor_name()
        except Exception as e:
            vendor_name = None
            irretrievable_params += 1
            exception_messages["vendor_name"] = str(e)

        try:
            score = self.score()
            score_normalized = VendorScraper.get_score_normalized(score)
        except Exception as e:
            score = None
            score_normalized = None
            irretrievable_params += 2
            exception_messages["score/score_normalized"] = str(e)

        try:
            registration = self.registration()
            registration = VendorScraper.normalize_date(registration, timestamp)
            registration_deviation = determine_date_deviation(registration)
        except Exception as e:
            registration = None
            registration_deviation = None
            irretrievable_params += 2
            exception_messages["registration/registration_deviation"] = str(e)

        try:
            last_login = self.last_login()
            last_login - VendorScraper.normalize_date(last_login, timestamp)
            last_login_deviation = determine_date_deviation(last_login)
        except Exception as e:
            last_login = None
            last_login_deviation = None
            irretrievable_params += 2
            exception_messages["last_login/last_login_deviation"] = str(e)

        try:
            sales = self.sales()
        except Exception as e:
            sales = None
            irretrievable_params += 1
            exception_messages["sales"] = str(e)

        try:
            info = self.info()
        except Exception as e:
            info = None
            irretrievable_params += 1
            exception_messages["info"] = str(e)

        try:
            feedback_list = self.feedback()
            feedback_list = feedback_handler(feedback_list, timestamp)
        except Exception as e:
            feedback_list = None
            irretrievable_params += 1
            exception_messages["feedback_list"] = str(e)

        page_specific_data = Vendor(vendor_name, score, score_normalized, registration, registration_deviation,
                                    last_login, last_login_deviation, sales, info, feedback_list)

        irretrievable_info_json = {"irretrievable_params": irretrievable_params, "tot_params": tot_params,
                                   "irretrievable_rate": (irretrievable_params / tot_params),
                                   "exception_params": exception_messages}

        return page_specific_data, irretrievable_info_json

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

    @staticmethod
    def normalize_date(date_to_normalize, file_creation_date):
        """Normalizes the date given the date to normalize and the file creation date"""
        try:
            # if the date is a datetime object, only keep the date
            if type(date_to_normalize) == datetime.datetime:
                date = date_to_normalize.date()
            # if the date is a string, the relative date needs to be calculated
            elif type(date_to_normalize) == str:
                date = calculate_time_since(date_to_normalize, file_creation_date)
            else:
                date = None

            # return a unix time
            return time.mktime(date.timetuple())
        except:
            return None


def contry_list(ships_to):
    """Returns a list of countries where shipped to"""
    try:
        # return in a list if only one country is known
        if type(ships_to) == str:
            ships_to = [ships_to]

        # Change abbreviations of countries into country names
        for n, country in enumerate(ships_to):
            if len(country) == 2:
                ships_to[n] = get_country(country)
    except:
        ships_to = None

    return ships_to


def get_country(abbreviation):
    """Return the right country when abbreviations were used. Returns the country as a string"""
    try:
        if abbreviation == 'ZZ':
            return 'Unspecified'
        else:
            return pycountry.countries.get(alpha_2=abbreviation).name
    except:
        return 'Country_naming_error'


def feedback_handler(feedback_list, file_date):
    """Static method to export all the feedback
    Feedback_list is the list of given feedback.
    Returns the feedback list with appropriate formatted time"""
    for p, feedback in enumerate(feedback_list):
        if type(feedback['date']) == datetime.datetime:
            date = feedback['date'].date()
            # calculate the precision of the given time, this the possible deviation there is
            feedback_list[p]['date_deviation'] = determine_date_deviation(feedback['date'])
            # Give the date in appropriate time format
            feedback_list[p]['date'] = time.mktime(date.timetuple())
        elif type(feedback['date']) == str:
            date = calculate_time_since(feedback['date'], file_date)
            # calculate the precision of the given time, this the possible deviation there is
            feedback_list[p]['date_deviation'] = determine_date_deviation(feedback['date'])
            # Give the date in appropriate time format
            feedback_list[p]['date'] = time.mktime(date.timetuple())
        else:
            # calculate the precision of the given time, this the possible deviation there is
            feedback_list[p]['date_deviation'] = None
            # Give the date in appropriate time format
            feedback_list[p]['date'] = None

    return feedback_list


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
