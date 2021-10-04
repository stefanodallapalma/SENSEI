import logging
from traceback import format_exc
from db import controller
from flask import Response, json, request
import utils

logger = logging.getLogger("Vendor endpoints")


def n_products():
    market = None

    if "market" in request.args:
        market = request.args.get('market').lower()
        logger.debug(market)

    product_controller = controller.ProductCleanedController()

    try:
        markets = product_controller.n_products_for_each_vendor(market)
    except Exception as e:
        error_msg = "Internal server error"
        logger.error(format_exc())
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(markets, sort_keys=False), status=200, mimetype="application/json")


def get_vendor(vendor_name):
    vendor_controller = controller.VendorAnalysisController()

    try:
        pass
    except Exception as e:
        error_msg = "Internal server error"
        logger.error(format_exc())
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps({}), status=200, mimetype="application/json")


def get_vendor_list():
    vendor_controller = controller.VendorAnalysisController()

    try:
        vendors = vendor_controller.get_distinct_vendor_names()
    except Exception as e:
        error_msg = "Internal server error"
        logger.error(format_exc())
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(vendors), status=200, mimetype="application/json")


def treemap_info(vendor_name):
    product_controller = controller.ProductCleanedController()

    try:
        drugs = product_controller.n_drugs(vendor_name)
    except Exception as e:
        error_msg = "Internal server error"
        logger.error(format_exc())
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(drugs), status=200, mimetype="application/json")