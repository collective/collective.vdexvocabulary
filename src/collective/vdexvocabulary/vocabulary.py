from collective.vdexvocabulary.term import VdexTerm
from zope.schema.vocabulary import getVocabularyRegistry
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import VocabularyRegistryError

import imsvdex.vdex
import logging
import os.path

logger = logging.getLogger("collective.vdexvocabulary")


class VdexVocabulary(object):
    """Zope Vocabulary Factory implementation for VDEX."""

    def __init__(self, vdex_filename, default_lang='en',
                 fallback_to_default_language=True):
        if not os.path.isabs(vdex_filename):
            raise Exception('please set absolute path for filename')
        with open(vdex_filename) as f:
            try:
                self.vdex = imsvdex.vdex.VDEXManager(
                    file=f,
                    lang=default_lang,
                    fallback=fallback_to_default_language
                )
            except imsvdex.vdex.VDEXError, e:
                raise imsvdex.vdex.VDEXError, vdex_filename + ': ' + str(e)

        self.cache = {}

    @property
    def vocab_identifier(self):
        return self.vdex.getVocabIdentifier()

    def getTerms(self, lang):
        xpath = self.vdex.vdexTag('term')
        terms = self.vdex.tree._root.findall(xpath)
        out = []
        if len(terms) == 0:
            return []
        for term in terms:
            out.append(dict(
                key=self.vdex.getTermIdentifier(term),
                value=self.vdex.getTermCaption(term, lang),
                description=self.vdex.getTermDescription(term, lang)))
        return out

    def getRelations(self, context, lang, items):
        registry = getVocabularyRegistry()
        items = [i['key'] for i in items]
        xpath = self.vdex.vdexTag('relationship')
        rels = self.vdex.tree._root.findall(xpath)

        out = {}
        if len(rels) == 0:
            return out

        for rel in rels:

            elems = {el.tag.split('}')[1]: el for el in rel.getchildren()}

            sourceTerm = elems['sourceTerm'].text
            sourceTermVocabName = elems['sourceTerm'].attrib.get(
                'vocabIdentifier',
                None
            )
            if sourceTermVocabName is None:
                if sourceTerm not in items:
                    raise Exception('sourceTerm (' + sourceTerm +
                                    ') not listed in vocabulary (' +
                                    self.vdex.getVocabIdentifier() + ').')
            else:
                try:
                    sourceTermVocab = registry.get(
                        context,
                        sourceTermVocabName
                    )
                except LookupError:
                    logger.warn(
                        'sourceTerm (' + sourceTerm +
                        ') not listed in vocabulary (' +
                        sourceTermVocabName + ').'
                )
                else:
                    if sourceTermVocab.getTermByToken(sourceTerm) is None:
                        logger.warn(
                            'sourceTerm (' + sourceTerm +
                            ') not listed in vocabulary (' +
                            sourceTermVocab.vdex.getVocabIdentifier() + ').'
                        )

            targetTerm = elems['targetTerm'].text
            targetTermVocabName = elems['targetTerm'].attrib.get(
                'vocabIdentifier',
                None
            )
            if targetTermVocabName is None:
                if targetTerm not in items:
                    raise Exception(
                        'targetTerm (' + targetTerm +
                        ') not listed in vocabulary (' +
                        self.vdex.getVocabIdentifier() + ').'
                    )
            else:
                try:
                    targetTermVocab = registry.get(
                        context,
                        targetTermVocabName
                    )
                except LookupError:
                    logger.warn(
                        'targetTerm (' + targetTerm +
                        ') not listed in vocabulary (' +
                        targetTermVocabName + ').'
                )
                else:
                    if targetTermVocab.getTermByToken(targetTerm) is None:
                        logger.warn(
                            'targetTerm (' + targetTerm +
                            ') not listed in vocabulary (' +
                            targetTermVocab.vdex.getVocabIdentifier() + ').'
                        )

            relationshipType = elems['relationshipType'].text
            relationshipVocabName = elems['relationshipType'].attrib.get(
                'source',
                None
            )
            relationshipVocab = registry.get(context, relationshipVocabName)
            if relationshipVocab is None:
                raise Exception(
                    'Relationship source (' +
                    relationshipVocabName +
                    ') does not exists'
                )
            if relationshipVocab.getTermByToken(relationshipType) is None:
                raise Exception(
                    'Relationship type (' + relationshipVocabName +
                    ') does not contain ' + 'relationship type (' +
                    relationshipType + ')'
                )

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
            # so use conditional imports in head area of this file
            from Products.CMFCore.utils import getToolByName
            from zope.app.component.hooks import getSite
            lang_tool = getToolByName(getSite(), 'portal_languages')
            lang = lang_tool.getPreferredLanguage()
            logger.debug('Got preferred language "%s"' % lang)
        except ImportError:
            lang = None
            logger.debug('Cant get preferred language, use default language.')

        if lang in self.cache:
            return self.cache[lang]

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
                relations.get(item['key'], {})))

        # try to do ordering with zope.ucol support
        if not self.vdex.order_significant:
            try:
                import zope.ucol
                collator = zope.ucol.Collator(str(lang))
                terms.sort(key=lambda x: collator.key(x.title))
            except ImportError:
                terms.sort(key=lambda x: x.title)

        self.cache[lang] = SimpleVocabulary(terms)
        return self.cache[lang]
