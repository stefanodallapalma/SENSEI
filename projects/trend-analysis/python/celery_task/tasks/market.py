import json
import traceback
from os.path import basename, normpath

# Third party imports
from celery import states

# Local application imports
from celery_task.celery_app import celery
from utils.FileUtils import getfiles
from scraper.handler import get_scraper_instance
from database.anita.decoder.market_decoder import *
from database.anita.controller.ProductController import ProductController
from database.anita.controller.VendorController import VendorController
from database.anita.controller.FeedbackController import FeedbackController
import modules.post_processing.product as pc_product
import modules.post_processing.vendor as pc_vendor
import modules.post_processing.pseudonym as pc_pseudonym
import modules.post_processing.feedback as pc_feedback

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
               "#vendors": 0, "#feedback": 0, "db_insert": False, "db_platform_updated": False}

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

    # Exit condition if there are 0 pages
    if not pages:
        self.update_state(state=states.SUCCESS, meta=content)
        return content

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
                        if product not in products and not product.isnull():
                            product.feedback = id_feedback
                            for feedback_elem in feedback:
                                feedback_elem.id = id_feedback
                            id_feedback += 1
                        else:
                            index_original_product = products.index(product)
                            original_product = products[index_original_product]
                            if original_product.feedback:
                                for feedback_elem in feedback:
                                    feedback_elem.id = original_product.feedback
                            else:
                                for feedback_elem in feedback:
                                    feedback_elem.id = id_feedback
                                products[index_original_product].feedback = id_feedback
                                id_feedback += 1

                        feedback_list += feedback
                        content["#feedback"] = len(feedback_list)
                        print("Feedback {}".format(len(feedback_list)))
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
                        if vendor not in vendors and not vendor.isnull():
                            vendor.feedback = id_feedback
                            for feedback_elem in feedback:
                                feedback_elem.id = id_feedback
                            id_feedback += 1
                        else:
                            index_original_vendor = vendors.index(vendor)
                            original_vendor = vendors[index_original_vendor]
                            if original_vendor.feedback:
                                for feedback_elem in feedback:
                                    feedback_elem.id = original_vendor.feedback
                            else:
                                vendors[index_original_vendor].feedback = id_feedback
                                for feedback_elem in feedback:
                                    feedback_elem.id = id_feedback
                                id_feedback += 1

                        feedback_list += feedback
                        content["#feedback"] = len(feedback_list)
                        print("Feedback {}".format(len(feedback_list)))
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

    # Rates
    if STATISTICAL_INFO:
        successfull_rate = (successfull_pages/len(pages))*100
        failure_rate = (failed_pages / len(pages)) * 100
        content["STATISTICAL INFO"]["successfull_rate"] = str(successfull_rate) + "%"
        content["STATISTICAL INFO"]["failure_rate"] = str(failure_rate) + "%"

    self.update_state(state='PROGRESS', meta=content)

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
    self.update_state(state='PROGRESS', meta=content)

    # Platform DB UPDATE
    delete_platform_db()
    try:
        update_platform_db()
        content["db_platform_updated"] = True
        self.update_state(state=states.SUCCESS, meta=content)
    except:
        traceback.print_exc()
        delete_platform_db()
        content["error"] = "Platform database error"
        self.update_state(state=states.FAILURE, meta=content)

    return content


def update_platform_db():
    pc_product.update_products()
    pc_vendor.update_vendors()
    pc_pseudonym.update_pseudonym()
    pc_feedback.update_feedback()


def delete_platform_db():
    pc_product.delete_products()
    pc_vendor.delete_vendors()
    pc_pseudonym.delete_pseudonym()
    pc_feedback.delete_feedback()
