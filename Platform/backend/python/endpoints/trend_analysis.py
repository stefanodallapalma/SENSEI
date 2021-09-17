import logging
from traceback import format_exc
from db import controller
from flask import Response, json, request
import utils

logger = logging.getLogger("Trend Analysis endpoints")


def drugs():
    y_category = request.args.get('y').lower()
    year = None
    month = None

    if 'year' in request.args:
        year = request.args.get('year').lower()
        logger.info(year)
        if not utils.valid_year(year):
            error_msg = "Invalid year paramenter. Year format accepted: YYYY"
            logger.error(format_exc())
            return Response(json.dumps(error_msg), status=400, mimetype="application/json")

    if 'month' in request.args and 'year' not in request.args:
        error_msg = "Invalid date parameter. Month can be passed only with a valid year"
        logger.error(format_exc())
        return Response(json.dumps(error_msg), status=400, mimetype="application/json")

    if 'month' in request.args:
        month = request.args.get('month').lower()
        logger.info(month)
        if not utils.valid_month(month):
            error_msg = "Invalid month paramenter. Month format accepted: 1, 01, 'January', 'Jan'"
            logger.error(format_exc())
            return Response(json.dumps(error_msg), status=400, mimetype="application/json")

        try:
            month = utils.convert_letteral_month_to_int(month)
        except:
            error_msg = "Invalid month paramenter."
            logger.error(format_exc())
            return Response(json.dumps(error_msg), status=400, mimetype="application/json")

    product_cleaned_controller = controller.ProductCleanedController()

    try:
        time = {}
        drugs = {}
        if y_category == 'price':
            time, drugs = product_cleaned_controller.price_group_by_drugs(year, month)
    except Exception as e:
        error_msg = "Internal server error"
        logger.error(format_exc())
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps([time, drugs]), status=200, mimetype="application/json")


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