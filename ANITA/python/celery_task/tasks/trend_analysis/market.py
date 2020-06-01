import json

# Third party imports
from celery import states

# Local application imports
from celery_task.celery_app import celery
from utils.FileUtils import getfiles, save_json
from modules.trend_analysis.scraper.market.handler import get_scraper_instance
from database.anita.decoder.market_decoder import *
from database.anita.controller.ProductController import ProductController
from database.anita.controller.VendorController import VendorController
from database.anita.controller.FeedbackController import FeedbackController

DEBUG = False
MESSAGE_LIMIT = 100

# Task ID
LOAD_DUMP_TASK_ID = "UPLOAD_DUMP"
REVERSE_LOAD_PAGE_TASK_ID = "UNDO_UPLOAD_DUMP"


@celery.task(bind=True)
def load_dump(self, dump_folder_path, market, timestamp):
    # Get files
    pages = getfiles(dump_folder_path, abs_path=True, ext_filter="html", recursive=True)

    content = {"file_analyzed": 0, "successfull_pages": 0, "failed_pages": 0, "total_files": len(pages), "#products": 0,
               "#vendors": 0, "db_insert": False}

    if DEBUG:
        content["error_pages"] = {}
        content["irretrievable_pages_rate"] = []
        content["irretrievable_parameters_page"] = []

    self.update_state(state=states.STARTED, meta=content)

    update_value = int(len(pages) / MESSAGE_LIMIT)
    print(update_value)

    # Get market scraper
    scraper = get_scraper_instance(market.lower())

    products = []
    vendors = []
    feedback_list = []

    page_analyzed = 0
    successfull_pages = 0
    failed_pages = 0
    for page in pages:
        # Extract info from an html page
        try:
            web_page_information, page_specific_data, irretrievable_info_json = scraper.extract_data(page, timestamp, market)

            if DEBUG:
                # Irretrievable rate and exceptions raised
                irretrievable_rate = irretrievable_info_json["irretrievable_rate"]
                irretrievable_page_rate = {"page": page, "rate": irretrievable_rate}
                content["irretrievable_pages_rate"].append(irretrievable_page_rate)

                exceptions = irretrievable_info_json["exception_params"]
                irretrievable_page = {"page": page, "exception_params": exceptions}
                content["irretrievable_parameters_page"].append(irretrievable_page)

            # Convert the information extracted into db models
            timestamp = web_page_information.date
            if web_page_information.page_type.lower() == "product":
                product = json.loads(json.dumps(page_specific_data.__dict__), cls=ProductScraperDecoder)
                product.market = market
                product.timestamp = timestamp
                products.append(product)
                content["#products"] = len(products)
            else:
                vendor = json.loads(json.dumps(page_specific_data.__dict__), cls=VendorScraperDecoder)
                vendor.market = market
                vendor.timestamp = timestamp
                vendors.append(vendor)
                content["#vendors"] = len(vendors)

            # feedback = json.loads(data, cls=FeedbackScraperDecoder)
            # feedback_list += feedback

            successfull_pages += 1
            content["successfull_pages"] = successfull_pages
        except Exception as e:
            if "error_pages" not in content:
                content["error_pages"] = {}

            if str(e) not in content["error_pages"]:
                content["error_pages"][str(e)] = 1
            else:
                content["error_pages"][str(e)] = content["error_pages"][str(e)] + 1

            failed_pages += 1
            content["failed_pages"] = failed_pages

        page_analyzed += 1
        content["file_analyzed"] = page_analyzed

        if (page_analyzed % update_value) == 0 or page_analyzed == len(pages):
            self.update_state(state='PROGRESS', meta=content)

    print("Products: {}".format(len(products)))
    print("Vendors: {}".format(len(vendors)))

    print("REMOVING DUPLICATES...")
    products = remove_products_duplicates(products)
    vendors = remove_vendors_duplicates(vendors)
    print("DUPLICATES REMOVED")

    print("Products: {}".format(len(products)))
    print("Vendors: {}".format(len(vendors)))
    content["#products"] = len(products)
    content["#vendors"] = len(vendors)

    if DEBUG:
        # Rates
        successfull_rate = (successfull_pages/len(pages))*100
        failure_rate = (failed_pages / len(pages)) * 100
        content["successfull_rate"] = str(successfull_rate) + "%"
        content["failure_rate"] = str(failure_rate) + "%"
    self.update_state(state='PROGRESS', meta=content)

    product_controller = ProductController()
    vendor_controller = VendorController()
    feedback_controller = FeedbackController()

    try:
        # Preconditions
        if not product_controller.exist():
            product_controller.create()

        if not vendor_controller.exist():
            vendor_controller.create()

        """if not feedback_controller.exist():
            feedback_controller.create()"""

        if products:
            product_controller.insert_beans(products)

        if vendors:
            vendor_controller.insert_beans(vendors)

        """if feedback_list:
            feedback_controller.insert_beans(feedback_list)"""
    except Exception as e:
        content["error"] = str(e)
        self.update_state(state=states.FAILURE, meta=content)
        return content

    content["db_insert"] = True
    self.update_state(state=states.SUCCESS, meta=content)

    return content


def remove_products_duplicates(products):
    new_products = []

    i = 0
    for product in products:
        i = 0
        while i < len(new_products) and not \
                (new_products[i].timestamp == product.timestamp and
                 new_products[i].market == product.market and
                 new_products[i].name == product.name and
                 new_products[i].vendor == product.vendor):
            i += 1

        if i >= len(new_products):
            new_products.append(product)

    return new_products


def remove_vendors_duplicates(vendors):
    new_vendors = []

    i = 0
    for vendor in vendors:
        i = 0
        while i < len(new_vendors) and not \
                (new_vendors[i].timestamp == vendor.timestamp and
                 new_vendors[i].market == vendor.market and
                 new_vendors[i].name == vendor.name):
            i += 1

        if i >= len(new_vendors):
            new_vendors.append(vendor)

    return new_vendors