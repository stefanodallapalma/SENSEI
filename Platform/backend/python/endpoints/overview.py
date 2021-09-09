import logging
from db import controller
from flask import Response, json

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
        logger.error(e)
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(biggest_vendors), status=200, mimetype="application/json")


def get_biggest_vendor(country):
    pass


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
        logger.error(e)
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(countries_dct), status=200, mimetype="application/json")


def get_country_raw_data(country):
    pass


def n_sales():
    product_cleanedcontroller = controller.ProductCleanedController()

    try:
        n_products = product_cleanedcontroller.n_products_per_country()
    except Exception as e:
        error_msg = "Internal server error"
        logger.error(e)
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(n_products), status=200, mimetype="application/json")


def n_sales_euro():
    product_cleanedcontroller = controller.ProductCleanedController()

    try:
        n_sales = product_cleanedcontroller.n_sales_per_country()
    except Exception as e:
        error_msg = "Internal server error"
        logger.error(e)
        return Response(json.dumps(error_msg), status=500, mimetype="application/json")

    return Response(json.dumps(n_sales), status=200, mimetype="application/json")
