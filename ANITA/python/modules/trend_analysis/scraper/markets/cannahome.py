# ----------------------------------------------------------
# This is the market scraper for cannahome
# Fill the indicated fields with answers, if you cannot
# find the specific field in the market. Let the function return None.
# ----------------------------------------------------------

# -- IMPORT
from dateutil.parser import parse

# Local import
from .scraper import Scraper, ProductScraper, VendorScraper


class CannahomeScraper(Scraper):

    def pagetype(self, soup):
        try:
            if soup.find('a', {'class': 'btn big wide'}).text == ' Order Product':
                return 'product'

            if soup.find('a', {'class': 'btn wide purple arrow-right'}).text == "View All Vendor's Listings":
                return 'vendor'
        except:
            raise Exception("Unknown type")


class CannahomeProductScraper(ProductScraper):

    def product_name(self):
        return self.soup.find('div', {"row"}).find('h2').text

    def vendor(self):
        return self.soup.find('div', {'class': "row rows-20"}).find('div', {'class': 'row'}).find('a').text

    def ships_from(self):
        return self.soup.find_all('div', {'class': "row cols-15"})[1].find_all('label')[1].text

    def ships_to(self):
        return None

    def price(self):
        return self.soup.find('div', {'class': "price"}).find('span', {'class': 'big'}).text.split(' ')[0]

    def info(self):
        return self.soup.find('div', {'class': 'top-tabs'}).find('div', {'class': "formatted"}).text

    def feedback(self):
        feedback_list = []

        # loop to walk through the feedback
        for review in self.soup.find_all('div', {'class': "col-5"})[2].find_all('li'):
            # Find the score, can be numerical score: (score, scale), or 'positive', 'negative' or 'neutral' for pos/neg
            # scores.
            score = (int(len(review.find_all('i', {'class': 'full'}))), 5)

            # The message of the feedback in type str
            message = review.find('div', {'class': 'right formatted'}).text

            # The time in datetime object or time ago in type str
            date = parse(review.find('date').text)

            # User, name of the user or encrypted user name (if any) in type str
            user = None  # not available

            # in json format
            feedback_json = {
                'score': score,
                'message': message,
                'date': date,
                'user': user,
            }
            feedback_list.append(feedback_json)

        return feedback_list


class CannahomeVendorScraper(VendorScraper):

    def vendor_name(self):
        return self.soup.find('div', {'class' : 'main-infos'}).find('h2').text

    def score(self):
        s = self.soup.find('div', {'class': 'main-infos'}).find('div', {'class': 'rating stars color-yellow'}).text
        return (float(s[s.find("[") + 1:s.find("]")]), 5)

    def registration(self):
        return None

    def last_login(self):
        return self.soup.find('div', {'class': 'corner'}).find('div', {'class' : 'aux'}).text  #returns a string

    def sales(self):
        return None

    def info(self):
        return self.soup.find('div', {'class' : 'contents'}).text

    def feedback(self):
        feedback_list = []

        # loop to walk through the feedback
        for review in self.soup.find('ul', {'class': 'row list-ratings columns'}).find_all('li'):
            # Find the score, can be numerical score: (score, scale), or 'positive', 'negative' or 'neutral'
            # for pos/neg scores.
            score = (len(review.find('div', {'class': 'rating stars color-yellow'}).find_all('i', {'class': 'full'})),
                     5)

            # The message of the feedback in type str
            message = review.find('div', {'class': 'right formatted'}).text

            # The time in datetime object or time ago in type str
            date = parse(review.find('date').text)

            # Name of the product that the feedback is about (if any) in type str
            product = review.find('small').text

            # User, name of the user or encrypted user name (if any) in type str
            user = None  # not present

            # Deals by user (if any) in type int or str (if range)
            deals = None  # not present

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
