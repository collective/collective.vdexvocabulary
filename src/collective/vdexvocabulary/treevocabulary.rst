The TreeVocabulary
------------------

A tree like (or also flat)  vocabulary for zope toolkit.

First the imports::

    >>> from collective.vdexvocabulary.treevocabulary import VdexTreeVocabularyFactory
    >>> import os
    >>> testfile = os.path.join(VDEXDIR, 'treetest.vdex')

Create a vocabulary from a file::

    >>> vdex_vocab_factory = VdexTreeVocabularyFactory(testfile)
    >>> vdex_vocab = vdex_vocab_factory(None)

Some checks, root level::

    >>> len(vdex_vocab._terms)
    2

And all::

    >>> len(vdex_vocab.term_by_value)
    13

    >>> len(vdex_vocab.term_by_token)
    13

    >>> len(vdex_vocab.path_by_value)
    13

Look at some details::

    >>> pprint(vdex_vocab.path_by_value)
    {'nwe': ['nwe'],
     'nwe.1': ['nwe', 'nwe.1'],
     'nwe.2': ['nwe', 'nwe.2'],
     'nwe.3': ['nwe', 'nwe.3'],
     'nwe.4': ['nwe', 'nwe.4'],
     'nwe.5': ['nwe', 'nwe.5'],
     'swe': ['swe'],
     'swe.1': ['swe', 'swe.1'],
     'swe.2': ['swe', 'swe.2'],
     'swe.3': ['swe', 'swe.3'],
     'swe.4': ['swe', 'swe.4'],
     'swe.5': ['swe', 'swe.5'],
     'swe.6': ['swe', 'swe.6']}

    >>> 'nwe.4' in vdex_vocab
    True

check translations::

    >>> from zope.i18n import translate
    >>> translate(vdex_vocab.term_by_value['nwe'].title)
    u'North-west of Europe'

    >>> translate(vdex_vocab.term_by_value['nwe'].title, target_language='en')
    u'North-west of Europe'

    >>> translate(vdex_vocab.term_by_value['nwe'].title, target_language='de')
    u'Nordwesteuropa'

check with negiotation

build mock negotiator::

    >>> from zope.i18n.interfaces import INegotiator
    >>> from zope.interface import implementer
    >>> @implementer(INegotiator)
    ... class MockNegotiator(object):
    ...     def getLanguage(self, langs, context):
    ...         return 'de'
    >>> from zope.component import provideUtility
    >>> provideUtility(MockNegotiator(), INegotiator)

run with mock::


    >>> translate(vdex_vocab.term_by_value['nwe'].title, context={})
    u'Nordwesteuropa'
