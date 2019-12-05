from scraper.scrape.MarketScrape import MarketScrape
from scraper.bean.Vendor import Vendor
from scraper.bean.Product import Product
from scraper.bean.Feedback import Feedback
import datetime
from datetime import datetime as dt
from bs4 import BeautifulSoup
import os

class BerlusconiScrape(MarketScrape):

    def product_scrape(self, html_pages):
        pass


    def vendor_scrape(self, url):
        """
        Extract info on vendor html page\n
        Input: html pages -> 3 pages related to the vendor page\n
        Return value: vendor
        """

        format = "%Y-%m-%d"

        html_pages = self.getVendorTabs(url)

        if (len(html_pages) > 4):
            raise Exception("BerlusconiScrape exception: the lenght of html pages must be 4 or less")

        url_profile_tab = html_pages[0]
        url_termcondition_tab = html_pages[1]
        url_pgp_tab = html_pages[2]
        url_feedback_tab = html_pages[3]
        
        # WORKS ON LOCAL (open(...)). TO DO: ONLINE SUPPORT 
        soup_profile_tab = BeautifulSoup(open(url_profile_tab), "html.parser")
        soup_termcondition_tab = BeautifulSoup(open(url_termcondition_tab), "html.parser")
        soup_pgp_tab = BeautifulSoup(open(url_pgp_tab), "html.parser")


        # Vendor - Parsing rules
        vendor = Vendor()

        vendor.name = soup_profile_tab.find('h1').text.strip().split()[0]

        positive = soup_profile_tab.find('a',{'style':'color:#41ad41;'}).text
        negative = soup_profile_tab.find('a',{'style':'color:red;'}).text
        vendor.dream_market_rating = [positive,negative]
        
        date = str(soup_profile_tab.find("i", {"class": "fa-feed"}).next_sibling.strip()[12:22])
        vendor.last_seen = dt.strptime(date, format).isoformat()

        date = str(soup_profile_tab.find("i", {"class": "fa-user"}).next_sibling.strip()[15:25])
        vendor.since = dt.strptime(date, format).isoformat()

        vendor.ships_from = soup_profile_tab.find("i", {"class": "fa fa-cube"}).next_sibling.strip()[13:]
        
        positive = str(soup_profile_tab.find("strong", {"style": "font-size:15px;"}).text)
        neutral = soup_profile_tab.find_all("strong", {"style": "font-size:15px;"})[1].text
        negative = soup_profile_tab.find_all("strong", {"style": "font-size:15px;"})[2].text
        vendor.rating = [positive, neutral, negative]
        
        vendor.orders_finalized = soup_profile_tab.find("strong",{"style":"font-size:15px;"}).text

        subsoup=soup_profile_tab.findAll('div',{'class':'col-md-4 text-center'})[1]
        vendor.finalized_early = subsoup.find('strong',{'style':"font-size:15px;"}).text

        vendor.profile = soup_profile_tab.find_all('div',{'class':'row'})[2].find_all('p')[10].text
        
        vendor.terms_conditions = soup_termcondition_tab.find_all('div',{'class':'row'})[2].find_all('p')[10].text
        
        vendor.pgp = soup_pgp_tab.find_all('div',{'class':'row'})[2].find_all('p')[10].text

        vendor.feedback = self.feedback_scrape(url_feedback_tab)

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
            new_feedback.buyer = feedback.find_all('td')[2].text[:-6]
            
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