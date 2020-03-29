import json
from json import JSONEncoder, JSONDecoder
from database.anita.model.SonarqubeBean import SonarqubeBean


class SonarqubeServerDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        keys = ["project_name", "timestamp", "pages"]
        if all(key in dct for key in keys):
            beans = []

            project_name = dct["project_name"]
            timestamp = dct["timestamp"]
            pages = dct["pages"]

            for page in pages:
                bean = SonarqubeBean(timestamp, project_name)
                if "Name" in page:
                    bean.page = page["Name"]
                    del [page["Name"]]

                for metric in page:
                    setattr(bean, metric, page[metric])

                beans.append(bean)

            return beans
        else:
            return dct


class SonarqubeDBDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        bean = SonarqubeBean()
        for key in dct:
            if key == "project_name":
                bean.project_name = dct["project_name"]
            elif key == "timestamp":
                bean.timestamp = dct["timestamp"]
            elif key == "page":
                bean.page = dct["page"]
            elif key == "label":
                bean.label = dct["label"]
            elif key == "label_three":
                bean.label_three = dct["label_three"]
            elif key == "number_links":
                bean.number_links = dct["number_links"]
            elif key == "number_of_words":
                bean.number_of_words = dct["number_of_words"]
            elif key == "min_words_in_sentence":
                bean.min_words_in_sentence = dct["min_words_in_sentence"]
            elif key == "max_words_in_sentence":
                bean.max_words_in_sentence = dct["max_words_in_sentence"]
            elif key == "bitcoin":
                bean.bitcoin = dct["bitcoin"]
            elif key == "deep_web":
                bean.deep_web = dct["deep_web"]
            else:
                setattr(bean, key, dct[key])
        return bean


class SonarqubeAdditionalInfoDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        bean = SonarqubeBean()
        bean.timestamp = dct["timestamp"]
        bean.project_name = dct["project_name"]
        bean.page = dct["page"]
        bean.number_links = dct["number_links"]
        bean.number_of_words = dct["number_of_words"]
        bean.min_words_in_sentence = dct["min_words_in_sentence"]
        bean.max_words_in_sentence = dct["max_words_in_sentence"]
        bean.bitcoin = dct["bitcoin"]
        bean.deep_web = dct["deep_web"]

        return bean