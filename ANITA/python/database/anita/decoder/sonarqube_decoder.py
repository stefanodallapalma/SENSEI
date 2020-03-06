import json
from json import JSONEncoder, JSONDecoder
from database.anita.bean.SonarqubeBean import SonarqubeBean


class SonarqubeServerDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        """keys = ["project_name", "timestamp", "metrics"]
        if all(key in dct for key in keys):
            bean = SonarqubeBean()
            for key in dct:
                if key == "project_name":
                    bean.project_name = dct["project_name"]
                elif key == "timestamp":
                    bean.timestamp = dct["timestamp"]
                elif key == "metrics":
                    metrics = dct["metrics"]
                    if "name" in metrics:
                        bean.page = metrics["name"]
                        del[metrics["name"]]

                    for metric_key in metrics:
                        setattr(bean, metric_key, metrics[metric_key])
            return bean
        else:
            return dct"""
        keys = ["project_name", "timestamp", "pages"]
        if all(key in dct for key in keys):
            beans = []

            project_name = dct["project_name"]
            timestamp = dct["timestamp"]
            pages = dct["pages"]

            for page in pages:
                bean = SonarqubeBean(timestamp, project_name)
                if "name" in page:
                    bean.page = page["name"]
                    del [page["name"]]

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
            else:
                setattr(bean, key, dict[key])
        return bean
