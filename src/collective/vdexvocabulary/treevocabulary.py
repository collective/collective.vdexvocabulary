from collective.vdexvocabulary.term import VdexTerm
from zope.schema.vocabulary import TreeVocabulary

import imsvdex.vdex
import os


class VdexTreeVocabulary(TreeVocabulary):

    def __init__(self, filename,
                 default_lang='en',
                 fallback_to_default_language=True,
                 *interfaces):
        super(VdexTreeVocabulary, self).__init__({}, *interfaces)
        if not os.path.isabs(filename):
            raise Exception('Please set absolute path for filename')
        with open(filename) as vdexfile:
            self.vdex = imsvdex.vdex.VDEXManager(
                file=vdexfile,
                lang=default_lang,
                fallback=fallback_to_default_language
            )
        root_vdexdict = self.vdex.getVocabularyDict()
        self._createTermTree(self._terms, root_vdexdict)
        self._populateIndexes(self._terms)

    def _createTermTree(self, subtree, vdexdict):
        """ Helper method that creates a tree-like dict with ITokenizedTerm
        objects as keys from a imsvdex tree.
        """
        for key, item_tuple in vdexdict.items():
            value, vdex_subtree = item_tuple
            term = VdexTerm(key, key, value)
            subtree[term] = VdexTreeVocabulary.terms_factory()
            if vdex_subtree:
                self._createTermTree(subtree[term], vdex_subtree)


class VdexTreeVocabularyFactory(object):

    def __init__(self, filename):
        self.vocabulary = VdexTreeVocabulary(filename)

    @property
    def vdex(self):
        return self.vocabulary.vdex


    def __call__(self, context):
        return self.vocabulary
