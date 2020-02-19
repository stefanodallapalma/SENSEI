from bs4 import BeautifulSoup
from datetime import datetime
from html_pages.bean.HtmlPage import HtmlPage

class ProductRules:

    def __init__(self, html_page):
        # WORKS ON LOCAL (open(...)). TO DO: ONLINE SUPPORT
        self._soup_profile = BeautifulSoup(open(html_page.profile_path), "html.parser")
        self._soup_termcondition = BeautifulSoup(open(html_page.term_and_condition_path), "html.parser")

    def name(self):
        '''Returns the name of the product'''
        return self._soup_profile.find('ol',{'class':'breadcrumb'}).find_all('li')[3].text

    def category(self):
        '''Returns the main category of the product'''
        return self._soup_profile.find('ol',{'class':'breadcrumb'}).find_all('li')[1].text

    def subcategory(self):
        '''Returns the subcategory of the product'''
        return self._soup_profile.find('ol',{'class':'breadcrumb'}).find_all('li')[2].text

    def vendor(self):
        '''Returns the username from the Berlusconi market'''
        return str(self._soup_profile.select("a[href*=vendor]")[0].text.strip())

    def price_eur(self):
        '''Returns the price from the Berlusconi market'''
        return str(self._soup_profile.find('div',{"class":"listing-price"}).strong.text)[:-5]

    def price_btc(self):
        '''Returns the price of the product in bitcoin'''
        return self._soup_profile.find('span',{'class':'text-muted'}).text.strip()

    def stock(self):
        '''Returns the price of the product in bitcoin'''
        if self._soup_profile.find('span',{'class':'label label-success label-full'}) != None:
            return self._soup_profile.find('span',{'class':'label label-success label-full'}).text.strip()
        else:
            return self._soup_profile.find('span',{'class':'label label-danger label-full'}).text.strip()

    def shipping_options(self):
        '''Returns the shipping options in a list'''
        if self.product_class() == 'Physical':
            return [option.text for option in self._soup_profile.find('select',{'name':'shipping_option'}).find_all('option')]
        else:
            return 'digital product'

    def product_class(self):
        '''Returns the class of the product'''
        return self._soup_profile.find('div',{'class':'col-sm-7'}).find_all('td')[3].text

    def escrow_type(self):
        '''Returns the escrow type'''
        return self._soup_profile.find('div',{'class':'col-sm-7'}).find_all('td')[5].text

    def ships_from(self):
        '''Returns where the product ships from'''
        if self.product_class() == 'Physical':
            return self._soup_profile.find('div',{'class':'col-sm-7'}).find_all('td')[7].text
        else:
            return 'digital product'

    def ships_to(self):
        '''Returns where the product ships to'''
        if self.product_class() == 'Physical':
            location = self._soup_profile.find('div', {'class': 'col-sm-7'}).find_all('td')[9].text
            if 'Worldwide shipping' in location:
                return ['Worldwide']
            if 'Worldwide' in location:
                return ['Worldwide']
            if 'countries' in location:
                return ['Worldwide']
            else:
                return location.replace(' ', '').split(',')
        return ['digital product']

    def items_sold(self):
        '''Returns the items sold'''
        date_list = self._soup_profile.find('div',{'class':'col-sm-7'}).find_all('em')
        for possible_date in date_list:
            if 'sold' in possible_date.text:
                sold=possible_date.text.split()[0]
        return int(sold)

    def orders_sold_since(self):
        '''Returns the date since when the orders are sold'''
        date_list = self._soup_profile.find('div',{'class':'col-sm-7'}).find_all('em')
        for possible_date in date_list:
            if 'sold' in possible_date.text:
                date= ' '.join(possible_date.text.split()[4:])
        return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")#.strftime("%d/%m/%Y %H:%M:%S")

    def details(self):
        '''Returns the description from the product'''
        try:
            return ''.join(self._soup_profile.find('p').text)
        except:
            return None

    def terms_and_conditions(self):
        '''Returns the terms and conditions of a product from the Berlusconi market'''
        try:
            if self._soup_termcondition.find('h4').text == 'Terms & Conditions':
                return str(self._soup_termcondition.find('div', {'class':'col-md-12'}).find('p').text)
        except:
            return None
