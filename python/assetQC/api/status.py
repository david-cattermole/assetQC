"""
Status

- Return an object from a Validator object.
- Defines the Success or Failure of a Validator.
- Holds any messages that the Validator wants to return.
"""


class StatusObject(object):
    def __init__(self, statusObj, msg, trace, validatorObj, fixerObjs):
        self.__statusObj = statusObj
        self.__trace = trace
        self.__msg = msg
        self.__validator = validatorObj
        self.__fixers = fixerObjs
        self.__hashValue = hash(statusObj)
        self.__hashValue += hash(msg)
        self.__hashValue += hash(validatorObj)
        for fixerObj in fixerObjs:
            self.__hashValue += hash(fixerObj)

    def getHash(self):
        return self.__hashValue

    def getStatus(self):
        return self.__statusObj

    def getMessage(self):
        return self.__msg

    def getTraceback(self):
        return self.__trace

    def getValidator(self):
        return self.__validator

    def getFixerList(self):
        return self.__fixers


class Status(Exception):
    """
    Base class for all status exceptions.
    """
    pass


class WarningStatus(Status):
    """
    Does not cause the asset to be invalid.
    Defines that the status may be a problem but will allow it.
    """
    pass


class ErrorStatus(Status):
    """
    Something happened that is bad and we cannot accept the problem.
    """
    pass


class FailureStatus(Status):
    """
    Something happened which is bad, but we can accept it and continue on.
    """
    pass


