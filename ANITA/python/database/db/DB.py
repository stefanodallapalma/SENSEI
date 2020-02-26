from abc import ABC, abstractmethod
from database.utils.DBUtils import get_db_parameters

class DB(ABC):
    def __init__(self, database_type, database_name=None):
        self._parameters = get_db_parameters(database_type)
        self._db_name = database_name

    @property
    def parameters(self):
        return self._parameters

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def search(self, query):
        pass

    @abstractmethod
    def insert(self, query, value):
        pass

    @abstractmethod
    def delete(self, query, value):
        pass

