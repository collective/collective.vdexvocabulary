
import os
import zope.interface
import zope.configuration
import zope.component.zcml

from collective.vdexvocabulary.vocabulary import VdexVocabulary
from collective.vdexvocabulary import MessageFactory as _


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

def VdexVocabularyDirective(_context, file=None, directory=None):

    if file is None and directory is None:
        raise TypeError("Either 'filename' or 'directory' must be given")

    if file:
        vocabulary = VdexVocabulary(file)
        zope.component.zcml.utility(_context,
            provides = zope.schema.interfaces.IVocabularyFactory,
            name = vocabulary.vdex.getVocabIdentifier(),
            component = vocabulary)

    if directory:
        for filename in os.listdir(directory):
            if filename[-5:] == '.vdex':
                vocabulary = VdexVocabulary(os.path.join(directory, filename))
                zope.component.zcml.utility(_context,
                    provides = zope.schema.interfaces.IVocabularyFactory,
                    name = vocabulary.vdex.getVocabIdentifier(),
                    component = vocabulary)
            
