# ----------------------------------------------------------
# This is a template the Empire Market
# Fill the indicated fields with answers, if you cannot
# find the specific field in the market. Let the function return None.
# ----------------------------------------------------------
#ONLY VENDOR RIGHT NOW
# -- IMPORT
from dateutil.parser import parse

# Local import
from .scraper import Scraper, ProductScraper, VendorScraper


class EmpiremarketScraper(Scraper):

    def pagetype(self, soup):
        try:
            if soup.find('h1', {'class': 'seth1'}).find('i').text == '| User Profile':
                return 'vendor'
        except:
            raise Exception("Unknown type")


class EmpiremarketVendorScraper(VendorScraper):

    def vendor_name(self):
        return self.soup.find('h1', {'class' : 'seth1'}).text.split(' |')[0]

    def score(self):
        return (float(self.soup.find('p', {'class' : 'bold'}).find('b').text),100)

    def registration(self):
        return parse(self.soup.find('span', {'class' : 'bold1'}).text)

    def last_login(self):
        return parse(self.soup.find_all('tbody')[1].find_all('td')[7].text)

    def sales(self):
        s = self.soup.find('h3', {'class': 'user_info_mid_head'}).find('span').text
        return s[s.find("(") + 1:s.find(")")]

    def info(self):
        if soup.find('a', {'class': 'tablinks focus'}).text == 'About':
            return self.soup.find('p', {'style': "word-wrap: break-word; white-space: pre-wrap;"}).text

    def feedback(self):
        return None

    def pgp(self):
        return None