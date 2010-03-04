
import os.path
import imsvdex.vdex
import logging
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import getVocabularyRegistry
from collective.vdexvocabulary.term import VdexTerm

logger = logging.getLogger("collective.vdexvocabulary")


class VdexVocabulary(object):
    
    def __init__(self, vdex_filename, default_lang='en', fallback_to_default_language=True):
        
        if not os.path.isabs(vdex_filename):
            raise Exception, 'please set absolute path for filename'
        f = open(vdex_filename)
        try:
            try:
                self.vdex = imsvdex.vdex.VDEXManager(file=f, lang=default_lang, fallback=fallback_to_default_language)
            except imsvdex.vdex.VDEXError, e:
                raise imsvdex.vdex.VDEXError, vdex_filename+': '+str(e)
        finally:
            f.close()
    
    def getTerms(self, lang):
        xpath = self.vdex.vdexTag('term')
        terms = self.vdex.tree._root.findall(xpath)
        if len(terms) != 0:
            out = []
            for term in terms:
                 out.append(dict(
                    key = self.vdex.getTermIdentifier(term),
                    value = self.vdex.getTermCaption(term, lang),
                    description = self.vdex.getTermDescription(term, lang)))
        return out
        
    def getRelations(self, context, lang, items):
        registry = getVocabularyRegistry()
        items = [i['key'] for i in items]
        xpath = self.vdex.vdexTag('relationship')
        rels = self.vdex.tree._root.findall(xpath)

        out = {}
        if len(rels) != 0:
            for rel in rels:
                
                elems = dict((el.tag.split('}')[1],el) for el in rel.getchildren())

                sourceTerm = elems['sourceTerm'].text
                sourceTermVocabName = elems['sourceTerm'].attrib.get('vocabIdentifier', None)
                if sourceTermVocabName is None:
                   if sourceTerm not in items:
                        raise Exception, 'sourceTerm ('+sourceTerm+') not listed in vocabulary ('+self.vdex.getVocabIdentifier()+').'
                else:
                    try:
                        sourceTermVocab = registry.get(context, sourceTermVocabName)
                        if sourceTermVocab.getTermByToken(sourceTerm) is None:
                            raise Exception, 'sourceTerm ('+sourceTerm+') not listed in vocabulary ('+sourceTermVocab.vdex.getVocabIdentifier()+').'
                    except:
                        pass

                targetTerm = elems['targetTerm'].text
                targetTermVocabName = elems['targetTerm'].attrib.get('vocabIdentifier', None)
                if targetTermVocabName is None:
                   if targetTerm not in items:
                        raise Exception, 'targetTerm ('+targetTerm+') not listed in vocabulary ('+self.vdex.getVocabIdentifier()+').'
                else:
                    try:
                        targetTermVocab = registry.get(context, targetTermVocabName)
                        if targetTermVocab.getTermByToken(targetTerm) is None:
                            raise Exception, 'targetTerm ('+targetTerm+') not listed in vocabulary ('+targetTermVocab.vdex.getVocabIdentifier()+').'
                    except:
                        pass

                relationshipType = elems['relationshipType'].text
                relationshipVocabName = elems['relationshipType'].attrib.get('source', None)
                relationshipVocab = registry.get(context, relationshipVocabName)
                if relationshipVocab is None:
                    raise Exception, 'Relationship source ('+relationshipVocabName+') does not exists'
                if relationshipVocab.getTermByToken(relationshipType) is None:
                    raise Exception, 'Relationship type ('+relationshipVocabName+') does not contain ' + \
                                     'relationship type ('+relationshipType+')'
                
                if sourceTerm not in out.keys():
                    out[sourceTerm] = {}
                if relationshipType not in [i for i in out[sourceTerm]]:
                    out[sourceTerm][relationshipType] = []
                
                out[sourceTerm][relationshipType].append(targetTerm)

        return out

    def __call__(self, context):
        # resolve language
        try:
            # TODO: need to depend only on zope
            from Products.CMFCore.utils import getToolByName
            lang = getToolByName(context, 'portal_languages').getPreferredLanguage()
        except:
            lang = None

        # build terms list
        items = self.getTerms(lang)
        relations = self.getRelations(context, lang, items)
        terms = []
        for item in items:
            
            terms.append(VdexTerm(
                item['key'],
                item['key'],
                item['value'],
                item['description'],
                relations.get(item['key'], [])))

        # try to do ordering with zope.ucol support
        if not self.vdex.order_significant:
            try:
                import zope.ucol
                collator = zope.ucol.Collator(str(lang))
                terms.sort(key = lambda x: collator.key(x.title))
            except:
                terms.sort(key = lambda x: x.title)
            
        return SimpleVocabulary(terms)

