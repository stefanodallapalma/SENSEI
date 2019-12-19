from flask import request
import os
from zipfile import ZipFile
from os import listdir
from os.path import isfile, join, splitext
import json

from html_pages.utils.HtmlPageUtils import get_html_pages

uploads_path = "uploads"
tmp_zip_path = uploads_path + "/tmpFile.zip"


def load_data():
    filed = request.files["file"]
    filed.save(tmp_zip_path)
    
    print("File saved")

    zip = ZipFile(tmp_zip_path, "r")
    zip.extractall(uploads_path)

    print("File unzipped")

    os.remove(tmp_zip_path)

    print("Zip File removed")

    data_folder = os.listdir(uploads_path)[0]

    # No data inside zip file
    if data_folder is None:
        print("No folder")
        return False
    

    # Analyse folder
    folder_path = join(uploads_path, data_folder)
    print("Folder path: ", folder_path)
        
    '''
    product_folder = None
    vendor_folder = None

    for f in listdir(folder_path):
        if "Products" in f:
            product_folder = f
        elif "Vendors" in f:
            vendor_folder = f
    
    if product_folder is not None:
        product_folder_path = join(folder_path, product_folder)
        product_dict = get_dict(product_folder_path)
    
    if vendor_folder is not None:
        vendor_folder_path = join(folder_path, vendor_folder)
        vendor_dict = get_dict(vendor_folder_path)
    '''

    html_pages = get_html_pages(folder_path)
    print("Size: ", len(html_pages))

    for html_page in html_pages:
        print(str(html_page))

    '''
    products = []
    vendors = []

    for html_page in html_pages:
        scrape = None
        if "Berlusconi" in html_page.market:
            scrape = BerlusconiScrape()

        if "Products" in html_page.category:
            product = scrape.product_scrape(html_page.html_page_path)
            json_product = json.dumps(product, default=lambda o: o.__dict__)
            products.append(product)
        elif "Vendors" in html_page.category:
            vendor = scrape.vendor_scrape(html_page.html_page_path)
            json_vendor = json.dumps(vendor, default=lambda o: o.__dict__)
            vendors.append(vendor)

    # TO DO: Save json
'''

    return True

def extract_pages_name(pages):
    names = set()

    for page in pages:
        page_without_ext = splitext(page)[0]
        split = page_without_ext.split("&")
        for word in split:
            if "code" in word:
                names.add(word.split("=")[1])
    
    return names

def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))


def get_dict(folder_path):
    # Key   -> timestamp
    # Value -> marketplace dictionary
    product_dict = {}

    # Second level: timestamps
    for timestamp in listdir(folder_path):
        # Key   -> marketplace
        # Value -> page dictionary
        market_dict = {}

        timestamp_folder_path = join(folder_path, timestamp)

        # Third level: marketplaces
        for market in listdir(timestamp_folder_path):
            # Key   -> page code
            # Value -> tabs
            pages_dict = {}

            pages = []
            market_folder_path = join(timestamp_folder_path, market)

            for page in listdir(market_folder_path):
                
                if isfile(join(market_folder_path, page)):
                    # Take the name of this page
                    pages.append(page)
            
            pages_code = extract_pages_name(pages)

            # For each code, extract all pages related
            for page_code in pages_code:
                tabs = []
                for page in pages:
                    if page_code in page:
                        tabs.append(page)
                
                pages_dict[page_code] = tabs
            
            market_dict[market] = pages_dict

        product_dict[timestamp] = market_dict