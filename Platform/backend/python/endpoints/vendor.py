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


def treemap_info(vendor_name):
    product_controller = controller.ProductCleanedController()

    try:
        drugs = product_controller.n_drugs(vendor_name)
    except Exception as e:
        error_msg = "Internal server error"
        logger.error(format_exc())
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(drugs), status=200, mimetype="application/json")


def get_vendor_names():
    if "vendor-name" in request.args:
        vendor = request.args.get('vendor-name').lower()
    else:
        vendor = ""

    limit = None
    if "top" in request.args:
        limit = request.args.get('top')
        logger.debug(limit)
        logger.debug(f"TYPE: {type(limit)}")

        try:
            limit = int(limit)
        except:
            error_msg = "Limit must be an integer"
            return Response(json.dumps(error_msg), status=400, mimetype="application/json")

        if limit <= 0:
            error_msg = "Limit must be higher than 0"
            return Response(json.dumps(error_msg), status=400, mimetype="application/json")

    vendor_controller = controller.VendorAnalysisController()

    try:
        vendors = vendor_controller.search_vendors(vendor, limit)
    except Exception as e:
        error_msg = "Internal server error"
        logger.error(format_exc())
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(vendors), status=200, mimetype="application/json")


def get_vendors_general_info():
    if "vendor-name" in request.args:
        vendor = request.args.get('vendor-name').lower()
    else:
        vendor = ""

    vendor_controller = controller.VendorAnalysisController()

    try:
        vendors = vendor_controller.get_general_vendors(vendor)
    except Exception as e:
        error_msg = "Internal server error"
        logger.error(format_exc())
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(vendors), status=200, mimetype="application/json")