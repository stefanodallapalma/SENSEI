import json
import traceback
from os.path import basename, normpath

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
                #print("Feedback type: {}".format(type(feedback)))

                """for i in range(len(feedback)):
                    feedback[i].id = id_feedback
                    feedback_list.append(feedback[i])
                content["#feedback"] = len(feedback_list)
                print("FEEDBACK")
                print(feedback)
                """
            if web_page_information.page_type.lower() == "product":
                product = json.loads(json.dumps(page_specific_data.__dict__), cls=ProductScraperDecoder)
                product.market = market
                product.timestamp = timestamp

                if feedback:
                    try:
                        print("FB PRODUCT")
                        if product not in products and not product.isnull():
                            product.feedback = id_feedback
                            print(product.feedback)
                            id_feedback += 1
                        else:
                            index_original_product = products.index(product)
                            original_product = products[index_original_product]
                            if original_product.feedback:
                                for feedback_elem in feedback:
                                    feedback_elem.id = original_product.feedback
                                print(original_product.feedback)
                            else:
                                products[index_original_product].feedback = id_feedback
                                print(products[index_original_product].feedback)
                                id_feedback += 1

                        feedback_list += feedback
                        content["#feedback"] = len(feedback_list)

                    except ValueError as e:
                        # No original found: null case - ignore
                        pass

                if product not in products and not product.isnull():
                    products.append(product)
                    content["#products"] = len(products)
                    print("Product {}".format(len(products)))

                # In the product and vendor it is saved just the id of the feedback> The feedback will be saved in
                # another json and db table
            else:
                vendor = json.loads(json.dumps(page_specific_data.__dict__), cls=VendorScraperDecoder)
                vendor.market = market
                vendor.timestamp = timestamp

                # In the product and vendor it is saved just the id of the feedback> The feedback will be saved in
                # another json and db table
                if feedback:
                    try:
                        print("FB VENDOR")
                        if vendor not in vendors and not vendor.isnull():
                            vendor.feedback = id_feedback
                            print(vendor.feedback)
                            id_feedback += 1
                        else:
                            index_original_vendor = vendors.index(vendor)
                            original_vendor = vendors[index_original_vendor]
                            if original_vendor.feedback:
                                for feedback_elem in feedback:
                                    feedback_elem.id = original_vendor.feedback
                                print(original_vendor.feedback)
                            else:
                                vendors[index_original_vendor].feedback = id_feedback
                                print(vendors[index_original_vendor].feedback)
                                id_feedback += 1

                        feedback_list += feedback
                        content["#feedback"] = len(feedback_list)
                    except ValueError as e:
                        # No original found: null case - ignore
                        pass

                if vendor not in vendors and not vendor.isnull():
                    vendors.append(vendor)
                    content["#vendors"] = len(vendors)
                    print("Vendor {}".format(len(vendors)))

            successfull_pages += 1
            content["successfull_pages"] = successfull_pages
        except Exception as e:
            file_name = basename(normpath(page))
            print("ERROR with the page \"{}\"".format(file_name))
            print("MESSAGE: {}".format(str(e)))
            print("TRACEBACK")
            traceback.print_exc()

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

    """products, feedback_list = remove_null_products(products, feedback_list)
    vendors, feedback_list = remove_null_vendors(vendors, feedback_list)

    print("Products not null: {}".format(len(products)))
    print("Vendors not null: {}".format(len(vendors)))
    print("Feedback: {}".format(len(feedback_list)))

    print("REMOVING DUPLICATES...")
    products, feedback_list = remove_products_duplicates(products, feedback_list)
    vendors, feedback_list = remove_vendors_duplicates(vendors, feedback_list)
    feedback_list = remove_feedback_duplicates(feedback_list)
    feedback_list = remove_unreference_feedback(feedback_list, products, vendors)
    print("DUPLICATES REMOVED")

    print("Products: {}".format(len(products)))
    print("Vendors: {}".format(len(vendors)))
    print("Feedback: {}".format(len(feedback_list)))
    content["#products"] = len(products)
    content["#vendors"] = len(vendors)"""

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
def remove_null_products(products, feedback_list):
    notnull_products = []
    notnull_feedback = []

    feedback_index_removed = []

    # All the pk must be not null
    for product in products:
        if not product.isnull():
            notnull_products.append(product)
        else:
            if product.feedback:
                feedback_index_removed.append(product.feedback)

    # Remove all feedback connected with null products
    for feedback in feedback_list:
        if feedback.id not in feedback_index_removed:
            notnull_feedback.append(feedback)

    return notnull_products, notnull_feedback


# TO DO: REFACTORING
def remove_null_vendors(vendors, feedback_list):
    notnull_vendors = []
    notnull_feedback = []

    feedback_index_removed = []

    # All the pk must be not null
    for vendor in vendors:
        if not vendor.isnull():
            notnull_vendors.append(vendor)
        else:
            if vendor.feedback:
                feedback_index_removed.append(vendor.feedback)

    for feedback in feedback_list:
        if feedback.id not in feedback_index_removed:
            notnull_feedback.append(feedback)

    return notnull_vendors, notnull_feedback


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
def remove_products_duplicates(products, feedback_list):
    new_products = []

    feedback_duplicate_dct = {}

    for product in products:
        i = 0

        # id feedback of a possible duplicate
        feedback_id = product.feedback

        while i < len(new_products) and new_products[i] != product:
            i += 1

        if i >= len(new_products):
            new_products.append(product)
        else:
            # Id of the original product
            original_feedback_id = new_products[i].feedback
            feedback_duplicate_dct[feedback_id] = original_feedback_id

    # Replace duplicate feedback id with the original one
    for feedback in feedback_list:
        if feedback.id in feedback_duplicate_dct:
            feedback.id = feedback_duplicate_dct[feedback.id]

    return new_products, feedback_list


# TO DO: REFACTORING
def remove_vendors_duplicates(vendors, feedback_list):
    new_vendors = []

    feedback_duplicate_dct = {}

    for vendor in vendors:
        i = 0

        # id feedback of a possible duplicate
        feedback_id = vendor.feedback

        while i < len(new_vendors) and new_vendors[i] != vendor:
            i += 1

        if i >= len(new_vendors):
            new_vendors.append(vendor)
        else:
            # Id of the original product
            original_feedback_id = new_vendors[i].feedback
            feedback_duplicate_dct[feedback_id] = original_feedback_id

    # Replace duplicate feedback id with the original one
    for feedback in feedback_list:
        if feedback.id in feedback_duplicate_dct:
            feedback.id = feedback_duplicate_dct[feedback.id]

    return new_vendors, feedback_list


def remove_feedback_duplicates(feedback_list):
    new_feedback_list = []

    for feedback in feedback_list:
        i = 0

        while i < len(new_feedback_list) and new_feedback_list[i] != feedback:
            i += 1

        if i >= len(new_feedback_list):
            new_feedback_list.append(feedback)

    return new_feedback_list
