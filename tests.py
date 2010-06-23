
import manuel.codeblock
import manuel.doctest
import manuel.testing
import unittest



def test_suite():
    m = manuel.doctest.Manuel()
    m += manuel.codeblock.Manuel()
    return manuel.testing.TestSuite(m, 'docs/index.txt',)


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

