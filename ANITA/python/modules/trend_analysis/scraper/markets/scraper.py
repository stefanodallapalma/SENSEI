from bs4 import BeautifulSoup
from abc import ABC, abstractmethod


class Scraper(ABC):
    def __init__(self):
        self.soup = None

    @property
    def soup(self):
        return self._soup

    @soup.setter
    def soup(self, value):
        self._soup = value

    @abstractmethod
    def pagetype(self):
        """Define how to distinguish vendor pages from product pages"""
        pass

    def extract_data(self, html_path):
        try:
            self.soup = BeautifulSoup(open(html_path), "html.parser")
        except:
            raise Exception("BS4 Problem!!!")


class ProductScraper(ABC):
    def __init__(self, html_path):
        try:
            self._soup = BeautifulSoup(open(html_path), "html.parser")
        except:
            raise Exception("BS4 Problem!!!")

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


class VendorScraper(ABC):
    def __init__(self, html_path):
        try:
            self._soup = BeautifulSoup(open(html_path), "html.parser")
        except:
            raise Exception("BS4 Problem!!!")

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
