# Local import
from .scraper import Scraper, ProductScraper, VendorScraper


class DrugsmedicineScraper(Scraper):
    def __init__(self):
        self.product_scraper = DrugsmedicineProductScraper()
        self.vendor_scraper = DrugsmedicineVendorScraper()

    def pagetype(self, soup):
        try:
            if soup.find('div', {'class': "table_wrapper"}).find_all('th')[0].text == 'Item info:':
                return 'product'

            if soup.find('table', {'class': "msgtable"}).find('th').text == 'Vendor stats:':
                return 'vendor'
        except:
            raise Exception("Unknown type")


class DrugsmedicineProductScraper(ProductScraper):

    def product_name(self):
        return self.soup.find('div', {"content grid-8-12"}).find('h3').text

    def vendor(self):
        return self.soup.find('div', {'class': "table_wrapper"}).find('a').text

    def ships_from(self):
        return self.soup.find('div', {"table_wrapper"}).find_all('td')[3].text

    def ships_to(self):
        return self.soup.find('div', {"table_wrapper"}).find_all('td')[5].text

    def price(self):
        return self.soup.find('div', {'price_big_inner'}).text.split()[0]

    def info(self):
        return self.soup.find('div', {'prod_info'}).text

    def feedback(self):
        feedback_list = []

        # loop to walk through the feedback
        for item in self.soup.find_all('div', {'class': 'comment_wrapper'}):
            # Find the score, can be numerical score: (score, scale), or 'positive', 'negative' or 'neutral' for pos/neg scores.
            score = (item.find('b').text.count('★'), 5)

            # The message of the feedback in type str
            message = item.find('p').text

            # The time in datetime object or time ago in type str
            date = ' '.join(item.find('span', {'class': 'commenttime'}).text.split())

            # User, name of the user or encrypted user name (if any) in type str
            user = None  # Not on website

            # in json format
            feedback_json = {
                'score': score,
                'message': message,
                'date': date,
                'user': user,
            }
            feedback_list.append(feedback_json)

        return feedback_list


class DrugsmedicineVendorScraper(VendorScraper):

    def vendor_name(self):
        return self.soup.find('h3').text

    def score(self):
        return (float(self.soup.find_all('td')[5].text.split('/')[0]),5)

    def registration(self):
        return self.soup.find_all('div',{'viewusercont'})[1].find_all('td')[1].text.replace(u'\xa0', u' ')

    def last_login(self):
        return self.soup.find_all('div',{'viewusercont'})[1].find_all('td')[3].text.replace(u'\xa0', u' ')

    def sales(self):
        return int(self.soup.find_all('td')[7].text)

    def info(self):
        return self.soup.find('div', {'class' : 'container container_large'}).text

    def feedback(self):
        feedback_list = []

        # loop to walk through the feedback
        for item in self.soup.find_all('div', {'class': 'comment_wrapper'}):
            # Find the score, can be numerical score: (score, scale), or 'positive', 'negative' or 'neutral'
            # for pos/neg scores.
            score = (item.find('b').text.count('★'), 5)

            # The message of the feedback in type str
            message = item.find('p').text

            # The time in datetime object or time ago in type str
            date = ' '.join(item.find('span', {'class': 'commenttime'}).text.split())

            # Name of the product that the feedback is about (if any) in type str
            product = None  # Not on website

            # User, name of the user or encrypted user name (if any) in type str
            user = None  # Not on website

            # Deals by user (if any) in type int or str (if range)
            deals = None  # Not on website

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
