# -*- coding: utf-8 -*-

Import Term and initalize::

    >>> from collective.vdexvocabulary.term import VdexTerm
    >>> import six

We use some german umlauts here, but repr is needed in a doctest :/

::

    >>> term = VdexTerm(u'f\xfc\xfc')
    >>> term
    <VdexTerm 'füü' at 0x...>

    >>> isinstance(term.value, six.text_type)
    True

    >>> isinstance(term.token, str)
    True

    >>> term.title is None
    True

Passing bytes as a token should work, too.

::

    >>> term = VdexTerm(u'f\xfc\xfc', token=b'b\xc3\xbc\xc3\xbc')
    >>> term
    <VdexTerm 'büü' at 0x...>

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
