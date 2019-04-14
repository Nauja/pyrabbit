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
            def load_script(target, **kwargs):
                return target

            pysachi.analyze([SCRIPT], load=load_script)
        except Exception as _:
            self.assertFalse(True)
            raise
