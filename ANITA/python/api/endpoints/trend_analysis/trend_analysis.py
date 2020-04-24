# Standard
import datetime
import logging
import traceback

# Third party imports
from flask import request, Response, json

logger = logging.getLogger("Trend Analysis Endpoints")


# Products
def get_products():
    return Response(json.dumps({"msg": "NOT IMPLEMENTED YET"}), status=500, mimetype="application/json")


# Vendors
def get_vendors():
    return Response(json.dumps({"msg": "NOT IMPLEMENTED YET"}), status=500, mimetype="application/json")


def get_vendor(vendor_name):
    return Response(json.dumps({"msg": "NOT IMPLEMENTED YET"}), status=500, mimetype="application/json")


