import logging
from traceback import format_exc
from db import controller
from flask import Response, json, request

logger = logging.getLogger("Trend Analysis endpoints")


def drugs():
    y_category = request.args.get('y')
    year = None
    month = None

    if 'year' in request.args:
        year = request.args.get('year')

    if 'month' in request.args:
        month = request.args.get('month')

    product_cleaned_controller = controller.ProductCleanedController()

    try:
        drugs = {}
        if y_category == 'price':
            drugs = product_cleaned_controller.price_group_by_drugs(year, month)
    except Exception as e:
        error_msg = "Internal server error"
        logger.error(format_exc())
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(drugs), status=200, mimetype="application/json")


def markets():
    x_time = request.args.get('x')
    y_category = request.args.get('y')

    try:
        pass
    except Exception as e:
        error_msg = "Internal server error"
        logger.error(format_exc())
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(True), status=200, mimetype="application/json")


def countries():
    x_time = request.args.get('x')
    y_category = request.args.get('y')

    try:
        pass
    except Exception as e:
        error_msg = "Internal server error"
        logger.error(format_exc())
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(True), status=200, mimetype="application/json")