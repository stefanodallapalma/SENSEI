# ----------------------------------------------------------
# This is a the scraper file for directdrugs.to
# Fill the indicated fields with answers, if you cannot
# find the specific field in the market. Let the function return None.
# ----------------------------------------------------------

# -- IMPORT
from dateutil.parser import parse

# Local import
from .scraper import Scraper, ProductScraper, VendorScraper


class DirectdrugsScraper(Scraper):
    def __init__(self):
        self.product_scraper = DirectdrugsProductScraper()

    def pagetype(self, soup):
        try:
            if soup.find('button', {'name': 'add-to-cart'}):
                return 'product'
        except:
            raise Exception("Unknown type")


class DirectdrugsProductScraper(ProductScraper):

    def product_name(self):
        return self.soup.find('h1', {'class':'product_title entry-title'}).text

    def vendor(self):
        return None

    def ships_from(self):
        return None

    def ships_to(self):
        return None

    def price(self):
        price = self.soup.find('p', {'class': 'price'}).text
        if len(price.split(' ')) == 2:
            price = price.split(' ')[1]
        if len(price.split('/')) == 2:
            price = price.split('/')[0]
        return price

    def category(self):
        return None

    def info(self):
        return self.soup.find('div', {'class' : 'woocommerce-product-details__short-description'}).text

    def feedback(self):
        feedback_list = []

        # loop to walk through the feedback
        reviews = self.soup.find('div', {'id': 'comments'})

        for review in reviews.find_all('li'):
            # Find the score, can be numerical score: (score, scale), or 'positive', 'negative' or 'neutral'
            # for pos/neg scores.
            score = (review.find('strong', {'class': 'rating'}).text, 5)

            # The message of the feedback in type str
            message = review.find('div', {'class': 'description'}).text

            # The time in datetime object or time ago in type str
            date = parse(review.find('time', {'class': 'woocommerce-review__published-date'}).text)

            # User, name of the user or encrypted user name (if any) in type str
            user = review.find('strong', {'class': 'woocommerce-review__author'}).text

            # in json format
            feedback_json = {
                'score': score,
                'message': message,
                'date': date,
                'user': user,
            }
            feedback_list.append(feedback_json)

        return feedback_list
