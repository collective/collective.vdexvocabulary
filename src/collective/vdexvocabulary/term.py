# coding=utf-8
from zope.interface import directlyProvides
from zope.interface import implementer
from zope.schema.interfaces import ITitledTokenizedTerm
from zope.schema.interfaces import ITokenizedTerm
from zope.schema.vocabulary import getVocabularyRegistry

import six


try:
    from six import ensure_str
except ImportError:

    def ensure_str(s, encoding="utf-8", errors="strict"):
        """Coerce *s* to `str`.
        For Python 2:
        - `unicode` -> encoded to `str`
        - `str` -> `str`
        For Python 3:
        - `str` -> `str`
        - `bytes` -> decoded to `str`
        """
        # Optimization: Fast return for the common case.
        if type(s) is str:
            return s
        if six.PY2 and isinstance(s, six.text_type):
            return s.encode(encoding, errors)
        elif six.PY3 and isinstance(s, six.binary_type):
            return s.decode(encoding, errors)
        elif not isinstance(s, (six.text_type, six.binary_type)):
            raise TypeError("not expecting type '%s'" % type(s))
        return s


@implementer(ITokenizedTerm)
class VdexTerm(object):
    """Vdex tokenized term used by VdexVocabulary."""

    def __init__(self, value, token=None, title=None, description=None, related=[]):
        self.value = value
        if token is None:
            token = value
        try:
            token = ensure_str(token)
        except TypeError:
            # Some non text like object
            token = str(token)
        self.token = token
        self.title = title
        if title is not None:
            directlyProvides(self, ITitledTokenizedTerm)
        self.description = description
        self.related = related

    def __repr__(self):
        rep = "<%s '%s' at %s>" % (
            self.__class__.__name__,
            self.token,
            hex(id(self))[:-1],
        )
        return rep
