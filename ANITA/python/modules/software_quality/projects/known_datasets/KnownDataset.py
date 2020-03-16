from abc import ABC, abstractmethod
from os.path import join

from utils.FileUtils import load_json

root_path = "../resources/known_datasets/"


class KnownDataset(ABC):
    def __init__(self, name=None):
        self._name = name

    @staticmethod
    def root_path():
        return root_path

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def path(self):
        return join(root_path, self.name)

    @property
    def json_path(self):
        return join(self.path, self.name + ".json")

    @abstractmethod
    def generate_additional_info(self, *args):
        pass

    @abstractmethod
    def merge(self, original_json, additional_json):
        pass

    def get_additional_info(self):
        return load_json(self.json_path)