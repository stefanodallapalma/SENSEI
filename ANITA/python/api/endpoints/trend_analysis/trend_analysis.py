# Standard
import datetime
import logging
import traceback

# Third party imports
from flask import request, Response, json

# Local imports
from database.anita.controller.ProductController import ProductController
from database.anita.controller.VendorController import VendorController
from database.anita.controller.FeedbackController import FeedbackController

logger = logging.getLogger("Trend Analysis Endpoints")


# ENDPOINTS
def get_vendors(marketplace):
    logger.debug("Trend-Analysis - Endpoint get_vendors (GET): START")
    vendor_controller = VendorController()

    # Retrieve all markets available in the db
    markets = vendor_controller.retrieve_markets()

    # Preconditions
    if marketplace is None or marketplace.lower() not in markets:
        logger.debug("Trend-Analysis - Endpoint get_vendors (GET): END")
        return Response(json.dumps({"error": "Marketplace not found"}), status=404, mimetype="application/json")

    # Get info from the db
    try:
        vendors = vendor_controller.retrieve_vendors()

        # Get vendors of a specific marketplace
        vendors = {marketplace: vendors[marketplace]}
    except Exception as e:
        logger.error("Internal server error")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        logger.debug("Trend-Analysis - Endpoint get_vendors (GET): END")
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    return Response(json.dumps(vendors, sort_keys=False), status=200, mimetype="application/json")


def get_vendor(marketplace, vendor):
    logger.debug("Trend-Analysis - Endpoint get_vendor (GET): START")
    vendor_controller = VendorController()
    feedback_controller = FeedbackController()

    # Retrieve all markets available in the db
    markets = vendor_controller.retrieve_markets()

    # Preconditions
    if marketplace is None or marketplace.lower() not in markets:
        logger.debug("Trend-Analysis - Endpoint get_vendor (GET): END")
        return Response(json.dumps({"error": "Marketplace not found"}), status=404, mimetype="application/json")

    # Get info from the db
    try:
        vendor_markets = vendor_controller.retrieve_vendor(vendor)
        vendor_market = {marketplace: vendor_markets[marketplace]}

        # Iterate over timestamps
        for timestamp in vendor_market[marketplace]:
            id = vendor_market[marketplace][timestamp]["feedback"]

            if id:
                # Get all feedback with this id
                feedback_list = feedback_controller.get_feedback(id)
                vendor_market[marketplace][timestamp]["feedback"] = feedback_list
            else:
                vendor_market[marketplace][timestamp]["feedback"] = []
    except Exception as e:
        logger.error("Internal server error")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        logger.debug("Trend-Analysis - Endpoint get_vendor (GET): END")
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    return Response(json.dumps(vendor_market), status=200, mimetype="application/json")


def get_products(marketplace):
    logger.debug("Trend-Analysis - Endpoint get_products (GET): START")
    product_controller = ProductController()

    # Retrieve all markets available in the db
    markets = product_controller.retrieve_markets()

    # Preconditions
    if marketplace is None or marketplace.lower() not in markets:
        logger.debug("Trend-Analysis - Endpoint get_products (GET): END")
        return Response(json.dumps({"error": "Marketplace not found"}), status=404, mimetype="application/json")

    # Get info from the db
    try:
        products = product_controller.retrieve_markets_timestamps_products()
        products = {marketplace: products[marketplace]}
    except Exception as e:
        logger.error("Internal server error")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        logger.debug("Trend-Analysis - Endpoint get_products (GET): END")
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    return Response(json.dumps(products), status=200, mimetype="application/json")


def get_product(marketplace):
    logger.debug("Trend-Analysis - Endpoint get_product (GET): START")
    product_controller = ProductController()
    feedback_controller = FeedbackController()

    # Retrieve all markets available in the db
    markets = product_controller.retrieve_markets()

    # Preconditions
    if marketplace is None or marketplace.lower() not in markets:
        logger.debug("Trend-Analysis - Endpoint get_product (GET): END")
        return Response(json.dumps({"error": "Marketplace not found"}), status=404, mimetype="application/json")

    name = request.form["name"]

    try:
        product = product_controller.get_product(marketplace, name)

        # Iterate over timestamps
        for timestamp in product[marketplace]:
            for i in range(len(product[marketplace][timestamp])):
                id = product[marketplace][timestamp][i]["feedback"]

                if id:
                    # Get all feedback with this id
                    feedback_list = feedback_controller.get_feedback(id)
                    product[marketplace][timestamp][i]["feedback"] = feedback_list
                else:
                    product[marketplace][timestamp][i]["feedback"] = []
    except Exception as e:
        logger.error("Internal server error")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        logger.debug("Trend-Analysis - Endpoint get_product (GET): END")
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    return Response(json.dumps(product), status=200, mimetype="application/json")


