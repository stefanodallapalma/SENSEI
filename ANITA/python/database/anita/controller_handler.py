from .controller.SonarqubeController import SonarqubeController
from .controller.ProductController import ProductController
from .controller.VendorController import VendorController
from .controller.FeedbackController import FeedbackController


def get_controller_instance(table_name):
    if table_name.lower() == "sonarqube":
        return SonarqubeController()

    if table_name.lower() == "product":
        return ProductController()

    if table_name.lower() == "vendor":
        return VendorController()

    if table_name.lower() == "feedback":
        return FeedbackController()

    raise Exception("Invalid table name")