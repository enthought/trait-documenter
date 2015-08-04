def is_python_26():
    import sys
    return sys.version_info < (2, 6)


class expected_failure_when(object):

    def __init__(self, condition):
        self.condition = condition

    def __call__(self, function):
        if is_python26():
            import unittest2 as unittest
        else:
            import unittest
        if self.condition:
            return unittest.expectedFailure(function)
        else:
            return function
