# -*- coding: utf-8 -*-
import doctest
import os
import pprint
import unittest


optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS


TESTFILES = [
    "term.rst",
    "treevocabulary.rst",
    "meta.rst",
]


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
            )
            for filename in TESTFILES
        ]
    )
