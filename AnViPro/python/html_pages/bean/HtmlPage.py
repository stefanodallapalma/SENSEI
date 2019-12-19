class HtmlPage:

    def __init__(self, category, timestamp, marketplace, code, html_page_path):
        self._category = category
        self._timestamp = timestamp
        self._marketplace = marketplace
        self._code = code
        self._html_page_path = html_page_path

    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, value):
        self._category = value
    

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
        self._marketplace = value
    

    @property
    def code(self):
        return self._code
    
    @code.setter
    def code(self, value):
        self._code = value

    
    @property
    def html_page_path(self):
        return self._html_page_path
    
    @html_page_path.setter
    def html_page_path(self, value):
        self._html_page_path = value
    

    def __str__(self):
        str_to_return = "Category: " + self._category + "\n"
        str_to_return += "Timestamp: " + self._timestamp + "\n"
        str_to_return += "Marketplace: " + self._marketplace + "\n"
        str_to_return += "Code: " + self._code + "\n"
        str_to_return += "Path: " + self._html_page_path + "\n"

        return str_to_return