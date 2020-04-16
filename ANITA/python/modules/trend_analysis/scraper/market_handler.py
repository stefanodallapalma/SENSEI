from .market_enum import Market
from .markets.agartha import AgarthaScraper
from .markets.apollon import ApollonScraper
from .markets.berlusconi import BerlusconiScraper
from .markets.cannahome import CannahomeScraper
from .markets.cannazon import CannazonScraper
from .markets.darkmarket import DarkmarketScraper
from .markets.directdrugs import DirectdrugsScraper
from .markets.drugscenter import DrugscenterScraper
from .markets.drugsmedicine import DrugsmedicineScraper
from .markets.empiremarket import EmpiremarketScraper
from .markets.palmetto import PalmettoScraper
from .markets.silkroad3 import Silkroad3Scraper
from .markets.tochka import TochkaScraper


def get_scraper_instance(market):
    if market == Market.AGARTHA or (isinstance(market, str) and market.upper() == Market.AGARTHA.name):
        return AgarthaScraper()

    elif market == Market.APOLLON or (isinstance(market, str) and market.upper() == Market.APOLLON.name):
        return ApollonScraper()

    elif market == Market.BERLUSCONI or (isinstance(market, str) and market.upper() == Market.BERLUSCONI.name):
        return BerlusconiScraper()

    elif market == Market.CANNAHOME or (isinstance(market, str) and market.upper() == Market.CANNAHOME.name):
        return CannahomeScraper()

    elif market == Market.CANNAZON or (isinstance(market, str) and market.upper() == Market.CANNAZON.name):
        return CannazonScraper()

    elif market == Market.DARKMARKET or (isinstance(market, str) and market.upper() == Market.DARKMARKET.name):
        return DarkmarketScraper()

    elif market == Market.DIRECTDRUGS or (isinstance(market, str) and market.upper() == Market.DIRECTDRUGS.name):
        return DirectdrugsScraper()

    elif market == Market.DRUGSCENTER or (isinstance(market, str) and market.upper() == Market.DRUGSCENTER.name):
        return DrugscenterScraper()

    elif market == Market.DRUGSMEDICINE or (isinstance(market, str) and market.upper() == Market.DRUGSMEDICINE.name):
        return DrugsmedicineScraper()

    elif market == Market.EMPIREMARKET or (isinstance(market, str) and market.upper() == Market.EMPIREMARKET.name):
        return EmpiremarketScraper()

    elif market == Market.PALMETTO or (isinstance(market, str) and market.upper() == Market.PALMETTO.name):
        return PalmettoScraper()

    elif market == Market.SILKROAD3 or (isinstance(market, str) and market.upper() == Market.SILKROAD3.name):
        return Silkroad3Scraper()

    elif market == Market.TOCHKA or (isinstance(market, str) and market.upper() == Market.TOCHKA.name):
        return TochkaScraper()

    else:
        raise Exception("Scraper not implemented yet")
