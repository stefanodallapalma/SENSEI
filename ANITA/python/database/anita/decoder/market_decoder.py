from json import JSONDecoder
from ..model.market_models import *


class ProductScraperDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        keys = Product.__dict__.keys()
        if all(key in dct for key in keys):
            # timestamp = dct["web_page"]["date"]
            # market = dct["web_page"]["market"]
            name = dct["page_data"]["name"]
            vendor = dct["page_data"]["vendor"]
            ships_from = dct["page_data"]["ships_from"]
            ships_to = dct["page_data"]["ships_to"]
            price = dct["page_data"]["price"]
            price_eur = dct["page_data"]["price_eur"]
            info = dct["page_data"]["info"]
            feedback = dct["page_data"]["feedback"]

            return Product(None, None, name, vendor, ships_from, ships_to, price, price_eur, info, feedback)
        else:
            return dct


class VendorScraperDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        keys = Vendor.__dict__.keys()
        if all(key in dct for key in keys):
            # timestamp = dct["web_page"]["date"]
            # market = dct["web_page"]["market"]
            name = dct["page_data"]["name"]
            score = dct["page_data"]["score"]
            score_normalized = dct["page_data"]["score_normalized"]
            registration = dct["page_data"]["registration"]
            registration_deviation = dct["page_data"]["registration_deviation"]
            last_login = dct["page_data"]["last_login"]
            last_login_deviation = dct["page_data"]["last_login_deviation"]
            sales = dct["page_data"]["sales"]
            info = dct["page_data"]["info"]
            feedback = dct["page_data"]["feedback"]

            return Vendor(None, None, name, score, score_normalized, registration, registration_deviation,
                          last_login, last_login_deviation, sales, info, feedback)
        else:
            return dct


class FeedbackScraperDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        keys = ["web_page", "page_data", "irretrievable_pages"]
        if all(key in dct for key in keys):
            feedback_models = []

            type = dct["web_page"]["page_type"].lower()
            timestamp = dct["web_page"]["date"]
            market = dct["web_page"]["market"]
            name = dct["page_data"]["name"]

            feedback_list = dct["page_data"]["feedback"]
            if isinstance(feedback_list, str):
                feedback_list = [feedback_list]

            for feedback in feedback_list:
                feedback_model = Feedback(type, timestamp, market, name, feedback)
                feedback_models.append(feedback_model)

            return feedback_models
        else:
            return dct