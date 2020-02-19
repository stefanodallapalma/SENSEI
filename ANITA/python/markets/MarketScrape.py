from abc import ABC, abstractmethod

class MarketScrape(ABC):
    
    @abstractmethod
    def product_scrape(self, html_page):
        pass

    @abstractmethod
    def vendor_scrape(self, html_page):
        pass

    @abstractmethod
    def feedback_scrape(self, html_page):
        pass