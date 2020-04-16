# ----------------------------------------------------------
# This is a template for new markets
# Fill the indicated fields with answers, if you cannot
# find the specific field in the market. Let the function return None.
# ----------------------------------------------------------

# -- IMPORT
# from datetime import datetime
from dateutil.parser import parse

# Local import
from .scraper import Scraper, ProductScraper, VendorScraper


class DrugscenterScraper(Scraper):

    def pagetype(self, soup):
        try:
            if soup.find('button', {'name': 'add-to-cart'}):
                return 'product'
        except:
            raise Exception("Unknown type")


class DrugscenterProductScraper(ProductScraper):

    def product_name(self):
        return self.soup.find('h1', {'class' : 'product-title product_title entry-title'}).text

    def vendor(self):
        return None

    def ships_from(self):
        return 'Gibraltar (european deliveries)'

    def ships_to(self):
        return 'Worldwide'

    def price(self):
        return self.soup.find('div', {'class' : 'price-wrapper'}).text

    def info(self):
        return self.soup.find('div', {'class' : 'product-short-description'}).text

    def feedback(self):
        feedback_list = []

        # loop to walk through the feedback
        reviews = self.soup.find('div', {'id': 'comments'}).find_all('li')
        for review in reviews:
            # Find the score, can be numerical score: (score, scale), or 'positive', 'negative' or 'neutral'
            # for pos/neg scores.
            score = (int(review.find('strong', {'class': 'rating'}).text), 5)

            # The message of the feedback in type str
            message = self.soup.find('div', {'class': 'description'}).text

            # The time in datetime object or time ago in type str
            date = parse(self.soup.find('time', {'class': 'woocommerce-review__published-date'}).text)

            # User, name of the user or encrypted user name (if any) in type str
            user = self.soup.find('strong', {'class': 'woocommerce-review__author'}).text

            # in json format
            feedback_json = {
                'score': score,
                'message': message,
                'date': date,
                'user': user,
            }
            feedback_list.append(feedback_json)

        return feedback_list
