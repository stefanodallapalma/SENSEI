import json

# Third party imports
from celery import states

# Local application imports
from celery_task.celery_app import celery
from utils.FileUtils import getfiles
from modules.trend_analysis.scraper.market.handler import get_scraper_instance
from database.anita.decoder.market_decoder import *
from database.anita.controller.ProductController import ProductController
from database.anita.controller.VendorController import VendorController
from database.anita.controller.FeedbackController import FeedbackController

# Task ID
LOAD_DUMP_TASK_ID = "UPLOAD_DUMP"
REVERSE_LOAD_PAGE_TASK_ID = "UNDO_UPLOAD_DUMP"


@celery.task(bind=True)
def load_dump(self, dump_folder_path, market, timestamp):
    # Get files
    pages = getfiles(dump_folder_path, abs_path=True, ext_filter="html", recursive=True)

    content = {"file_analyzed": 0, "total_files": len(pages), "db_insert": False}
    self.update_state(state=states.STARTED, meta=content)

    # Get market scraper
    scraper = get_scraper_instance(market.lower())

    products = []
    vendors = []
    feedback_list = []

    i = 0
    for page in pages:
        # Extract info from an html page
        try:
            data = scraper.extract_data(page, timestamp, market)
        except:
            # TO FINISH
            content["error"] = ""

        # Convert the information extracted into db models
        if data["web_page"]["page_type"].lower() == "product":
            product = json.loads(data, cls=ProductScraperDecoder)
            products.append(product)
        else:
            vendor = json.loads(data, cls=VendorScraperDecoder)
            vendors.append(vendor)

        feedback = json.loads(data, cls=FeedbackScraperDecoder)
        feedback_list += feedback

        i += 1
        content["file_analyzed"] = i
        self.update_state(state='PROGRESS', meta=content)

    product_controller = ProductController()
    vendor_controller = VendorController()
    feedback_controller = FeedbackController()

    # Preconditions
    if not product_controller.exist():
        product_controller.create()

    if not vendor_controller.exist():
        vendor_controller.create()

    if not feedback_controller.exist():
        feedback_controller.create()

    product_controller.insert_beans(products)
    vendor_controller.insert_beans(vendors)
    feedback_controller.insert_beans()

    content["db_insert"] = True
    self.update_state(state=states.SUCCESS, meta=content)

    return content