
from zope.interface import implements
from zope.interface import directlyProvides
from zope.schema.interfaces import ITokenizedTerm
from zope.schema.interfaces import ITitledTokenizedTerm
from zope.schema.vocabulary import getVocabularyRegistry


class VdexTerm(object):
    """Vdex tokenized term used by VdexVocabulary."""

    implements(ITokenizedTerm)


    def __init__(self, value, token=None, title=None, description=None, relationships=[]):
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
                
        self.related = {}
        
        for r in relationships:
            if not self.related.has_key(r['vocab']):
                self.related[r['vocab']] = []
            self.related[r['vocab']].append(r['target'])
            
        
