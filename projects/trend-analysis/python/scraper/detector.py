# ----------------------------------------------------------
# This is a module that identifies market
# To add a market, add an if statement.
# find a specific field in the page that uniquely identifies the market
# ----------------------------------------------------------
from .enum import Market


def identify_market(soup):
    try:
        # BERLUSCONI MARKET
        if soup.find('img', {'alt': "BERLUSCONI MARKET"}): #berlusconi image in page
            return Market.BERLUSCONI

        # APOLLON MARKET
        if 'Apollon' in soup.find('span', {'class': 'bigger-90'}).text:
            return Market.APOLLON

        # AGARTHA MARKET
        if 'Agartha' in soup.find('div', {'id': 'page-heading'}).text:
            return Market.AGARTHA

        # TOCHKA MARKET
        if 'Tochka' in soup.find_all('a', {'class': 'item'})[-1].text:
            return Market.TOCHKA

        # DRUGSMEDICINE Market
        if soup.find('div', {'class': 'fix grid-3-12'}).find('img', {'id': 'logo_image'}):
            return Market.DRUGSMEDICINE

        # CANNAHOME Market
        if soup.find('img', {'alt': 'CannaHome'}):  # If the image with this alt exists.
            return Market.CANNAHOME

        # Silk Road 3.1
        if 'Silk Road 3' in soup.find('div', {'id': 'd'}).text:
            return Market.SILKROAD3

        # Empire Market
        if 'Empire Market' in soup.find('div', {'class': 'footer'}).text:
            return Market.EMPIREMARKET

        # SURFACE WEB: directdrugs
        if soup.find('div', {'class': 'site-branding'}).find('img',
                                                             {'alt': 'DirectDrugs. Buy research drugs.'}):
            return Market.DIRECTDRUGS

        # SURFACE WEB: drugscenter
        if soup.find('div', {'class': 'copyright-footer'}).find('strong').text == 'drugs-center.biz':
            return Market.DRUGSCENTER

        # SURFACE WEB: palmetto
        if soup.find('div', {'class': 'header'}).find('strong').text == 'Palmetto State Armory':
            return Market.PALMETTO

        # cannazon
        if 'cannazon' in soup.find('div', {'class': 'footer-bottom'}).text.lower():
            return Market.CANNAZON

        # darkmarket
        if soup.find('img', {'alt': 'DarkMarket'}):
            return Market.DARKMARKET
    except:
        raise Exception("Soup ERROR!")

    return Market.UNDEFINED








