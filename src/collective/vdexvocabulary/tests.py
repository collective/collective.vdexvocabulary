# -*- coding: utf-8 -*-
import doctest
import os
import pprint
import re
import six
import unittest


optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS


TESTFILES = [
    "term.rst",
    "treevocabulary.rst",
    "meta.rst",
]


class Py23DocChecker(doctest.OutputChecker):
    def check_output(self, want, got, optionflags):
        if six.PY2:
            got = re.sub("u'(.*?)'", "'\\1'", got)
        return doctest.OutputChecker.check_output(self, want, got, optionflags)


def test_suite():
    return unittest.TestSuite(
        [
            doctest.DocFileSuite(
                filename,
                optionflags=optionflags,
                globs={
                    "pprint": pprint.pprint,
                    "VDEXDIR": os.path.join(os.path.dirname(__file__), "vdex"),
                },
                checker=Py23DocChecker(),
            )
            for filename in TESTFILES
        ]
    )
