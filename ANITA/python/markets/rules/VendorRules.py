from bs4 import BeautifulSoup
import pycountry
from datetime import datetime
from html_pages.bean.HtmlPage import HtmlPage

class VendorRules:

    def __init__(self, html_page):
        self._soup_profile_tab = BeautifulSoup(open(html_page.profile_path), "html.parser")
        self._soup_termcondition_tab = BeautifulSoup(open(html_page.term_and_condition_path), "html.parser")
        self._soup_pgp_tab = BeautifulSoup(open(html_page.pgp_path), "html.parser")

    def name(self):
        '''Returns the vendorname from the Berlusconi market'''
        return self._soup_profile_tab.find('h1').text.strip().split()[0]

    def dream_market_rating(self):
        '''Returns the positive rating of the dreammarket from the Berlusconi market'''
        positive = self._soup_profile_tab.find('a',{'style':'color:#41ad41;'}).text
        negative = self._soup_profile_tab.find('a',{'style':'color:red;'}).text
        return [positive,negative]

    def last_seen(self):
        '''Returns the last seen moment of the vendor'''
        date = str(self._soup_profile_tab.find("i", {"class": "fa-feed"}).next_sibling.strip()[12:22])
        return datetime.strptime(date, "%Y-%m-%d")#.strftime("%d/%m/%Y")

    def since(self):
        '''Returns the registration moment of the vendor'''
        date = str(self._soup_profile_tab.find("i", {"class": "fa-user"}).next_sibling.strip()[15:25])
        return datetime.strptime(date, "%Y-%m-%d")#.strftime("%d/%m/%Y")

    def ships_from(self):
        '''Returns where the vendor ships from'''
        country = self._soup_profile_tab.find("i", {"class": "fa fa-cube"}).next_sibling.strip()[13:]
        return self.get_country(country)

    def rating(self):
        '''Returns the rating of the vendor'''
        positive = str(self._soup_profile_tab.find("strong", {"style": "font-size:15px;"}).text)
        neutral = self._soup_profile_tab.find_all("strong", {"style": "font-size:15px;"})[1].text
        negative = self._soup_profile_tab.find_all("strong", {"style": "font-size:15px;"})[2].text
        return [positive,neutral,negative]

    def orders_finalized(self):
        '''Returns how may orders are finalized'''
        return self._soup_profile_tab.find("strong",{"style":"font-size:15px;"}).text

    def finalized_early(self):
        subsoup = self._soup_profile_tab.findAll('div', {'class': 'col-md-4 text-center'})[1]
        return subsoup.find('strong', {'style': "font-size:15px;"}).text

    def profile(self):
        '''Returns the profile of the vendor'''
        #return soup.find_all('div',{'class':'row'})[2].find_all('p')[10].text
        if 'Profile' in self._soup_profile_tab.find('h4').text:
            return self._soup_profile_tab.find_all('div',{'class':'row'})[2].find_all('p')[10].text
        return None

    def terms_conditions(self):
        '''Returns the profile of the vendor'''
        #return soup.find_all('div',{'class':'row'})[2].find_all('p')[10].text
        if 'Terms' in self._soup_termcondition_tab.find('h4').text:
            return self._soup_termcondition_tab.find_all('div',{'class':'row'})[2].find_all('p')[10].text
        return None

    def pgp(self):
        '''Returns the profile of the vendor'''
        #return soup.find_all('div',{'class':'row'})[2].find_all('p')[10].text
        if 'Vendor PGP' in self._soup_pgp_tab.find('h4').text:
            return self._soup_pgp_tab.find_all('div',{'class':'row'})[2].find_all('p')[10].text
        return None



    def get_country(self, abbreviation):
        try:
            if abbreviation == 'ZZ':
                return 'Unspecified'
            else:
                return pycountry.countries.get(alpha_2=abbreviation).name
        except:
            return 'Country_naming_error'