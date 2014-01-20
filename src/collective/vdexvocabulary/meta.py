from collective.vdexvocabulary import MessageFactory as _
from collective.vdexvocabulary.vocabulary import VdexVocabulary
from collective.vdexvocabulary.treevocabulary import VdexTreeVocabulary

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
        abs_filename = os.path.join(directory, filename)
        abs_filename = os.path.abspath(abs_filename)
        vocabulary = cls(abs_filename)
        zope.component.zcml.utility(_context,
            provides=zope.schema.interfaces.IVocabularyFactory,
            name=vocabulary.vdex.getVocabIdentifier(),
            component=vocabulary)


def base_directive(_context, cls, file=None, directory=None):
    if file is None and directory is None:
        raise TypeError("Either 'filename' xor 'directory' must be given")
    if file:
        registerfile(_context, file, cls)
    else:
        for filename in os.listdir(directory):
            if filename.endswith('.vdex'):
                registerfile(_context, filename, cls)


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
        VdexTreeVocabulary,
        file=file,
        directory=directory
    )
