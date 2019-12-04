#from scraper.scrape.BerlusconiScrape import BerlusconiScrape
from flask import jsonify, request
import json

def berlusconi_vendor_list():
    return request.form("url")
    #scraper = BerlusconiScrape()

    #vendor = scraper.vendor_scrape(html_pages)


    #return json.dumps(vendor, default=lambda o: o.__dict__), 200
