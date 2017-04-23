"""
Base class for storing arbitrary data.

This should NOT be used directly by API users.
"""


class BaseDataObject(object):
    """
    Base class for almost all 'assetQC' classes - contains helpful functions 
    for sub-classes.
    
    This should NOT be used directly by API users.
    """
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
