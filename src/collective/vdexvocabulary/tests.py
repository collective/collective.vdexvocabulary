from interlude import interact
from Testing import ZopeTestCase as ztc

import doctest
import unittest

optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS


class VDEXTestcase(ztc.ZopeTestCase):
    """Base TestCase for VDEX tests."""


TESTFILES = [
    'term.rst',
    'vocabulary.rst',
    'meta.rst',
]


def test_suite():
    return unittest.TestSuite([
        ztc.ZopeDocFileSuite(
            filename,
            optionflags=optionflags,
            globs={'interact': interact,
                },
            test_class=VDEXTestcase
        ) for filename in TESTFILES])
