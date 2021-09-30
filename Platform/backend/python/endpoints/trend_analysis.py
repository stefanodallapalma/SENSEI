import logging
from traceback import format_exc
from db import controller
from flask import Response, json, request
import utils

logger = logging.getLogger("Trend Analysis endpoints")


def drugs():
    country = None
    market = None
    y_category = request.args.get('y').lower()
    year = None
    month = None

    if "country" in request.args:
        country = request.args.get('country').capitalize()
        logger.debug(country)

    if "market" in request.args:
        market = request.args.get('market').lower()
        logger.debug(market)

    if 'month' in request.args and 'year' not in request.args:
        error_msg = "Invalid date parameter. Month can be passed only with a valid year"
        logger.error(format_exc())
        return Response(json.dumps(error_msg), status=400, mimetype="application/json")

    if 'year' in request.args:
        year = request.args.get('year').lower()
        logger.debug(year)
        if not utils.valid_year(year):
            error_msg = "Invalid year paramenter. Year format accepted: YYYY"
            logger.error(format_exc())
            return Response(json.dumps(error_msg), status=400, mimetype="application/json")

    if 'month' in request.args:
        month = request.args.get('month').lower()
        logger.debug(month)
        if not utils.valid_month(month):
            error_msg = "Invalid month paramenter. Month format accepted: 1, 01, 'January', 'Jan'"
            return Response(json.dumps(error_msg), status=400, mimetype="application/json")

        try:
            month = utils.convert_letteral_month_to_int(month)
        except:
            error_msg = "Invalid month paramenter."
            logger.error(format_exc())
            return Response(json.dumps(error_msg), status=400, mimetype="application/json")

    product_cleaned_controller = controller.ProductCleanedController()
    vendor_analysis_controller = controller.VendorAnalysisController()

    try:
        if y_category == 'price':
            time, drugs_ds = product_cleaned_controller.ta_by_price('drug', country=country, market=market, year=year,
                                                                    month=month)
        elif y_category == 'n. products':
            time, drugs_ds = product_cleaned_controller.ta_by_n_products('drug', country=country, market=market,
                                                                         year=year, month=month)
        elif y_category == 'n. vendors':
            time, drugs_ds = vendor_analysis_controller.ta_by_n_vendors('drug', country=country, market=market,
                                                                        year=year, month=month)
        else:
            error_msg = "Invalid y parameter. Valid y params: 'price', 'n. products', 'n. vendors'"
            logger.error(format_exc())
            return Response(json.dumps(error_msg), status=400, mimetype="application/json")
    except Exception as e:
        error_msg = "Internal server error"
        logger.error(format_exc())
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps([time, drugs_ds]), status=200, mimetype="application/json")


def markets():
    country = None
    drug = None
    y_category = request.args.get('y').lower()
    year = None
    month = None

    if "country" in request.args:
        country = request.args.get('country').capitalize()
        logger.debug(country)

    if "drug" in request.args:
        drug = request.args.get('drug').capitalize()
        logger.debug(drug)

    if 'month' in request.args and 'year' not in request.args:
        error_msg = "Invalid date parameter. Month can be passed only with a valid year"
        logger.error(format_exc())
        return Response(json.dumps(error_msg), status=400, mimetype="application/json")

    if 'year' in request.args:
        year = request.args.get('year').lower()
        logger.debug(year)
        if not utils.valid_year(year):
            error_msg = "Invalid year paramenter. Year format accepted: YYYY"
            logger.error(format_exc())
            return Response(json.dumps(error_msg), status=400, mimetype="application/json")

    if 'month' in request.args:
        month = request.args.get('month').lower()
        logger.debug(month)
        if not utils.valid_month(month):
            error_msg = "Invalid month paramenter. Month format accepted: 1, 01, 'January', 'Jan'"
            return Response(json.dumps(error_msg), status=400, mimetype="application/json")

        try:
            month = utils.convert_letteral_month_to_int(month)
        except:
            error_msg = "Invalid month paramenter."
            logger.error(format_exc())
            return Response(json.dumps(error_msg), status=400, mimetype="application/json")

    product_cleaned_controller = controller.ProductCleanedController()
    vendor_analysis_controller = controller.VendorAnalysisController()

    try:
        if y_category == 'price':
            time, markets_ds = product_cleaned_controller.ta_by_price('market', country=country, drug=drug, year=year,
                                                                      month=month)
        elif y_category == 'n. products':
            time, markets_ds = product_cleaned_controller.ta_by_n_products('market', country=country, drug=drug, year=year,
                                                                           month=month)
        elif y_category == 'n. vendors':
            time, markets_ds = vendor_analysis_controller.ta_by_n_vendors('market', country=country, drug=drug, year=year,
                                                                          month=month)
        else:
            error_msg = "Invalid y parameter. Valid y params: 'price', 'n. products', 'n. vendors'"
            logger.error(format_exc())
            return Response(json.dumps(error_msg), status=400, mimetype="application/json")

    except Exception as e:
        error_msg = "Internal server error"
        logger.error(format_exc())
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps([time, markets_ds]), status=200, mimetype="application/json")


def countries():
    market = None
    drug = None
    y_category = request.args.get('y').lower()
    year = None
    month = None

    if "market" in request.args:
        market = request.args.get('market').lower()
        logger.debug(market)

    if "drug" in request.args:
        drug = request.args.get('drug').capitalize()
        logger.debug(market)

    if 'month' in request.args and 'year' not in request.args:
        error_msg = "Invalid date parameter. Month can be passed only with a valid year"
        logger.error(format_exc())
        return Response(json.dumps(error_msg), status=400, mimetype="application/json")

    if 'year' in request.args:
        year = request.args.get('year').lower()
        logger.debug(year)
        if not utils.valid_year(year):
            error_msg = "Invalid year paramenter. Year format accepted: YYYY"
            logger.error(format_exc())
            return Response(json.dumps(error_msg), status=400, mimetype="application/json")

    if 'month' in request.args:
        month = request.args.get('month').lower()
        logger.debug(month)
        if not utils.valid_month(month):
            error_msg = "Invalid month paramenter. Month format accepted: 1, 01, 'January', 'Jan'"
            return Response(json.dumps(error_msg), status=400, mimetype="application/json")

        try:
            month = utils.convert_letteral_month_to_int(month)
        except:
            error_msg = "Invalid month paramenter."
            logger.error(format_exc())
            return Response(json.dumps(error_msg), status=400, mimetype="application/json")

    product_cleaned_controller = controller.ProductCleanedController()
    vendor_analysis_controller = controller.VendorAnalysisController()

    try:
        if y_category == 'price':
            time, countries_ds = product_cleaned_controller.ta_by_price('country', market=market, drug=drug, year=year,
                                                                        month=month)
        elif y_category == 'n. products':
            time, countries_ds = product_cleaned_controller.ta_by_n_products('country', market=market, drug=drug, year=year,
                                                                             month=month)
        elif y_category == 'n. vendors':
            time, countries_ds = vendor_analysis_controller.ta_by_n_vendors('country', market=market, drug=drug, year=year,
                                                                            month=month)
        else:
            error_msg = "Invalid y parameter. Valid y params: 'price', 'n. products', 'n. vendors'"
            logger.error(format_exc())
            return Response(json.dumps(error_msg), status=400, mimetype="application/json")
    except Exception as e:
        error_msg = "Internal server error"
        logger.error(format_exc())
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps([time, countries_ds]), status=200, mimetype="application/json")