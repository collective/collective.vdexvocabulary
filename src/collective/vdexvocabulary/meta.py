from collective.vdexvocabulary import MessageFactory as _
from collective.vdexvocabulary.vocabulary import VdexVocabulary
from collective.vdexvocabulary.treevocabulary import VdexTreeVocabularyFactory

import os
import zope.interface
import zope.component.zcml
import zope.configuration
import zope.schema


class IVdexVocabulary(zope.interface.Interface):
    """Directive which registers a new vdex vocabulary."""

    file = zope.configuration.fields.Path(
        title=_(u"Vocabulary file"),
        description=_(u""),
        required=False
        )

    directory = zope.configuration.fields.Path(
        title=_(u"Vocabularies directory"),
        description=_(u""),
        required=False
        )

def registerfile(_context, filename, cls):
        vocabulary_factory = cls(os.path.abspath(filename))
        zope.component.zcml.utility(_context,
            provides=zope.schema.interfaces.IVocabularyFactory,
            name=vocabulary_factory.vocab_identifer,
            component=vocabulary_factory)


def base_directive(_context, cls, file=None, directory=None):
    if file is None and directory is None:
        raise TypeError("Either 'filename' xor 'directory' must be given")
    if file:
        registerfile(_context, file, cls)
    else:
        for filename in os.listdir(directory):
            if filename.endswith('.vdex'):
                registerfile(_context, os.path.join(directory, filename), cls)


def VdexVocabularyDirective(_context, file=None, directory=None):
    """ZCML directive to provide flat vdex vocabularies."""
    base_directive(_context,
        VdexVocabulary,
        file=file,
        directory=directory
    )


def VdexTreeVocabularyDirective(_context, file=None, directory=None):
    """ZCML directive to provide tree like vocabularies."""
    base_directive(_context,
        VdexTreeVocabularyFactory,
        file=file,
        directory=directory
    )
