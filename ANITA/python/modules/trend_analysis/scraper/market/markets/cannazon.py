# ----------------------------------------------------------
# This is a template for new market
# Fill the indicated fields with answers, if you cannot
# find the specific field in the market. Let the function return None.
# ----------------------------------------------------------

# -- IMPORT
# from datetime import datetime
from dateutil.parser import parse

# Local import
from .scraper import Scraper, ProductScraper, VendorScraper


class CannazonScraper(Scraper):

    def pagetype(self, soup):
        try:
            if soup.find('h2', {'class': 'title text-center'}).text == 'Product Details':
                return 'product'

            if soup.find('h2', {'class': 'title text-center'}).text == 'Vendor Profile':
                return 'vendor'
        except:
            raise Exception("Unknown type")


class CannazonProductScraper(ProductScraper):

    def product_name(self):
        return self.soup.find('div', {'class': 'product-information border-box container-box'}).find('h2').text

    def vendor(self):
        return list(self.soup.find('div', {
            'class': 'product-information border-box container-box product-information-vendor'}).find(
                'a', {'class': 'vendor_rating'}).stripped_strings)[0]

    def ships_from(self):
        ships_from = None
        data = list(
            self.soup.find('div', {'class':
                                  'product-information border-box container-box product-information-vendor'}).find(
                'a', {'class': 'vendor_rating'}).stripped_strings)
        for idx, value in enumerate(data):
            if value == 'Shipping From:':
                ships_from = data[idx + 1]
        return ships_from

    def ships_to(self):
        country_list = None
        data = list(
            self.soup.find('div', {'class':
                                  'product-information border-box container-box product-information-vendor'}).find(
                'a', {'class': 'vendor_rating'}).stripped_strings)
        for idx, value in enumerate(data):
            if value == 'Shipping To:':
                country_list = []
                string = data[idx + 1].split("|")
                for country in string:
                    country = country.replace('\t', '').replace('\n', '')
                    country_list.append(country)
        return country_list

    def price(self):
        return self.soup.find('p', {'class' : 'price'}).text

    def info(self):
        info = ''
        for content in self.soup.find_all('div', {'class': 'content'})[:4]:
            info = info + content.text
        return info

    def feedback(self):
        return None


class CannazonVendorScraper(VendorScraper):

    def vendor_name(self):
        return self.soup.find('div', {'class': 'col-xs-12 vendor-box container-box'}).find('h2').text

    def score(self):
        """ Return the score of the vendor in one of these two options:
            1. The score in a tuple as first item (float/int) and second item as the scale (float/int).
            Example: a 4.95 of scale up to 5: (4.95, 5), 97.7%: (97.7, 100)
            2. When the item consists of positives and negatives and possibly neutrals. [positive, negative, neutral]
            example: 96 negative, no neutrals, 20 positives: [20, 96, 0]
            """
        pos = self.soup.find('span', {'class': 'badge badge-positive'}).text
        neg = self.soup.find('span', {'class': 'badge badge-negative'}).text
        return [pos, neg, 0]

    def registration(self):
        return parse(list(self.soup.find('div', {'class': 'col-xs-12 col-sm-6'}).stripped_strings)[1])

    def last_login(self):
        return None

    def sales(self):
        return int(list(self.soup.find('div', {'class': 'col-xs-12 col-sm-6'}).stripped_strings)[-1])

    def info(self):
        return self.soup.find_all('div', {'class': 'content'})[1].text + self.soup.find_all('div', {'class': 'content'})[2].text

    def feedback(self):
        feedback_list = []

        # loop to walk through the feedback
        for review in self.soup.find_all('div', {'class': 'content'})[0].find_all('div', {'class': 'row'}):

            # Find the score, can be numerical score: (score, scale), or 'positive', 'negative' or 'neutral' for pos/neg
            # scores.
            if self.soup.find('span', {'class': 'badge badge-positive'}):
                score = 'positive'
            elif self.soup.find('span', {'class': 'badge badge-negative'}):
                score = 'negative'
            else:
                score = None

            # The message of the feedback in type str
            message = list(review.find('div', {'class': 'col-xs-6'}).stripped_strings)[0]

            # The time in datetime object or time ago in type str
            date = parse(review.find('em').text)

            # Name of the product that the feedback is about (if any) in type str
            product = review.find('a').text

            # User, name of the user or encrypted user name (if any) in type str
            user = None  # Non existent

            # Deals by user (if any) in type int or str (if range)
            deals = None  # Non existent

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
    """ Return the pgp as a string """
    # example: return soup.find('div', {'class' : 'container container_large'}).text
    return soup.find_all('div', {'class': 'content'})[3].text


# -- VENDOR FEEDBACK DATA
def v_feedback(soup):
    """ Return the feedback for the vendors"""



