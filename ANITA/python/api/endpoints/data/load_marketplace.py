from flask import request, Response, json
from zipfile import ZipFile
import os, shutil
from os.path import join

from html_pages.utils.HtmlPageUtils import get_html_pages
from html_pages.bean.Category import Category
from html_pages.bean.Marketplace import Marketplace
from scraper.BerlusconiScrape import BerlusconiScrape
from database.anita.AnitaDB import AnViProDB

upload_zip_path = "../resources/zip/"
zip_path = upload_zip_path + "tmpFile.zip"
db_parameters_path = "../resources/db_parameters"


def load_data():
    file = request.files["file"]

    print("ZIP STEP")
    # Save zip, extract all files and remove zip file
    file.save(zip_path)
    zip = ZipFile(zip_path, "r")
    zip.extractall(upload_zip_path)
    os.remove(zip_path)


    print("HTML INFO STEP")
    data_folder = os.listdir(upload_zip_path)[0]

    # No data inside zip file
    if data_folder is None:
        print("No folder")
        return Response(json.dumps("Data folder empty"), status=400, mimetype="application/json")

    # Analyse folder
    folder_path = join(upload_zip_path, data_folder)
    html_pages = get_html_pages(folder_path)

    print("PROD/VEND STEP")
    products = []
    vendors = []

    for html_page in html_pages:
        # Detect the markets to use
        # TESTED ONLY WITH BERLUSCONI SCRAPER

        if html_page.marketplace == Marketplace.BERLUSCONI:
            scrape = BerlusconiScrape()
        else:
            scrape = None

        if scrape is not None:
            if html_page.category == Category.PRODUCT:
                product = scrape.product_scrape(html_page)
                product.timestamp = html_page.timestamp
                products.append(product)

            elif html_page.category == Category.VENDOR:
                vendor = scrape.vendor_scrape(html_page)
                vendor.timestamp = html_page.timestamp
                vendors.append(vendor)

    print("DB STEP")

    db = AnViProDB(db_parameters_path)
    db.insertVendors(vendors)
    print("VENDORS SAVED")

    db.insertProducts(products)
    print("PRODUCTS SAVED")

    shutil.rmtree(folder_path)

    return Response(json.dumps("Operation successfully"), status=200, mimetype="application/json")