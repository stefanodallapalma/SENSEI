import json
import traceback

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

STATISTICAL_INFO = True
MESSAGE_LIMIT = 100

# Task ID
LOAD_DUMP_TASK_ID = "UPLOAD_DUMP"
REVERSE_LOAD_PAGE_TASK_ID = "UNDO_UPLOAD_DUMP"


@celery.task(bind=True)
def load_dump(self, dump_folder_path, market, timestamp):
    product_controller = ProductController()
    vendor_controller = VendorController()
    feedback_controller = FeedbackController()

    # Preconditions
    if not product_controller.exist():
        product_controller.create(encode="utf8mb4")
        print("Product table created")

    if not vendor_controller.exist():
        vendor_controller.create(encode="utf8mb4")
        print("Vendor table created")

    if not feedback_controller.exist():
        feedback_controller.create(encode="utf8mb4")
        print("Feedback table created")

    # Get files
    pages = getfiles(dump_folder_path, abs_path=True, ext_filter="html", recursive=True)

    content = {"file_analyzed": 0, "successfull_pages": 0, "failed_pages": 0, "total_files": len(pages), "#products": 0,
               "#vendors": 0, "#feedback": 0, "db_insert": False}

    if STATISTICAL_INFO:
        content["STATISTICAL INFO"] = {"page not analyzed": 0, "page not analyzed - error_pages": {},
                                       "page analysed - missing parameters": []}

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

    # Retrieve the last feedback id from the db
    id_feedback = feedback_controller.get_last_feedback_id()
    if id_feedback is None:
        id_feedback = 1
    else:
        id_feedback += 1

    for page in pages:
        # Extract info from an html o docker-composepage
        try:
            web_page_information, page_specific_data, irretrievable_info_json = scraper.extract_data(page, timestamp, market)
            if web_page_information.page_type.lower() == "product":
                print("Product {}".format(len(products) + 1))
            if web_page_information.page_type.lower() == "vendor":
                print("Vendor {}".format(len(vendors) + 1))

            if STATISTICAL_INFO:
                # Irretrievable rate and exceptions raised
                irretrievable_rate = irretrievable_info_json["irretrievable_rate"]
                exceptions = irretrievable_info_json["exception_params"]
                irretrievable_page = {"page": page, "missing_rate": irretrievable_rate, "exception_params": exceptions}
                content["STATISTICAL INFO"]["page analysed - missing parameters"].append(irretrievable_page)

            # Convert the information extracted into db models
            timestamp = web_page_information.date

            # Check if there are any feedback in the specific page
            feedback = None
            if page_specific_data.__dict__["feedback"]:
                feedback = json.loads(json.dumps(page_specific_data.__dict__), cls=FeedbackScraperDecoder)
                print("Feedback type: {}".format(type(feedback)))
                for i in range(len(feedback)):
                    feedback[i].id = id_feedback
                    feedback_list.append(feedback[i])
                content["#feedback"] = len(feedback_list)

            if web_page_information.page_type.lower() == "product":
                product = json.loads(json.dumps(page_specific_data.__dict__), cls=ProductScraperDecoder)
                product.market = market
                product.timestamp = timestamp

                # In the product and vendor it is saved just the id of the feedback> The feedback will be saved in
                # another json and db table
                product.feedback = None
                if feedback:
                    product.feedback = id_feedback

                products.append(product)
                content["#products"] = len(products)
            else:
                vendor = json.loads(json.dumps(page_specific_data.__dict__), cls=VendorScraperDecoder)
                vendor.market = market
                vendor.timestamp = timestamp

                # In the product and vendor it is saved just the id of the feedback> The feedback will be saved in
                # another json and db table
                vendor.feedback = None
                if feedback:
                    vendor.feedback = id_feedback

                vendors.append(vendor)
                content["#vendors"] = len(vendors)

            if feedback:
                id_feedback += 1

            successfull_pages += 1
            content["successfull_pages"] = successfull_pages
        except Exception as e:
            failed_pages += 1
            content["failed_pages"] = failed_pages

            if STATISTICAL_INFO:
                content["STATISTICAL INFO"]["page not analyzed"] += 1
                exception_name = type(e).__name__
                msg = exception_name + " - " + str(e)

                if msg not in content["STATISTICAL INFO"]["page not analyzed - error_pages"]:
                    content["STATISTICAL INFO"]["page not analyzed - error_pages"][msg] = 0

                content["STATISTICAL INFO"]["page not analyzed - error_pages"][msg] += 1

        page_analyzed += 1
        content["file_analyzed"] = page_analyzed

        if (page_analyzed % update_value) == 0 or page_analyzed == len(pages):
            self.update_state(state='PROGRESS', meta=content)

    print("Products: {}".format(len(products)))
    print("Vendors: {}".format(len(vendors)))
    print("Feedback: {}".format(len(feedback_list)))

    products = remove_null_products(products)
    vendors = remove_null_vendors(vendors)
    print("Products not null: {}".format(len(products)))
    print("Vendors not null: {}".format(len(vendors)))

    print("REMOVING DUPLICATES...")
    products = remove_products_duplicates(products)
    vendors = remove_vendors_duplicates(vendors)
    feedback_list = remove_unreference_feedback(feedback_list, products, vendors)
    print("DUPLICATES REMOVED")

    print("Products: {}".format(len(products)))
    print("Vendors: {}".format(len(vendors)))
    print("Feedback: {}".format(len(feedback_list)))
    content["#products"] = len(products)
    content["#vendors"] = len(vendors)

    # Rates
    if STATISTICAL_INFO:
        successfull_rate = (successfull_pages/len(pages))*100
        failure_rate = (failed_pages / len(pages)) * 100
        content["STATISTICAL INFO"]["successfull_rate"] = str(successfull_rate) + "%"
        content["STATISTICAL INFO"]["failure_rate"] = str(failure_rate) + "%"

    self.update_state(state='PROGRESS', meta=content)

    # Database step
    try:
        if products:
            product_controller.insert_beans(products)

        if vendors:
            vendor_controller.insert_beans(vendors)

        if feedback_list:
            feedback_controller.insert_beans(feedback_list)
    except:
        traceback.print_exc()
        content["error"] = "Database error"
        self.update_state(state=states.FAILURE, meta=content)
        return content

    content["db_insert"] = True
    self.update_state(state=states.SUCCESS, meta=content)

    return content


