"""
Assert statements and return status codes.
"""

from assetQC.api.status import FailureStatus


class BaseTestObject(object):
    def __init__(self):
        super(BaseTestObject, self).__init__()

    def assertEqual(self, first, second, msg=None):
        """
        Asserts that 'first' argument is equal to 'second' argument.

        :param first: First input
        :param second: Second input
        :param msg: The message string raised with the exception.
        :return:
        """
        if first != second:
            v = {'className': self.getClassName(),
                 'result': (str(first) + '!=' + str(second))}
            if not msg:
                msg = 'Assert Equal.'
            msg = '{className}: {msg} {result!r}'.format(msg=msg, **v)
            raise FailureStatus(msg)
        return

    def assertAlmostEqual(self, first, second, precision=5, msg=None):
        """
        Asserts the value at the given 'first' equals 'value'.

        :param first: First input
        :param second: Second input
        :param precision: Number of significant numbers to check to.
        :param msg: The message string raised with the exception.
        :return:
        """
        rFirst = round(first, precision)
        rSecond = round(second, precision)
        if rFirst != rSecond:
            v = {'className': self.getClassName(),
                 'result': (str(rFirst) + ' != ' + str(rSecond))}
            if not msg:
                msg = 'Assert Almost Equal.'
            msg = '{className}: {msg} {result!r}'.format(msg=msg, **v)
            raise FailureStatus(msg)
        return

    def assertNotEqual(self, first, second, msg=None):
        """
        Asserts that 'first' argument are not equal to 'second'.

        :param first: First input
        :param second: Second input
        :param msg: The message string raised with the exception.
        :return:
        """
        if first == second:
            v = {'className': self.getClassName(),
                 'result': (str(first) + ' != ' + str(second))}
            if not msg:
                msg = 'Assert Not Equal.'
            msg = '{className}: {msg} {result!r}'.format(msg=msg, **v)
            raise FailureStatus(msg)
        return

    def assertTrue(self, condition, msg=None):
        """
        Asserts that the 'condition' given equals True.

        :param condition: Condition (or expression) to check.
        :param msg: The message string raised with the exception.
        :return:
        """
        if not condition:
            v = {'className': self.getClassName(),
                 'result': condition}
            if not msg:
                msg = 'Assert True.'
            msg = '{className}: {msg} {result!r}'.format(msg=msg, **v)
            raise FailureStatus(msg)
        return

    def assertFalse(self, condition, msg=None):
        """
        Asserts that the 'condition' given equals False.

        :param condition: Condition (or expression) to check.
        :param msg: The message string raised with the exception.
        :return:
        """
        if condition:
            v = {'className': self.getClassName(),
                 'result': condition}
            if not msg:
                msg = 'Assert True.'
            msg = '{className}: {msg} {result!r}'.format(msg=msg, **v)
            raise FailureStatus(msg)
        return

