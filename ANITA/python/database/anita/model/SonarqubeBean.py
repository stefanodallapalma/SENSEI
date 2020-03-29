class SonarqubeBean:
    def __init__(self, timestamp=None, project_name=None, page=None, label=None, label_three=None, number_links=None, number_of_words=None,
                 min_words_in_sentence=None, max_words_in_sentence=None, bitcoin=None, deep_web=None):
        self._timestamp = timestamp
        self._project_name = project_name
        self._page = page
        self._label = label
        self._label = label_three
        self._number_links = number_links
        self._number_of_words = number_of_words
        self._min_words_in_sentence = min_words_in_sentence
        self._max_words_in_sentence = max_words_in_sentence
        self._bitcoin = bitcoin
        self._deep_web = deep_web

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = value

    @property
    def project_name(self):
        return self._project_name

    @project_name.setter
    def project_name(self, value):
        self._project_name = value

    @property
    def page(self):
        return self._page

    @page.setter
    def page(self, value):
        self._page = value

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def label_three(self):
        return self._label_three

    @label_three.setter
    def label_three(self, value):
        self._label_three = value

    @property
    def number_links(self):
        return self._number_links

    @number_links.setter
    def number_links(self, value):
        self._number_links = value

    @property
    def number_of_words(self):
        return self._number_of_words

    @number_of_words.setter
    def number_of_words(self, value):
        self._number_of_words = value

    @property
    def min_words_in_sentence(self):
        return self._min_words_in_sentence

    @min_words_in_sentence.setter
    def min_words_in_sentence(self, value):
        self._min_words_in_sentence = value

    @property
    def max_words_in_sentence(self):
        return self._max_words_in_sentence

    @max_words_in_sentence.setter
    def max_words_in_sentence(self, value):
        self._max_words_in_sentence = value

    @property
    def bitcoin(self):
        return self._bitcoin

    @bitcoin.setter
    def bitcoin(self, value):
        self._bitcoin = value

    @property
    def deep_web(self):
        return self._deep_web

    @deep_web.setter
    def deep_web(self, value):
        self._deep_web = value

    @staticmethod
    def __prop__():
        return [key for key in SonarqubeBean.__dict__
                if not key.startswith("_") and "property object at" in str(SonarqubeBean.__dict__[key])]