# TO DO: REFACTORING
def remove_null_products(products):
    notnull_products = []

    for product in products:
        if product.timestamp is not None and product.market is not None and product.name is not None and\
                product.price is not None:
            notnull_products.append(product)

    return notnull_products


# TO DO: REFACTORING
def remove_null_vendors(vendors):
    notnull_vendors = []

    for vendor in vendors:
        if vendor.timestamp is not None and vendor.market is not None and vendor.name is not None:
            notnull_vendors.append(vendor)

    return notnull_vendors


def remove_unreference_feedback(feedback_list, products, vendors):
    ref_feedback_list = []

    ids = []
    for product in products:
        if product.feedback:
            ids.append(product.feedback)

    for vendor in vendors:
        if vendor.feedback:
            ids.append(vendor.feedback)

    for feedback in feedback_list:
        if feedback.id in ids:
            ref_feedback_list.append(feedback)

    return ref_feedback_list


# TO DO: REFACTORING
def remove_products_duplicates(products):
    new_products = []

    for product in products:
        i = 0

        while i < len(new_products) and not \
                (new_products[i].timestamp == product.timestamp and
                 new_products[i].market.lower() == product.market.lower() and
                 new_products[i].name.lower() == product.name.lower() and
                 new_products[i].vendor.lower() == product.vendor.lower() and
                 new_products[i].price.lower() == product.price.lower()):

            i += 1

        if i >= len(new_products):
            new_products.append(product)

    return new_products


# TO DO: REFACTORING
def remove_vendors_duplicates(vendors):
    new_vendors = []

    i = 0
    for vendor in vendors:
        i = 0
        while i < len(new_vendors) and not \
                (new_vendors[i].timestamp == vendor.timestamp and
                 new_vendors[i].market.lower() == vendor.market.lower() and
                 new_vendors[i].name.lower() == vendor.name.lower()):
            i += 1

        if i >= len(new_vendors):
            new_vendors.append(vendor)

    return new_vendors