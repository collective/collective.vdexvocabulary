from collective.vdexvocabulary.term import VdexTerm
from zope.component import provideUtility
from zope.i18n.interfaces import INegotiator
from zope.i18n.interfaces import ITranslationDomain
from zope.i18nmessageid import MessageFactory
from zope.interface import implementer
from zope.schema.vocabulary import TreeVocabulary

import imsvdex.vdex
import os


@implementer(ITranslationDomain)
class VdexTranslationDomain(object):

    def __init__(self, vdex):
        self.vdex = vdex

    @property
    def domain(self):
        return 'collective.vdexvocabulary.%s' % self.vdex.getVocabIdentifier()

    def translate(self, msgid, mapping=None, context=None,
                  target_language=None, default=None):
        # msgid is always kind|termidentifer
        # i.e.: caption|prod.1 or description|prod.45
        kind, msgid = msgid.split('|')

        # handle default
        if default is None:
            default = unicode(msgid)

        # get vdex term for msgid
        vdexterm = self.vdex.getTermById(msgid)
        if vdexterm is None:
            return default

        # fetch translations from vdex
        if kind == 'caption':
            tag = self.vdex.vdexTag('caption')
        elif kind == 'description':
            tag = self.vdex.vdexTag('description')
        else:
            raise ValueError("kind '%' part of i18n-messageid '%s|%s' "
                             "is not valid" % (kind, kind, msgid))
        xpath = '%s/%s' % (tag, self.vdex.vdexTag('langstring'))
        translations = self.vdex.getAllLangstrings(vdexterm.findall(xpath))

        # find out what the target language should be
        if target_language is None and context is not None:
            langs = translations.keys()
            negotiator = getUtility(INegotiator)
            target_language = negotiator.getLanguage(langs, context)

        # fetch matching translation or default
        return translations.get(target_language, default).decode('utf-8')


class VdexTreeVocabulary(TreeVocabulary):
    """A tree vocabulary
    """

    def __init__(self, filename, *interfaces):
        super(VdexTreeVocabulary, self).__init__({}, *interfaces)

        # read vdex file
        if not os.path.isabs(filename):
            raise Exception('Please set absolute path for filename')
        with open(filename) as vdexfile:
            self.vdex = imsvdex.vdex.VDEXManager(vdexfile)

        # create and register translation domain per vocabulary
        translationdomain = VdexTranslationDomain(self.vdex)
        provideUtility(
            translationdomain,
            ITranslationDomain,
            translationdomain.domain
        )
        message_factory = MessageFactory(translationdomain.domain)

        # build TreeVocabulary with children
        rootelement = self.vdex.tree._root
        self._createTermTree(rootelement, self._terms, message_factory)
        self._populateIndexes(self._terms)


    def _createTermTree(self, element, terms, _):
        """ Helper method that creates a tree-like dict with ITokenizedTerm
        objects as keys from a imsvdex tree.
        """
        term_elements = element.findall(self.vdex.vdexTag('term'))
        for term_element in term_elements:
            identifier = self.vdex.getTermIdentifier(term_element)
            term = VdexTerm(
                identifier,  # value
                identifier,  # token
                # i18n message id for title
                _('caption|%s' % identifier,
                  default=identifier.decode('utf-8')),
                # i18n message id for description
                _('description|%s' % identifier, default=u""),
                # todo: add related
                []
            )
            terms[term] = VdexTreeVocabulary.terms_factory()
            self._createTermTree(term_element, terms[term], _)


class VdexTreeVocabularyFactory(object):

    def __init__(self, filename):
        self.filename = filename
        self.default_language = default_language
        self.vocabulary = VdexTreeVocabulary(filename)

    def vocab_identifier(self):
        return self.vocabulary.vdex.getVocabIdentifier()

    def __call__(self, context):
        return self.vocabulary
