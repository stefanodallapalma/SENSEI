from flask import request
from zipfile import ZipFile
import json
import os
from os.path import join

from html_pages.utils.HtmlPageUtils import get_html_pages
from html_pages.bean.Category import Category
from html_pages.bean.Marketplace import Marketplace
from scraper.BerlusconiScrape import BerlusconiScrape
from db.AnViProDB import AnViProDB

upload_zip_path = "../resources/zip/"
zip_path = upload_zip_path + "tmpFile.zip"
db_parameters_path = "../resources/db_parameters"


def load_data():
    filed = request.files["file"]
    filed.save(zip_path)
    
    print("File saved")

    zip = ZipFile(zip_path, "r")
    zip.extractall(upload_zip_path)

    print("File unzipped")

    os.remove(zip_path)

    print("Zip File removed")

    data_folder = os.listdir(upload_zip_path)[0]

    # No data inside zip file
    if data_folder is None:
        print("No folder")
        return False
    

    # Analyse folder
    folder_path = join(upload_zip_path, data_folder)
    print("Folder path: ", folder_path)


    html_pages = get_html_pages(folder_path)

    products = []
    vendors = []

    for html_page in html_pages:
        # Detect the scraper to use
        # TESTED ONLY WITH BERLUSCONI SCRAPER

        if html_page.marketplace == Marketplace.BERLUSCONI:
            scrape = BerlusconiScrape()
        else:
            scrape = None

        if scrape is not None:
            if html_page.category == Category.PRODUCT:
                product = scrape.product_scrape(html_page)
                product.timestamp = html_page.timestamp
                #products.append(json.dumps(product, default=lambda o: o.__dict__))
                products.append(product)

            elif html_page.category == Category.VENDOR:
                vendor = scrape.vendor_scrape(html_page)
                vendor.timestamp = html_page.timestamp
                vendors.append(vendor)
                #vendors.append(json.dumps(vendor, default=lambda o: o.__dict__))

            else:
                print("HTML PAGE UNDEFINED: ", html_page.category)

    print("Save info into db")

    db = AnViProDB(db_parameters_path)
    db.insertVendors(vendors)
    print("VENDORS SAVED")

    db.insertProducts(products)
    print("PRODUCTS SAVED")

    return True

def load_single_data():
    category = request.files["category"]
    marketplace = request.files["marketplace"]
    
