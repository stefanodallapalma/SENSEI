from json import JSONDecoder
from ..model.market_models import *


class ProductScraperDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        keys = ["product_name", "vendor", "ships_from", "ships_to", "price", "price_eur", "info", "feedback"]
        if all(key in dct for key in keys):
            name = None
            vendor = None
            ships_from = None
            ships_to = None
            price = None
            price_eur = None
            info = None

            if "product_name" in dct:
                name = dct["product_name"]

            if "vendor" in dct:
                vendor = dct["vendor"]

            if "ships_from" in dct:
                ships_from = dct["ships_from"]

            if "ships_to" in dct:
                ships_to = dct["ships_to"]

            if "price" in dct:
                price = dct["price"]

            if "price_eur" in dct:
                price_eur = dct["price_eur"]

            if "info" in dct:
                info = dct["info"]

            return Product(None, None, name, vendor, ships_from, ships_to, price, price_eur, info, None)
        else:
            return dct


class VendorScraperDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        keys = ["name", "score", "score_normalized", "registration", "registration_deviation", "last_login",
                 "last_login_deviation", "sales", "info", "feedback"]
        if all(key in dct for key in keys):
            name = None
            score = None
            score_normalized = None
            registration = None
            registration_deviation = None
            last_login = None
            last_login_deviation = None
            sales = None
            info = None
            pgp = None

            if "name" in dct:
                name = dct["name"]

            if "score" in dct:
                score = dct["score"]

            if "score_normalized" in dct:
                score_normalized = dct["score_normalized"]

            if "registration" in dct:
                registration = dct["registration"]

            if "registration_deviation" in dct:
                registration_deviation = dct["registration_deviation"]

            if "last_login" in dct:
                last_login = dct["last_login"]

            if "last_login_deviation" in dct:
                last_login_deviation = dct["last_login_deviation"]

            if "sales" in dct:
                sales = dct["sales"]

            if "info" in dct:
                info = dct["info"]

            if "pgp" in dct:
                pgp = dct["pgp"]

            return Vendor(None, None, name, score, score_normalized, registration, registration_deviation,
                          last_login, last_login_deviation, sales, info, None, pgp)
        else:
            return dct


class FeedbackScraperDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        product_keys = ["product_name", "vendor", "ships_from", "ships_to", "price", "price_eur", "info", "feedback"]
        vendor_keys = ["name", "score", "score_normalized", "registration", "registration_deviation", "last_login",
                "last_login_deviation", "sales", "info", "feedback"]

        if all(key in dct for key in product_keys) or all(key in dct for key in vendor_keys):
            feedback_list = []
            feedback_list_json = dct["feedback"]

            product = False
            if all(key in dct for key in product_keys):
                product = True

            for feedback_json in feedback_list_json:
                # A feedback's product does not have the product and the deal parameters
                if product:
                    feedback = Feedback(id=None, score=feedback_json["score"], message=feedback_json["message"],
                                        date=feedback_json["date"], user=feedback_json["user"])
                else:
                    feedback = Feedback(id=None, score=feedback_json["score"], message=feedback_json["message"],
                                        date=feedback_json["date"], product=feedback_json["product"],
                                        user=feedback_json["user"], deals=feedback_json["deals"])
                feedback_list.append(feedback)

            return feedback_list
        else:
            return dct