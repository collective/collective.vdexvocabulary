
from zope.interface import implements
from zope.interface import directlyProvides
from zope.schema.interfaces import ITokenizedTerm
from zope.schema.interfaces import ITitledTokenizedTerm


class VdexTerm(object):
    """Vdex tokenized term used by VdexVocabulary."""

    implements(ITokenizedTerm)

    def __init__(self, value, token=None, title=None, description=None):
        self.value = value
        if token is None:
            token = value
        self.token = str(token)
        self.title = title
        if title is not None:
            directlyProvides(self, ITitledTokenizedTerm)
        self.description = description

