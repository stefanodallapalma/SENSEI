from markets.MarketScrape import MarketScrape
from markets.bean.Vendor import Vendor
from markets.rules.VendorRules import VendorRules
from markets.bean.Product import Product
from markets.rules.ProductRules import ProductRules
from markets.bean.Feedback import Feedback
from datetime import datetime as dt
from bs4 import BeautifulSoup
import os

class BerlusconiScrape(MarketScrape):

    def product_scrape(self, html_page):
        """
        Extract info on vendor html page\n
        Input: html page class\n
        Return value: product extracted
        """

        productRules = ProductRules(html_page)

        product = Product()

        product.timestamp = html_page.timestamp
        product.market = html_page.marketplace.name

        product.name = productRules.name()
        product.product_class = productRules.product_class()
        product.category = productRules.category()
        product.subcategory = productRules.subcategory()
        product.vendor = productRules.vendor()
        product.price_eur = productRules.price_eur()
        product.price_btc = productRules.price_btc()
        product.stock = productRules.stock()
        product.shipping_options = productRules.shipping_options()
        product.escrow_type = productRules.escrow_type()
        product.ships_from = productRules.ships_from()
        product.ships_to = productRules.ships_to()
        product.items_sold = productRules.items_sold()
        product.orders_sold_since = productRules.orders_sold_since()
        product.details = productRules.details()
        product.terms_and_conditions = productRules.terms_and_conditions()

        return product


    def vendor_scrape(self, html_page):
        """
        Extract info on vendor html page\n
        Input: html page class\n
        Return value: vendor extracted
        """

        vendorRules = VendorRules(html_page)

        vendor = Vendor()

        vendor.timestamp = html_page.timestamp
        vendor.market = html_page.marketplace.name

        vendor.name = vendorRules.name()
        vendor.dream_market_rating = vendorRules.dream_market_rating()
        vendor.last_seen = vendorRules.last_seen()
        vendor.since = vendorRules.since()
        vendor.ships_from = vendorRules.ships_from()
        vendor.rating = vendorRules.rating()
        vendor.orders_finalized = vendorRules.orders_finalized()
        vendor.finalized_early = vendorRules.finalized_early()
        vendor.profile = vendorRules.profile()
        vendor.terms_conditions = vendorRules.terms_conditions()
        vendor.pgp = vendorRules.pgp()
        #vendor.feedback = self.feedback_scrape(url_feedback_tab)

        return vendor


    def feedback_scrape(self, html_page):
        soup_feedback_tab = BeautifulSoup(open(html_page), "html.parser")

        rating = None

        feedbacks = []

        for feedback in soup_feedback_tab.find_all('div',{'class':'row'})[2].find_all('tr')[1:]: #loop per review
            format = "%Y-%m-%d %H:%M:%S"

            # The rating is shown as a 'thumbs up' or 'thumbs down' picture
            if feedback.find_all('td')[0].find_all('i', {'class':"fa fa-thumbs-o-up"}):          
                rating='Thumbs Up'
            if feedback.find_all('td')[0].find_all('i', {'class':"fa fa-thumbs-o-down"}):
                rating='Thumbs Down'
            
            # Feedback - parsing rules
            new_feedback = Feedback()

            # Content of message
            new_feedback.message = feedback.find_all('td')[1].text
            
            # Buyer feedback
            new_feedback.buyer = feedback.find_all('td')[2].text
            
            # find order count
            count = feedback.find_all('td')[2].text
            new_feedback.buyer_order_count = count[count.find("[")+1:count.find("]")]
            
            # Date of review
            new_feedback.date = dt.strptime(feedback.find_all('td')[3].text[:-4], format).isoformat()
            
            # Price in eur
            new_feedback.price=feedback.find_all('td')[4].text
        
            feedbacks.append(new_feedback)
        
        return feedbacks

    # STUB !!!!!!!!!!
    def getVendorTabs(self, url):
        """
        This function takes 4 tabs from main url vendor page\n
        Input: url page\n
        Return: 4 tabs: profile, termcondition, pgp and feedback tabs
        """

        profile_tab = url
        termcondition_tab = os.path.splitext(url)[0] + "&tab=2.htm" 
        pgp_tab = os.path.splitext(url)[0] + "&tab=3.htm"
        feedback_tab = os.path.splitext(url)[0] + "&tab=4.htm"

        return profile_tab, termcondition_tab, pgp_tab, feedback_tab


    # STUB !!!!!!!!!!
    def getProductTabs(self, url):
        """
        This function takes 4 tabs from main url vendor page\n
        Input: url page\n
        Return: 4 tabs: profile, termcondition, pgp and feedback tabs
        """

        profile_tab = url
        termcondition_tab = os.path.splitext(url)[0] + "&tab=2.htm"
        feedback_tab = os.path.splitext(url)[0] + "&tab=3.htm"

        return profile_tab, termcondition_tab, feedback_tab