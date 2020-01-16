from html_pages.bean.Category import Category
from html_pages.bean.Marketplace import Marketplace

class HtmlPage:

    '''def __init__(self, category, timestamp, marketplace, code, profile_path, term_and_condition_path, pgp_path, feedback_paths):
        self._category = self.category(category)
        self._timestamp = timestamp
        self._marketplace = marketplace
        self._code = code

        # TABS
        self._profile_path = profile_path
        self._term_and_condition_path = term_and_condition_path
        self._pgp_path = pgp_path
        self._feedback_paths = feedback_paths
    '''

    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, value):
        if value.lower() == "products":
            self._category = Category.PRODUCT
        elif value.lower() == "vendors":
            self._category = Category.VENDOR
        else:
            self._category = Category.UNDEFINED

    @property
    def timestamp(self):
        return self._timestamp
    
    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = value
    

    @property
    def marketplace(self):
        return self._marketplace
    
    @marketplace.setter
    def marketplace(self, value):
        if value.lower() == "agartha":
            self._marketplace = Marketplace.AGARTHA
        elif value.lower() == "apollion":
            self._marketplace = Marketplace.APOLLION
        elif value.lower() == "berlusconi":
            self._marketplace = Marketplace.BERLUSCONI
        elif value.lower() == "drugs medicine":
            self._marketplace = Marketplace.DRUGS_MEDICINE
        elif value.lower() == "tochka":
            self._marketplace = Marketplace.TOCHKA
        else:
            self._marketplace = Marketplace.UNDEFINED


    @property
    def code(self):
        return self._code
    
    @code.setter
    def code(self, value):
        self._code = value

    
    @property
    def profile_path(self):
        return self._profile_path
    
    @profile_path.setter
    def profile_path(self, value):
        self._profile_path = value

    @property
    def term_and_condition_path(self):
        return self._term_and_condition_path

    @term_and_condition_path.setter
    def term_and_condition_path(self, value):
        self._term_and_condition_path = value

    @property
    def pgp_path(self):
        return self._pgp_path

    @pgp_path.setter
    def pgp_path(self, value):
        self._pgp_path = value

    @property
    def feedback_paths(self):
        return self._feedback_paths

    @feedback_paths.setter
    def feedback_paths(self, value):
        self._feedback_paths = value


    def __str__(self):
        str_to_return = "Category: " + self._category + "\n"
        str_to_return += "Timestamp: " + self._timestamp + "\n"
        str_to_return += "Marketplace: " + self._marketplace + "\n"
        str_to_return += "Code: " + self._code + "\n"
        str_to_return += "Profile path: " + self._profile_path + "\n"
        str_to_return += "Terms and conditions path: " + self._term_and_condition_path + "\n"

        if self._pgp_path is not None:
            str_to_return += "Pgp path: " + self._pgp_path + "\n"

        if self._feedback_paths is None:
            str_to_return += "Feedback paths: no feedback paths available\n"
        else:
            i = 1
            for path in self._feedback_paths:
                str_to_return += "Feedback path " + str(i) + ": " + path + "\n"
                i += 1

        return str_to_return