# -- IMPORT
from datetime import datetime

# Local import
from .scraper import Scraper, ProductScraper, VendorScraper


class ApollonScraper(Scraper):

    def pagetype(self, soup):
        try:
            if soup.find('h3').text == 'Item For Sale : ':
                return 'product'

            if soup.find('h3').text == 'User Profile : ':
                return 'vendor'
        except:
            raise Exception("Unknown type")


class ApollonProductScraper(ProductScraper):

    def product_name(self):
        return self.soup.find('div', {'class' : 'col-sm-12'}).find('a').text

    def vendor(self):
        return self.soup.find_all('div', {'class' : 'col-sm-12'})[1].find('small').find('b').text.split('(')[0][:-1]

    def ships_from(self):
        ship_from = self.soup.find_all('div', {'class': 'col-sm-12'})[1].find_all('small')[12]
        for item in ship_from('b'):
            item.decompose()
        return ship_from.text[1:-1]

    def ships_to(self):
        return self.soup.find_all('div', {'class' : 'col-sm-12'})[1].find_all('small')[14].text[1:-1]

    def price(self):
        return ' '.join(self.soup.find('span', {'class' : 'label label-info'}).text.split(' ')[3:5])

    def info(self):
        if self.soup.find('li', {'class': 'active'}).text == 'Product Description':
            return self.soup.find('pre').text

    def feedback(self):
        # loop to walk through the feedback
        feedback_list = []
        if self.soup.find('li', {'class': 'active'}).text == 'Feedback':
            for item in self.soup.find('div', {'class': 'table-responsive'}).find('tbody').find('tbody').find_all('tr'):

                # Find the score, can be numerical score: (score, scale), or 'positive', 'negative' or 'neutral'
                # for pos/neg scores.
                score_line = item.find_all('td')[0].text
                if score_line == '☒':
                    score = 'negative'
                elif score_line == '☑':
                    score = 'positive'
                else:
                    score = None

                # The message of the feedback in type str
                message = item.find_all('td')[1].small.text

                # The time in datetime object or time ago in type str
                time_line = item.find_all('td')[4]
                for a in time_line('a'):
                    a.decompose()
                date = datetime.strptime(time_line.text, "%b %d, %Y %H:%M")

                # User, name of the user or encrypted user name (if any) in type str
                user = item.find_all('td')[2].text

                # in json format
                feedback_json = {
                    'score': score,
                    'message': message,
                    'date': date,
                    'user': user,
                }
                feedback_list.append(feedback_json)
        else:
            feedback_list = None

        return feedback_list


class ApollonVendorScraper(VendorScraper):

    def vendor_name(self):
        return self.soup.find('div', {'class' : 'col-sm-12'}).find('small').find('b').text.split('(')[0][:-1]

    def score(self):
        score = self.soup.find('div', {'class': 'col-sm-5'}).find_all('span')[4]
        for item in score('b'):
            item.decompose()
        return (int(score.text[1:-2]), 100)

    def registration(self):
        date = self.soup.find('div', {'class': 'col-sm-5'}).find_all('span')[5]
        for item in date('b'):
            item.decompose()
        date_string = date.text
        return datetime.strptime(date_string, "%b %d, %Y")

    def last_login(self):
        date = self.soup.find('div', {'class': 'col-sm-5'}).find_all('span')[6]
        for item in date('b'):
            item.decompose()
        date_string = date.text
        return datetime.strptime(date_string, "%b %d, %Y")

    def sales(self):
        sales = self.soup.find('div', {'class': 'col-sm-2'}).find_all('span')[0]
        for item in sales('b'):
            item.decompose()
        return sales.text

    def info(self):
        return self.soup.find_all('div', {'class' : 'panel panel-default'})[5].text

    def feedback(self):
        feedback_list = []
        if self.soup.find('li', {'class': 'active'}).text in ['Positive Feedback', 'Negative Feedback', 'Neutral Feedback']:

            # Find the score, can be numerical score: (score, scale), or 'positive', 'negative' or 'neutral' for pos/neg scores.
            if self.soup.find('li', {'class': 'active'}).text == 'Positive Feedback':
                score = 'positive'
            elif self.soup.find('li', {'class': 'active'}).text == 'Negative Feedback':
                score = 'negative'
            elif self.soup.find('li', {'class': 'active'}).text == 'Neutral Feedback':
                score = 'neutral'
            else:
                score = None

            # loop to walk through the feedback
            for item in self.soup.find('tbody').find_all('tr'):

                # The message of the feedback in type str
                message = item('td')[1]('small')[0].text

                # The time in datetime object or time ago in type str
                time_line = item('td')[4]
                for a in time_line('a'):
                    a.decompose()
                date = datetime.strptime(time_line.text, "%b %d, %Y %H:%M")

                # Name of the product that the feedback is about (if any) in type str
                product_line = item('td')[1]
                for small in product_line('small'):
                    small.decompose()
                product = product_line.text

                # User, name of the user or encrypted user name (if any) in type str
                user = item('td')[2].text

                # Deals by user (if any) in type int or str (if range)
                deals = None  # not present in this site

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