import doctest
import os

import grandfatherson

from test_filters import *


class Main(unittest.main):
    """Loads doctests with the rest of the TestSuite"""
    doctests = [grandfatherson]

    def parseArgs(self, *args, **kwargs):
        unittest.main.parseArgs(self, *args, **kwargs)
        if not getattr(self, 'testNames', None):
            self.createDocTests(None)

    def createTests(self):
        doctests = set(d.__name__ for d in self.doctests)

        # Filter out doctests to avoid confusing super'
        if self.testNames:
            testnames = set(self.testNames)
            self.testNames = list(testnames - doctests)
        else:
            testnames = set()

        unittest.main.createTests(self)

        self.createDocTests(testnames & doctests)

    def createDocTests(self, testnames):
        optionflags = (doctest.ELLIPSIS |
                       doctest.NORMALIZE_WHITESPACE)
        # Add doctests back in
        for mod in self.doctests:
            if testnames is None or mod.__name__ in testnames:
                self.test.addTest(
                    doctest.DocTestSuite(mod, optionflags=optionflags)
                )
