# ----------------------------------------------------------
# Marketscraper darkmarket
# ----------------------------------------------------------

# -- IMPORT
# from datetime import datetime
from dateutil.parser import parse

# Local import
from .scraper import Scraper, ProductScraper, VendorScraper


class DarkmarketScraper(Scraper):

    def pagetype(self, soup):
        try:
            if 'cart' in soup.find('div', {'class': 'col-md-7'}).text:
                return 'product'

            if 'Vendor' in soup.find('ol', {'class': 'breadcrumb'}).text:
                return 'vendor'
        except:
            raise Exception("Unknown type")


class DarkmarketProductScraper(ProductScraper):

    def product_name(self):
        return self.soup.find('div', {'class': 'col-md-5'}).find('h2').text

    def vendor(self):
        return self.soup.find('a', {'class': 'btn btn-light btn-sm'}).find('span').text

    def ships_from(self):
        ships_from = None
        data = self.soup.find('div', {'class', 'mt-4'}).find_all('p')
        for string in data:
            if 'Ships from' in string.text:
                ships_from = string.find('strong').text
        return ships_from

    def ships_to(self):
        ships_to = None
        data = self.soup.find('div', {'class', 'mt-4'}).find_all('p')
        for string in data:
            if 'Ships all' in string.text:
                ships_to = string.find('em').text.split(',')
                if ships_to == ['']:
                    ships_to = None
        return ships_to

    def price(self):
        price_dict = dict()
        price_list = self.soup.find('div', {'class', 'col-md-12 text-center'}).find_all('li')
        for item in price_list:
            price_dict[item.text.replace('\n', '')] = item.find('strong').text.replace('\n', '')
        return None  # replace None

    def info(self):
        info = ''
        for string in self.soup.find('div', {'class': 'mt-4'}).find_all('p'):
            info = info + string.text
        return info

    def feedback(self):
        feedback_list = []

        # loop to walk through the feedback
        for review in self.soup.find('table', {'class': 'table table-striped'}).find('tbody').find_all('tr'):
            # Find the score, can be numerical score: (score, scale), or 'positive', 'negative' or 'neutral' for pos/neg
            # scores.
            score = (len(review.find_all('td')[0].find_all('i', {'class': 'fas fa-star'})), 5)

            # The message of the feedback in type str
            message = review.find_all('td')[3].text.replace('\n', '')

            # The time in datetime object or time ago in type str
            date = None  # non existent

            # User, name of the user or encrypted user name (if any) in type str
            user = None  # non existent

            # in json format
            feedback_json = {
                'score': score,
                'message': message,
                'date': date,
                'user': user,
            }
            feedback_list.append(feedback_json)

        return feedback_list


class DarkmarketVendorScraper(VendorScraper):

    def vendor_name(self):
        return self.soup.find('div', {'class': 'col-sm-5'}).find('a').text

    def score(self):
        s = self.soup.find('div', {'class': 'col-md-4 col-sm-6'}).find('span').text
        score = s[s.find("(") + 1:s.find(")")]
        return score

    def registration(self):
        return parse('01' + self.soup.find_all('span', {'class': 'font-weight-semibold'})[1].text)

    def last_login(self):
        return self.soup.find('a', {'class': 'btn btn-outline-info'}).text

    def sales(self):
        return None

    def info(self):
        return self.soup.find('div', {'class': 'col-sm-12'}).text

    def feedback(self):
        feedback_list = []

        # loop to walk through the feedback
        for review in self.soup.find('div', {'class': 'row mt-3'}).find('tbody').find_all('tr'):

            score = None
            # Find the score, can be numerical score: (score, scale), or 'positive', 'negative' or 'neutral'
            # for pos/neg scores.
            if review.find_all('td')[0].find('span').find('span', {'class': "fas fa-plus-circle text-success"}):
                score = 'positive'
            elif review.find_all('td')[0].find('span').find('span', {'class': "fas fa-minus-circle text-danger"}):
                score = 'negative'
            elif review.find_all('td')[0].find('span').find('span', {'class': "fas fa-stop-circle text-secondary"}):
                score = 'neutral'

            # The message of the feedback in type str
            message = review.find_all('td')[0].find('span').text

            # The time in datetime object or time ago in type str
            date = review.find_all('td')[2].text.replace('\n', '')

            # Name of the product that the feedback is about (if any) in type str
            product = review.find_all('td')[0].find_all('span')[3].text

            # User, name of the user or encrypted user name (if any) in type str
            user = review.find_all('td')[1].find('span').text.split('Buyer: ')[1].replace('\n', '')

            # Deals by user (if any) in type int or str (if range)
            deals = None  # non existent

            # in json format
            feedback_json = {
                'score': score,
                'message': message,
                'date': date,
                'product': product,
                'user': user,
                'deals': deals
            }
            feedback_list.append(feedback_json)

        return feedback_list


def v_pgp(soup):
    """ Return the pgp as a string"""
    return soup.find("textarea")
