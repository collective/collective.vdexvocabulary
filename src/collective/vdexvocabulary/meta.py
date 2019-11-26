from collective.vdexvocabulary import MessageFactory as _
from collective.vdexvocabulary.treevocabulary import VdexTreeVocabularyFactory
from collective.vdexvocabulary.vocabulary import VdexVocabulary

import logging
import os
import zope.component.zcml
import zope.configuration
import zope.interface
import zope.schema


logger = logging.getLogger("collective.vdexvocabulary")


class IVdexVocabulary(zope.interface.Interface):
    """Directive which registers a new vdex vocabulary."""

    file = zope.configuration.fields.Path(
        title=_(u"Vocabulary file"), description=_(u""), required=False
    )

    directory = zope.configuration.fields.Path(
        title=_(u"Vocabularies directory"), description=_(u""), required=False
    )

    environment = zope.configuration.fields.Path(
        title=_(u"Environment variable containing absolute base path"),
        description=_(u""),
        required=False,
    )

    default_language = zope.schema.TextLine(
        title=_(u"Default language"), description=_(u""), required=False
    )


def registerfile(_context, filename, cls, default_language=None):
    filename = os.path.abspath(filename)
    if default_language:
        vocabulary_factory = cls(filename, default_lang=default_language)
    else:
        vocabulary_factory = cls(filename)
    logger.debug("loading vocabulary at {0} as {1}".format(filename, cls))
    zope.component.zcml.utility(
        _context,
        provides=zope.schema.interfaces.IVocabularyFactory,
        name=vocabulary_factory.vocab_identifier,
        component=vocabulary_factory,
    )


def base_directive(
    _context,
    cls,
    filename=None,
    directory=None,
    environment=None,
    default_language=None,
):
    if filename is None and directory is None:
        raise TypeError("Either 'filename' xor 'directory' must be given")
    if environment:
        base_dir = os.environ.get(environment, None)
        if base_dir:
            if filename:
                filename = os.path.join(base_dir, filename)
            else:
                directory = os.path.join(base_dir, directory)
    if filename:
        registerfile(_context, filename, cls)
    else:
        for filename in os.listdir(directory):
            if filename.endswith(".vdex"):
                registerfile(
                    _context,
                    os.path.join(directory, filename),
                    cls,
                    default_language=default_language,
                )


def VdexVocabularyDirective(
    _context, file=None, directory=None, environment=None, default_language=None,
):
    """ZCML directive to provide flat vdex vocabularies."""
    base_directive(
        _context,
        VdexVocabulary,  # this is in fact the factory
        filename=file,
        directory=directory,
        environment=environment,
        default_language=default_language,
    )


def VdexTreeVocabularyDirective(
    _context, file=None, directory=None, environment=None, default_language=None,
):
    """ZCML directive to provide tree like vocabularies."""
    base_directive(
        _context,
        VdexTreeVocabularyFactory,
        filename=file,
        directory=directory,
        default_language=default_language,
    )
