# Local import
from .scraper import Scraper, ProductScraper, VendorScraper


class TochkaScraper(Scraper):
    def __init__(self):
        self.product_scraper = TochkaProductScraper()
        self.vendor_scraper = TochkaVendorScraper()

    def pagetype(self, soup):
        try:
            if soup.find_all('div', {'class': "ui segment"})[1].find_all('h3')[0].text == 'Purchase':
                return 'product'

            if soup.find('h3', {'class': "ui dividing header"}).text == 'About':
                return 'vendor'
        except:
            raise Exception("Unknown type")


class TochkaProductScraper(ProductScraper):

    def product_name(self):
        title = self.soup.find('h2', {"ui dividing header"})
        for span in title('span'):
            span.decompose()
        return ' '.join(title.text.split())

    def vendor(self):
        return ' '.join(self.soup.find('div', {'class': "content card-header"}).text.split())[1:]

    def ships_from(self):
        return self.soup.find('table', {'class': "ui celled table fluid inverted green"}).find_all('span')[1].text

    def ships_to(self):
        return self.soup.find('table', {'class': "ui celled table fluid inverted green"}).find_all('span')[2].text

    def price(self):
        price_list = [' '.join(item.text.split()) for item in
                      self.soup.find('table', {'ui very basic table'}).find_all('td')]
        i = 0
        price_dict = dict()
        while i < len(price_list):
            price_dict[price_list[i]] = price_list[i + 1]
            i += 2
        return price_dict

    def info(self):
        return self.soup.find('div', {'ui segment'}).text

    def feedback(self):
        feedback_list = []

        # loop to walk through the feedback
        for item in self.soup.find('div', {'class', 'ui comments'}).find_all('div', {'class': 'comment'}):
            # Find the score, can be numerical score: (score, scale), or 'positive', 'negative' or 'neutral' for pos/neg scores.
            score = (item.find('span').text.split()[0], 5)

            # The message of the feedback in type str
            message = item.find('pre').text

            # The time in datetime object or time ago in type str
            date = item.find('span', {'class': 'date'}).text

            # User, name of the user or encrypted user name (if any) in type str
            user = item.find('a', {'class': 'author'}).text[1:]

            # in json format
            feedback_json = {
                'score': score,
                'message': message,
                'date': date,
                'user': user,
            }
            feedback_list.append(feedback_json)

        return feedback_list


class TochkaVendorScraper(VendorScraper):

    def vendor_name(self):
        return ' '.join(self.soup.find('div', {'class': "content card-header"}).text.split())[1:]

    def score(self):
        return (float(self.soup.find('div', {'class' : 'ui label dark-green tiny'}).find('span').text),5)

    def registration(self):
        return ' '.join(self.soup.find_all('div', {'class' : 'date'})[0].text.split()[1:])

    def last_login(self):
        return ' '.join(self.soup.find_all('div', {'class' : 'date'})[1].text.split()[2:])

    def sales(self):
        return None

    def info(self):
        return self.soup.find('div', {'class' : 'ui container'}).text

    def feedback(self):
        feedback_list = []

        # loop to walk through the feedback
        if self.soup.find_all('a', {'class': 'item active'})[1].text.split()[0] == 'Reviews':
            for item in self.soup.find('div', {'class': 'ui comments'}).find_all('div', {'class': 'comment'}):
                # Find the score, can be numerical score: (score, scale), or 'positive', 'negative' or 'neutral' for pos/neg scores.
                score = (item('span')[0].text.split()[0], 5)

                # The message of the feedback in type str
                message = item('pre')[0].text

                # The time in datetime object or time ago in type str
                date = item.find('span', {'class': 'date'}).text

                # Name of the product that the feedback is about (if any) in type str
                product = None  # not on website

                # User, name of the user or encrypted user name (if any) in type str
                user = item('a', {'class': 'author'})[0].text[1:]

                # Deals by user (if any) in type int or str (if range)
                deals = None  # not on website

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
