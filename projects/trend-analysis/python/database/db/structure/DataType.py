class DataType:
    def __init__(self, type, param=None):
        self._type = type
        self._param = param

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def param(self):
        return self._param

    @param.setter
    def param(self, value):
        self._param = value
