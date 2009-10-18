
import os.path
import imsvdex.vdex
from zope.schema.vocabulary import SimpleVocabulary
from collective.vdexvocabulary.term import VdexTerm


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
            for term in terms:
                yield dict(
                    key = self.vdex.getTermIdentifier(term),
                    value = self.vdex.getTermCaption(term, lang),
                    description = self.vdex.getTermDescription(term, lang))
        
    def __call__(self, context):
        # resolve language
        try:
            # TODO: need to depend only on zope
            from Products.CMFCore.utils import getToolByName
            lang = getToolByName(context, 'portal_languages').getPreferredLanguage()
        except:
            lang = None

        # build terms list
        terms = []
        for item in self.getTerms(lang):
            terms.append(VdexTerm(
                item['key'],
                item['key'],
                item['value'],
                item['description']))

        # try to do ordering with zope.ucol support
        if not self.vdex.order_significant:
            try:
                import zope.ucol
                collator = zope.ucol.Collator(str(lang))
                terms.sort(key = lambda x: collator.key(x.title))
            except:
                terms.sort(key = lambda x: x.title)

        return SimpleVocabulary(terms)

