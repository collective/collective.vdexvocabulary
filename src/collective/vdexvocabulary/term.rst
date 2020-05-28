# -*- coding: utf-8 -*-

Import Term and initalize::

    >>> from collective.vdexvocabulary.term import VdexTerm

We use some german umlauts here, but repr is needed in a doctest :/

::

    >>> term = VdexTerm('füü')
    >>> term
    <VdexTerm 'füü' at 0x...>

    >>> isinstance(term.value, str)
    True

    >>> isinstance(term.token, str)
    True

    >>> term.title is None
    True

Passing bytes as a token should work, too.

::

    >>> term = VdexTerm('füü', token='füü'.encode("utf-8"))
    >>> term
    <VdexTerm 'füü' at 0x...>

    >>> isinstance(term.token, str)
    True

Now with numbers:::

    >>> term.description is None
    True

    >>> term2 = VdexTerm(1234)

    >>> term2.value
    1234

    >>> term2.token
    '1234'

    >>> term2 = VdexTerm(12.34, title="foo", description="bar")

    >>> term2.value
    12.34

    >>> term2.title
    'foo'

    >>> term2.description
    'bar'

