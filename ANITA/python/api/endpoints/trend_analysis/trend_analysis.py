# Standard
import datetime
import logging
import traceback

# Third party imports
from flask import request, Response, json

# Local imports
from database.anita.controller.ProductController import ProductController
from database.anita.controller.VendorController import VendorController

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
        vendors = vendors[marketplace]
    except Exception as e:
        logger.error("Internal server error")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        logger.debug("Trend-Analysis - Endpoint get_vendors (GET): END")
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    return Response(json.dumps(vendors), status=200, mimetype="application/json")


def get_vendor(marketplace, vendor):
    logger.debug("Trend-Analysis - Endpoint get_vendor (GET): START")
    vendor_controller = VendorController()

    # Retrieve all markets available in the db
    markets = vendor_controller.retrieve_markets()

    # Preconditions
    if marketplace is None or marketplace.lower() not in markets:
        logger.debug("Trend-Analysis - Endpoint get_vendor (GET): END")
        return Response(json.dumps({"error": "Marketplace not found"}), status=404, mimetype="application/json")

    # Get info from the db
    try:
        vendor = vendor_controller.retrieve_vendor(vendor)
        vendor = vendor[marketplace]
    except Exception as e:
        logger.error("Internal server error")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        logger.debug("Trend-Analysis - Endpoint get_vendor (GET): END")
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    return Response(json.dumps(vendor), status=200, mimetype="application/json")


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
        products = products[marketplace]
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

    # Retrieve all markets available in the db
    markets = product_controller.retrieve_markets()

    # Preconditions
    if marketplace is None or marketplace.lower() not in markets:
        logger.debug("Trend-Analysis - Endpoint get_product (GET): END")
        return Response(json.dumps({"error": "Marketplace not found"}), status=404, mimetype="application/json")

    name = request.form["name"]

    try:
        product = product_controller.get_product(marketplace, name)
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
        vendors = vendor_controller.retrieve_vendors()
    except Exception as e:
        logger.error("Internal server error")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        logger.debug("Trend-Analysis - Endpoint get_vendors (GET): END")
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    return Response(json.dumps(vendors), status=200, mimetype="application/json")


def graph_analysis_vendor(vendor):
    logger.debug("Trend-Analysis - Endpoint get_vendor (GET): START")
    vendor_controller = VendorController()

    # Get info from the db
    try:
        vendor = vendor_controller.retrieve_vendor(vendor)
    except Exception as e:
        logger.error("Internal server error")
        logger.error(str(e))
        logger.error(traceback.format_exc())
        logger.debug("Trend-Analysis - Endpoint get_vendor (GET): END")
        error_content = {"error": "Internal server error", "msg": str(e), "traceback": traceback.format_exc()}
        return Response(json.dumps(error_content), status=500, mimetype="application/json")

    return Response(json.dumps(vendor), status=200, mimetype="application/json")
