from enum import Enum


class DBType(Enum):
    MYSQL = 1
    POSTGRESQL = 2
    MONGODB = 3
    UNDEFINED = 0