def get_vendor_products(marketplace, vendor):
    logger.debug("Trend-Analysis - Endpoint get_vendor_products (GET): START")
    product_controller = ProductController()

    # Retrieve all markets available in the db
    markets = product_controller.retrieve_markets()

    # Preconditions
    if marketplace is None or marketplace.lower() not in markets:
        logger.debug("Trend-Analysis - Endpoint get_vendor_products (GET): END")
        return Response(json.dumps({"error": "Marketplace not found"}), status=404, mimetype="application/json")

    try:
        product = product_controller.retrieve_vendor_products(vendor)
        if marketplace in product[vendor]:
            product = product[vendor][marketplace]
        else:
            product = {}
    except Exception as e:
        logger.error("Internal server error")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        logger.debug("Trend-Analysis - Endpoint get_vendor_products (GET): END")
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    return Response(json.dumps(product), status=200, mimetype="application/json")


def get_vendor_product(marketplace, vendor):
    logger.debug("Trend-Analysis - Endpoint get_vendor_product (GET): START")
    product_controller = ProductController()
    feedback_controller = FeedbackController()

    # Retrieve all markets available in the db
    markets = product_controller.retrieve_markets()

    # Preconditions
    if marketplace is None or marketplace.lower() not in markets:
        logger.debug("Trend-Analysis - Endpoint get_vendor_product (GET): END")
        return Response(json.dumps({"error": "Marketplace not found"}), status=404, mimetype="application/json")

    name = request.form["name"]

    try:
        product = product_controller.retrieve_vendor_product(vendor, name)
        if marketplace in product[vendor]:
            product = product[vendor][marketplace]

            for timestamp in product:
                for i in range(len(product[timestamp])):
                    id = product[timestamp][i]["feedback"]

                    if id:
                        feedback_list = feedback_controller.get_feedback(id)
                        product[timestamp][i]["feedback"] = feedback_list
                    else:
                        product[timestamp][i]["feedback"] = []
        else:
            product = {}
    except Exception as e:
        logger.error("Internal server error")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        logger.debug("Trend-Analysis - Endpoint get_vendor_product (GET): END")
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    return Response(json.dumps(product), status=200, mimetype="application/json")


def graph_analysis():
    logger.debug("Trend-Analysis - Endpoint get_vendors (GET): START")
    vendor_controller = VendorController()

    # Get info from the db
    try:
        market_timestamp_vendors = vendor_controller.retrieve_vendors()
    except Exception as e:
        logger.error("Internal server error")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        logger.debug("Trend-Analysis - Endpoint get_vendors (GET): END")
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    vendors_markets = reverse_market_vendors(market_timestamp_vendors)

    return Response(json.dumps(vendors_markets), status=200, mimetype="application/json")


def graph_analysis_vendor(vendor):
    logger.debug("Trend-Analysis - Endpoint get_vendor (GET): START")
    vendor_controller = VendorController()

    # Get info from the db
    try:
        market_timestamp_vendors = vendor_controller.retrieve_vendors()
    except Exception as e:
        logger.error("Internal server error")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        logger.debug("Trend-Analysis - Endpoint get_vendor (GET): END")
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    vendors_markets = reverse_market_vendors(market_timestamp_vendors)

    vendor_markets = {}
    if vendor in vendors_markets:
        vendor_markets[vendor] = vendors_markets[vendor]
    else:
        return Response(json.dumps({"error": "Vendor not found"}), status=404, mimetype="application/json")

    return Response(json.dumps(vendor_markets), status=200, mimetype="application/json")


# Functions
def reverse_market_vendors(markets_timestamps_vendors):
    # Remove the timestamps
    market_vendors = {}
    for market in markets_timestamps_vendors:
        vendors = set()
        for timestamp in markets_timestamps_vendors[market]:
            vendors.update(markets_timestamps_vendors[market][timestamp])
        market_vendors[market] = list(vendors)

    # Invert the association. NEW RELATION: vendor -> market
    vendors_markets = {}
    for market in market_vendors:
        for vendor in market_vendors[market]:
            if vendor not in vendors_markets:
                vendors_markets[vendor] = []

            vendors_markets[vendor].append(market)

    return vendors_markets