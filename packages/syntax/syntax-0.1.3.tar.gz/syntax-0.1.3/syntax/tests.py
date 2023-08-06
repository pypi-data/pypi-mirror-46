## When you import this, tests should run
## extended_tests.py

import unittest

from syntax import it, constructor


class MethodPipeTests(unittest.TestCase):
    def test_1(self):
        assert (3 | it) == 3

    def test_2(self):
        assert (3 | (it + 3)) == 6

    def test_3(self):
        assert (3 | (3 + it)) == 6
                                                                
    def test_4(self):
        assert ("Asdf" | ("34" + it)) == "34Asdf"

    def test_5(self):
        assert ([1, 2, 3] | it.replace(3, 4)) == [1, 2, 4]

    def test_6(self):
        assert (3 | (not it)) == False


class Constructor(unittest.TestCase):
    def test_1(self):
        class X:
            @constructor
            def __init__(a):
                pass

        instance = X(3)
        assert instance.a == 3

unittest.main(module="syntax.tests", exit=False)