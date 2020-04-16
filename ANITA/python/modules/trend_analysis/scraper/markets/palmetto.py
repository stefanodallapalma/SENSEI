# ----------------------------------------------------------
# This is the market scraper for Palmetto
# Fill the indicated fields with answers, if you cannot
# find the specific field in the market. Let the function return None.
# ----------------------------------------------------------

# -- IMPORT
# from datetime import datetime
from dateutil.parser import parse

# Local import
from .scraper import Scraper, ProductScraper, VendorScraper


class PalmettoScraper(Scraper):

    def pagetype(self, soup):
        try:
            if soup.find('button', {'class': 'button btn-cart'}).text == 'Add to Cart':
                return 'product'
        except:
            raise Exception("Unknown type")


class PalmettoProductScraper(ProductScraper):

    def product_name(self):
        return self.soup.find('div', {'class' : 'product-name'}).text

    def vendor(self):
        return None

    def ships_from(self):
        return None

    def ships_to(self):
        return None

    def price(self):
        return self.soup.find('span', {'class' : 'price-value'}).text

    def info(self):
        info = self.soup.find('div', {'class': 'short-description'}).text
        info = info + self.soup.find('div', {'class': 'box-collateral box-description'}).text
        info += self.soup.find('div', {'class': 'box-collateral box-additional'}).text
        return info

    def feedback(self):
        feedback_list = []

        # loop to walk through the feedback
        for review in self.soup.find_all('div', {'class': 'TTreview'}):
            # Find the score, can be numerical score: (score, scale), or 'positive', 'negative' or 'neutral'
            # for pos/neg scores.
            score = (
            int(str(review.find('meta', {'itemprop': 'ratingValue'})).split('content=')[1].split(' ')[0][1]), 5)

            # The message of the feedback in type str
            message = review.find('div', {'class', 'TTreviewBody'}).text

            # The time in datetime object or time ago in type str
            date = parse(review.find('div', {'itemprop': "dateCreated"}).text)

            # User, name of the user or encrypted user name (if any) in type str
            user = review.find('span', {'itemprop': "author"}).text

            # in json format
            feedback_json = {
                'score': score,
                'message': message,
                'date': date,
                'user': user,
            }
            feedback_list.append(feedback_json)

        return feedback_list
