from .market_enum import Market
from .markets.agartha import AgarthaScraper


def get_scraper_instance(market):
    if market == Market.AGARTHA or (isinstance(market, str) and market.upper() == Market.AGARTHA.name):
        return AgarthaScraper()