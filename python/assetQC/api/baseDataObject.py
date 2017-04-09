"""
Base class for storing arbitrary data.
"""


class BaseDataObject(object):
    def __init__(self):
        super(BaseDataObject, self).__init__()
        self.__data = dict()

    @property
    def data(self):
        return self.__data

    def getClassName(self):
        return self.__class__.__name__

    def getObjectHash(self):
        return hash(self)
