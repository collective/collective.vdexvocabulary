
from zope.interface import implements
from zope.interface import directlyProvides
from zope.schema.interfaces import ITokenizedTerm
from zope.schema.interfaces import ITitledTokenizedTerm
from zope.schema.vocabulary import getVocabularyRegistry


class VdexTerm(object):
    """Vdex tokenized term used by VdexVocabulary."""

    implements(ITokenizedTerm)


    def __init__(self, value, token=None, title=None, description=None, related=[]):
        self.value = value
        if token is None:
            token = value
        try:
            self.token = str(token)
        except:
            self.token = str(token.encode('utf-8'))
        self.title = title
        if title is not None:
            directlyProvides(self, ITitledTokenizedTerm)
        self.description = description
        self.related = related
        
