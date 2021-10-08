import logging
from flask import request, Response, json
from traceback import format_exc

import db.controller as controller

logger = logging.getLogger("Graph endpoints")


def get_markets_data():
    vendor_controller = controller.VendorAnalysisController()

    try:
        markets = vendor_controller.get_vendors_foreach_market()
    except Exception as e:
        error_msg = "Internal server error"
        logger.error(format_exc())
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(markets), status=200, mimetype="application/json")


def get_vendor_info():
    vendor = request.args.get('vendor-name')
    logger.debug(vendor)

    vendor_controller = controller.VendorAnalysisController()

    try:
        vendor_response = {"vendor": vendor, "markets": {}}

        vendor_markets = vendor_controller.n_markets_foreach_vendor()
        if vendor not in vendor_markets:
            error_msg = "Vendor not found"
            logger.info(error_msg)
            return Response(json.dumps(error_msg), status=404, mimetype="application/json")

        vendor_response["n_markets"] = vendor_markets[vendor]

        vendor_markets_products = vendor_controller.n_products_foreach_market_vendor()
        if vendor not in vendor_markets_products:
            vendor_response["markets"] = None
        else:
            markets_products = vendor_markets_products[vendor]
            for market in markets_products:
                vendor_response["markets"][market] = markets_products[market]

    except Exception as e:
        error_msg = "Internal server error"
        logger.error(format_exc())
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(vendor_response), status=200, mimetype="application/json")