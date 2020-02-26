from enum import Enum


class Type(Enum):
    VARCHAR = 1
    INT = 2
    DOUBLE = 3
    DATETIME = 4
    BIT = 5
    TIMESTAMP = 6
    UNDEFINED = 0
