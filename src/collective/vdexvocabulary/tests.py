
try:
    import unittest2 as unittest
except:
    import unittest

from zope.testing import doctestunit
from zope.component import testing


import collective.vdexvocabulary

class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            ztc.installPackage(collective.vdexvocabulary)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass


def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='collective.vdexvocabulary',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='collective.vdexvocabulary.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
