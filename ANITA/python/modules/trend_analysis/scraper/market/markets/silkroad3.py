# ----------------------------------------------------------
# This is the market scraper for silkroad3
# Fill the indicated fields with answers, if you cannot
# find the specific field in the market. Let the function return None.
# ----------------------------------------------------------

# -- IMPORT
from datetime import datetime

# Local import
from .scraper import Scraper, ProductScraper, VendorScraper


class Silkroad3Scraper(Scraper):
    def __init__(self):
        self.product_scraper = Silkroad3ProductScraper()
        self.vendor_scraper = Silkroad3VendorScraper()

    def pagetype(self, soup):
        try:
            if soup.find('div', {'id': 'vp'}).find(
                    'h3').text == 'Place Order':  # you can only place an order if product
                return 'product'

            if 'Last active' in soup.find('div', {'align': 'left'}).text:  # really difficult to find a tag for vendor
                return 'vendor'
        except:
            raise Exception("Unknown type")


class Silkroad3ProductScraper(ProductScraper):

    def product_name(self):
        return self.soup.find('div', {
            'style': 'text-align:center; font-size:16px; display:inline-block;color:#333;font-weight:bold'}).find(
            'h3').text

    def vendor(self):
        return self.soup.find('div', {'style': 'color:#555;font-weight:bold;font-size:12px'}).find_all('a')[1].text

    def ships_from(self):
        info = list(self.soup.find('div', {'style': 'color:#555;font-weight:bold;font-size:12px'}).stripped_strings)
        return info[info.index('Ships From:') + 1]

    def ships_to(self):
        return None

    def price(self):
        info = list(self.soup.find('div', {'style': 'color:#555;font-weight:bold;font-size:12px'}).stripped_strings)
        return info[info.index('Price:') + 1]

    def info(self):
        return self.soup.find_all('div', {'id': 'cats'})[1].text

    def feedback(self):
        feedback_list = []

        # loop to walk through the feedback
        for review in self.soup.find('div', {'style': 'padding:0px; margin-bottom:10px; font-size:12px;'}).find_all('div', {
            'id': 'cats'}):
            # Find the score, can be numerical score: (score, scale), or 'positive', 'negative' or 'neutral'
            # for pos/neg scores.
            score = (float(list(review.find('div').stripped_strings)[0].split('/')[0]),
                     float(list(review.find('div').stripped_strings)[0].split('/')[1]))

            # The message of the feedback in type str
            message = review.find('span').text
            if message == 'No feedback.':
                message = None

            # The time in datetime object or time ago in type str
            date = list(review.stripped_strings)[4].split(')')[1]  # bit messy

            # User, name of the user or encrypted user name (if any) in type str
            user = list(review.stripped_strings)[1]

            # in json format
            feedback_json = {
                'score': score,
                'message': message,
                'date': date,
                'user': user,
            }
            feedback_list.append(feedback_json)

        return feedback_list


class Silkroad3VendorScraper(VendorScraper):

    def vendor_name(self):
        return list(self.soup.find('div', {'id' : 'cats'}).find('b').stripped_strings)[0]

    def score(self):
        pos = list(self.soup.find('div', {'id': 'cats'}).find('b').stripped_strings)[1]
        neg = list(self.soup.find('div', {'id': 'cats'}).find('b').stripped_strings)[3]
        return [pos, neg, 0]

    def registration(self):
        return None

    def last_login(self):
        return list(self.soup.find_all('div', {'align' : 'left'})[2].stripped_strings)[0] #messy

    def sales(self):
        return None

    def info(self):
        return ' '.join(list(self.soup.find_all('div', {'align' : 'left'})[2].stripped_strings)[1:])

    def feedback(self):
        feedback_list = []

        # loop to walk through the feedback
        for review in self.soup.find_all('div', {'align': 'left'})[4].find_all('div', {'id': 'cats'})[1:]:

            # Find the score, can be numerical score: (score, scale), or 'positive', 'negative' or 'neutral'
            # for pos/neg scores.
            score = (float(list(review.find('div').stripped_strings)[0].split('/')[0]),
                     float(list(review.find('div').stripped_strings)[0].split('/')[1]))
            # The message of the feedback in type str
            message = review.find_all('span')[2].text
            if message == 'No feedback.':
                message = None

            # The time in datetime object or time ago in type str
            date = list(review.find('span').stripped_strings)[-1].split(')')[1]

            # Name of the product that the feedback is about (if any) in type str
            product = list(review.find('span').stripped_strings)[4]

            # User, name of the user or encrypted user name (if any) in type str
            user = list(review.find('span').stripped_strings)[1]

            # Deals by user (if any) in type int or str (if range)
            deals = None  # not existing

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

    def pgp(self):
        return None