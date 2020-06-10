# coding=utf-8
from zope.interface import directlyProvides
from zope.interface import implementer
from zope.schema.interfaces import ITitledTokenizedTerm
from zope.schema.interfaces import ITokenizedTerm
from zope.schema.vocabulary import getVocabularyRegistry
import six

try:
    from Products.CMFPlone.utils import safe_nativestring
except ImportError:
    if six.PY2:
        from Products.CMFPlone.utils import safe_encode as safe_nativestring
    else:
        from Products.CMFPlone.utils import safe_unicode as safe_nativestring


@implementer(ITokenizedTerm)
class VdexTerm(object):
    """Vdex tokenized term used by VdexVocabulary."""

    def __init__(self, value, token=None, title=None, description=None, related=[]):
        self.value = value
        if token is None:
            token = value
        token = safe_nativestring(token)
        if not isinstance(token, str):
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
