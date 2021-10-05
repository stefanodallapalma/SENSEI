import logging
import operator
from traceback import format_exc
from db import controller
from flask import Response, json, request
from utils import month_year_date_format

logger = logging.getLogger("Overview endpoints")


def get_countries():
    vendor_analysis_controller = controller.VendorAnalysisController()

    try:
        countries = vendor_analysis_controller.get_distinct_ships_from()
    except Exception as e:
        error_msg = "Internal server error"
        logger.error(e)
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(countries), status=200, mimetype="application/json")


def get_biggest_vendors():
    vendor_analysis_controller = controller.VendorAnalysisController()
    product_cleanedcontroller = controller.ProductCleanedController()

    try:
        # Retrieve the list of all countries
        countries = vendor_analysis_controller.get_distinct_ships_from()

        biggest_vendors = {}
        for country in countries:
            biggest_vendor = product_cleanedcontroller.best_vendor(country)
            if not biggest_vendor:
                biggest_vendors[country] = "NA"
            else:
                biggest_vendors[country] = biggest_vendor

        # Add the best vendor, considering all the countries
        best_vendor = product_cleanedcontroller.best_vendor()
        biggest_vendors["All"] = "NA"
        if best_vendor:
            biggest_vendors["All"] = best_vendor

    except Exception as e:
        error_msg = "Internal server error"
        logger.error(format_exc())
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(biggest_vendors), status=200, mimetype="application/json")


def get_countries_raw_data():
    vendor_analysis_controller = controller.VendorAnalysisController()
    product_cleanedcontroller = controller.ProductCleanedController()
    review_controller = controller.ReviewController()

    try:
        # Country list - Init default dictionary
        countries = vendor_analysis_controller.get_distinct_ships_from()
        countries_dct = {}
        for country in countries:
            countries_dct[country] = {}

        for country in countries:
            countries_dct[country]["n_vendors"] = "NA"
            countries_dct[country]["n_products"] = "NA"
            countries_dct[country]["n_reviews"] = "NA"

        # Retrieve n_vendors
        n_vendors = vendor_analysis_controller.n_vendors_per_country()
        for country, n in n_vendors.items():
            countries_dct[country]["n_vendors"] = n

        # Retrieve n_products
        n_products = product_cleanedcontroller.n_products_per_country()
        for country, n in n_products.items():
            countries_dct[country]["n_products"] = n

        # Retrieve n_reviews
        n_reviews = review_controller.n_reviews_per_country()
        for country, n in n_reviews.items():
            countries_dct[country]["n_reviews"] = n

    except Exception as e:
        error_msg = "Internal server error"
        logger.error(format_exc())
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(countries_dct), status=200, mimetype="application/json")


def get_country_raw_data(country):
    pass


def n_sales():
    product_cleanedcontroller = controller.ProductCleanedController()
    country_controller = controller.CountryController()

    try:
        n_products = product_cleanedcontroller.n_products_per_country()
        countries = country_controller.get_countries_alpha2code()

        logger.debug(countries)

        n_products_alpha2code = []
        for country in n_products:
            if country not in countries:
                try:
                    alpha2code = country_controller.add_country(country)
                except Exception as e:
                    logger.info(f"Invalid country `{country}`: SKIPPED")
            else:
                alpha2code = countries[country]
                
            n_products_alpha2code.append({"country": country, "n. products": n_products[country],
                                          "alpha2code": alpha2code})

        if "top" in request.args:
            n_elements = request.args.get('top')
            n_products_alpha2code = {k: n_products_alpha2code[k] for k in list(n_products_alpha2code)[:int(n_elements)]}
    except Exception as e:
        error_msg = "Internal server error"
        logger.error(format_exc())
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(n_products_alpha2code, sort_keys=False), status=200, mimetype="application/json")


def top_sales():
    # Default value
    top_sales = 4

    if "top" in request.args:
        top_sales = int(request.args.get('top'))

    product_cleanedcontroller = controller.ProductCleanedController()

    try:
        n_products = product_cleanedcontroller.n_products_per_country()
        n_products = {k: n_products[k] for k in list(n_products)[:int(top_sales)]}

        tot_product = product_cleanedcontroller.n_products()

        top_sales_list = []
        for key, value in n_products.items():
            sale = {"country": key, "n_products": value, "percentage": round((value/tot_product)*100, 2)}
            top_sales_list.append(sale)
    except Exception as e:
        error_msg = "Internal server error"
        logger.error(format_exc())
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(top_sales_list), status=200, mimetype="application/json")


def top_vendors():
    # Default value
    n_vendors = 7

    if "n-vendors" in request.args:
        n_vendors = int(request.args.get('n-vendors'))

    product_cleaned_controller = controller.ProductCleanedController()

    try:
        top_vendors = product_cleaned_controller.get_top_vendors(limit=n_vendors)
        latest_timestamp = product_cleaned_controller.last_timestamp()
        sum_prices = int(product_cleaned_controller.sum_price())
        date = month_year_date_format(latest_timestamp)

        json_response = {"date": date, "price": sum_prices, "top_vendors": top_vendors}
    except Exception as e:
        error_msg = "Internal server error"
        logger.error(format_exc())
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(json_response), status=200, mimetype="application/json")


def n_sales_euro():
    product_cleanedcontroller = controller.ProductCleanedController()

    try:
        n_sales = product_cleanedcontroller.n_sales_per_country()
    except Exception as e:
        error_msg = "Internal server error"
        logger.error(e)
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(n_sales), status=200, mimetype="application/json")


def get_insights():
    vendor_analysis_controller = controller.VendorAnalysisController()
    product_cleanedcontroller = controller.ProductCleanedController()
    review_controller = controller.ReviewController()

    try:
        # N. markets
        tot_markets = len(controller.get_markets())

        # N. vendors
        tot_vendors = vendor_analysis_controller.n_vendors()

        # N. products
        tot_products = product_cleanedcontroller.n_products()

        # N. reviews
        tot_reviews = review_controller.n_review()
    except Exception as e:
        error_msg = "Internal server error"
        logger.error(e)
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    insight_json = {"n_markets": tot_markets, "n_vendors": tot_vendors, "n_products": tot_products,
                    "n_reviews": tot_reviews}

    return Response(json.dumps(insight_json), status=200, mimetype="application/json")


def latest_month_sales():
    product_cleaned_controller = controller.ProductCleanedController()

    try:
        latest_month_sales = product_cleaned_controller.latest_monthly_sales()
    except Exception as e:
        error_msg = "Internal server error"
        logger.error(format_exc())
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(latest_month_sales), status=200, mimetype="application/json")
