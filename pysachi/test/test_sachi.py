import unittest
import pysachi

SCRIPT = """
class User:
    def __init__(self, login, password):
        self._login = login
        self._password = password

    @property
    def login(self):
        return self._login

    @property
    def password(self):
        return self._password

class Operation:
    def __init__(self, a, func, b):
        self._a = a
        self._func = func
        self._b = b

    def result():
        return self._func(a, b)
"""


class TestSachi(unittest.TestCase):
    def test_sachi(self):
        try:
            pysachi.run(
                [SCRIPT],
                analyze=lambda target, **kwargs: pysachi.analyze(
                    target, get_source=str, **kwargs
                ),
                checkers=pysachi.get_checkers(),
            )
        except Exception as _:
            self.assertFalse(True)
            raise
