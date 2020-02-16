from scraper.BerlusconiScrape import BerlusconiScrape
from flask import request
import json

def berlusconi_product_list():
    url = request.values["url"]
    scraper = BerlusconiScrape()

    product = scraper.product_scrape(url)

    return json.dumps(product, default=lambda o: o.__dict__)

def berlusconi_vendor_list():
    url = request.values["url"]
    scraper = BerlusconiScrape()

    vendor = scraper.vendor_scrape(url)

    return json.dumps(vendor, default=lambda o: o.__dict__)
