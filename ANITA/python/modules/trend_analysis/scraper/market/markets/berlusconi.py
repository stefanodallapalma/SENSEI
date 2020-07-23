'''This is the specific file for the Berlusconi market that will be used by the main scraper'''
from datetime import datetime

# Local import
from .scraper import Scraper, ProductScraper, VendorScraper


class BerlusconiScraper(Scraper):

    def pagetype(self, soup):
        try:
            if soup.find('button', {'class': "btn btn-block btn-danger btn-lg"}).text == ' Buy Now ':
                return 'product'

            if soup.find('span', {'class': "label label-primary"}).text == 'Vendor':
                return 'vendor'
        except:
            raise Exception("Unknown type")


class BerlusconiProductScraper(ProductScraper):

    def product_name(self):
        return self.soup.find('ol',{'class':'breadcrumb'}).find_all('li')[3].text

    def vendor(self):
        return str(self.soup.select("a[href*=vendor]")[0].text.strip())

    def ships_from(self):
        if self.soup.find('div', {'class': 'col-sm-7'}).find_all('td')[3].text == 'Physical':
            return self.soup.find('div', {'class': 'col-sm-7'}).find_all('td')[7].text
        else:
            return None

    def ships_to(self):
        if self.soup.find('div', {'class': 'col-sm-7'}).find_all('td')[3].text == 'Physical':
            location = self.soup.find('div', {'class': 'col-sm-7'}).find_all('td')[9].text
            if 'Worldwide shipping' in location:
                return ['Worldwide']
            if 'Worldwide' in location:
                return ['Worldwide']
            if 'countries' in location:
                return ['Worldwide']
            else:
                return location.replace(' ', '').split(',')
        return None

    def price(self):
        return str(self.soup.find('div',{"class":"listing-price"}).strong.text)#[:-5]

    def info(self):
        if self.soup.find_all('li', {'class': 'active'})[2].text == 'Details':
            return ''.join(self.soup.find('p').text)
        else:
            return None

    def feedback(self):
        if 'No feedbacks yet' not in self.soup.find('div', {'class': 'col-md-12'}).text:
            feedback_list = []

            # loop to walk through the feedback
            for item in self.soup.find('div', {'class': 'col-md-12'}).find_all('tr')[1:]:
                # Find the score, can be numerical score: (score, scale), or 'positive', 'negative' or 'neutral'
                # for pos/neg scores.
                if item.find_all('td')[0].find_all('i', {'class': "fa fa-thumbs-o-up"}):
                    score = 'positive'
                elif item.find_all('td')[0].find_all('i', {'class': "fa fa-thumbs-o-down"}):
                    score = 'negative'
                elif item.find_all('td')[0].find_all('i', {'class': "fa fa-circle-o"}):
                    score = 'neutral'
                else:
                    score = None

                # The message of the feedback in type str
                message = item.find_all('td')[1].text

                # The time in datetime object or time ago in type str
                date = datetime.strptime(item.find_all('td')[3].text[:-4], "%Y-%m-%d %H:%M:%S")

                # User, name of the user or encrypted user name (if any) in type str
                user = item.find_all('td')[2].text[:-5]

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


class BerlusconiVendorScraper(VendorScraper):

    def vendor_name(self):
        return self.soup.find('h1').text.strip().split()[0]

    def score(self):
        # example: return soup.find_all('td')[5].text
        positive = str(self.soup.find("strong", {"style": "font-size:15px;"}).text)
        neutral = self.soup.find_all("strong", {"style": "font-size:15px;"})[1].text
        negative = self.soup.find_all("strong", {"style": "font-size:15px;"})[2].text
        return [positive, negative, neutral]

    def registration(self):
        date = str(self.soup.find("i", {"class": "fa-user"}).next_sibling.strip()[15:25])
        return datetime.strptime(date, "%Y-%m-%d")  # .strftime("%d/%m/%Y")

    def last_login(self):
        date = str(self.soup.find("i", {"class": "fa-feed"}).next_sibling.strip()[12:22])
        return datetime.strptime(date, "%Y-%m-%d")  # .strftime("%d/%m/%Y")

    def sales(self):
        return int(self.soup.find("strong", {"style": "font-size:15px;"}).text)

    def info(self):
        if self.soup.find_all('li', {'class': 'active'})[2].text == 'Profile':
            return self.soup.find_all('div', {'class': 'row'})[2].find_all('p')[10].text
        return None

    def feedback(self):
        feedback_list = []
        if self.soup.find_all('li', {'class': 'active'})[2].text == 'Feedback':
            # loop to walk through the feedback, thus create a list of all feedback
            for item in self.soup.find('tbody').find_all('tr'):

                # Find the score, can be numerical score: (score, scale), or 'positive', 'negative' or 'neutral'
                # for pos/neg scores.
                if item.find_all('td')[0].find_all('i', {'class': "fa fa-thumbs-o-up"}):
                    score = 'positive'
                elif item.find_all('td')[0].find_all('i', {'class': "fa fa-thumbs-o-down"}):
                    score = 'negative'
                else:
                    score = 'error'

                # The message of the feedback in type str
                message = item.find_all('td')[1].text

                # The time in datetime object or time ago in type str
                date = datetime.strptime(item.find_all('td')[3].text[:-4], "%Y-%m-%d %H:%M:%S")

                # Name of the product that the feedback is about (if any) in type str
                product = None  # fill in

                # User, name of the user or encrypted user name (if any) in type str
                user = item('td')[2].text.split()[0]

                # Deals by user (if any) in type int or str (if range)
                deals = int(item('td')[2].text.split()[1][1:-1])

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
