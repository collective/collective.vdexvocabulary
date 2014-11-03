What this package do?
=====================

`IMS VDEX`_ is a standard for exchanging vocabularies.
``collective.vdexvocabulary`` bridges between vdex vocabularies and zope
vocabularies (``zope.schema.vocabularies``), so you can easily use it in
systems like Plone/ Zope, Pyramid or any other Zope-Toolkit supporting system.


.. contents::


Whats so special about it?
==========================

``collective.vdexvocabulary`` contains two different types of vocabularies:

1. If you have big vocabularies with a lot of relations, like +10.000
   terms with +30.000 relations, so this would be perfect use case to use
   the ``VdexVocabulary`` type of ``collective.vdexvocabulary``.

2. If you have tree-like vocabularies this is perfect too. ``TreeVocabulary``
   supports nested/ hierachical vocabularies.

Also there is other stuff which not supported by other vocabulary packages
(i.e. for Plone/Zope):

* i18n support. IMS VDEX supports translations within the VDEX-XML-File, both
  vocabulary types are supporting this way of translations.

* proper order also with unicode characters (if zope.ucol is installed,
  vdexvocabulary only). If VDEX is order-sigificant the order given by vdex
  file is taken (supported by both vocabulary types).

* easy registration using zcml

* relations as it specified in IMS VDEX standard (for now only VdexVocabulary)


How do I use it?
================

Configuration
-------------

In your configure.zcml add::

    <configure
        ...
        xmlns:vdex="http://namespaces.zope.org/vdex"
        ...>

      <include package="collective.vdexvocabulary" file="meta.zcml" />
      <include package="collective.vdexvocabulary" />

And to register a vdex vocabulary simply add line bellow pointing to file
containing vdex vocabulary::

    <configure
        ...
        xmlns:vdex="http://namespaces.zope.org/vdex"
        ...>

      <vdex:vocabulary file="path-to/very-interesting.xml" />

or for tree vocabularies::

      <vdex:treevocabulary file="path-to/very-interesting-tree.xml" />

To make registration of vocabularies even easier you can also register
several vocabularies and just point to directory::

    <configure
        ...
        xmlns:vdex="http://namespaces.zope.org/vdex"
        ...>

      <vdex:vocabulary directory="path-to/my-vdex-vocabularies" />

or for tree vocabularies::

      <vdex:treevocabulary directory="path-to/my-vdex-vocabularies" />

vdex files in ``path-to/my-vdex-vocabularies`` directory should have ending
``.vdex`` to be recognized by ``vdex:vocabulary`` ZCML directive.

Sometimes you dont want VDEX-files inside your code tree. Therefore an
environment variable can be given defining the base directory::

      <vdex:vocabulary file="my-vocabulary.vdex: environment="VDEX_BASE_DIR" />

or for tree vocabularies::

      <vdex:treevocabulary file="my-vocabulary.vdex: environment="VDEX_BASE_DIR" />

Before running the code with environment variable relative filenames/directories
one has to set the environmant variable, i.e. do an
``export VDEX_BASE_DIR=/home/joe/vdex/`` in order to make it look for the vdex
at ``/home/joe/vdex/my-vocabulary.vdex``.


Usage in Code
-------------

Vocabularies are named utiltiies in a zope-toolkit manner. The name is taken
from the vdex file, its the ``vocabIdentifier``.

Given a vocabulary with the name ``beeeurope`` (see tree example below) one has
to get the utility using the zope component architecture way::

    >>> from zope.component import getUtility
    >>> from zope.schema.interfaces import IVocabularyFactory
    >>> factory = zope.component.getUtility(IVocabularyFactory, 'beeeurope')

The factory returns on call a vocabulary. It expects a context, which can be
``None`` in our case. If you are in an application server pass here your current
context. In case of flat vocabularies this is used to detect the language, for
tree vocabularies it is ignored, here an more advanced method is used to support
i18n::

    >>> context = None
    >>> vocabulary = factory(context)

Now you can use the vocabulary::

    >>> for term in vocabulary:
    ...     print term.value
    ...     print term.token
    ...     print term.title
    ...     print term.description


How to use tree-vocabularies
----------------------------

Once looked up as shown above traversing the tree is easy. It works as defined
in ``zope.schema.interfaces.ITreeVocabulary``. The ``term`` is also the key for
the sublevel::

    >>> def printlevel(leveldict, ident=0):
    ...     for term in leveldict:
    ...         print indent * '  ' + term.title
    ...         printlevel(leveldict[term], indent+1)

Hint: ``collective.dynatree`` uses this kind of vocabularies and can be used as
an example for own implementations too.


How to access relations (from code)
-----------------------------------

Relations are defined by `ISO2788`_.

To get listing of BMW car models from above VDEX example you have to::

    >>> from zope.schema.vocabulary import getVocabularyRegistry

    >>> vr = getVocabularyRegistry()
    >>> car_manufacturers = vr.get(self.context, 'your.package.car_manufacturers')
    >>> car_models = vr.get(self.context, 'your.package.car_models')

    >>> bmw = car_manufacturers.getTerm('bmw')
    >>> bmw_car_models = bmw.related.get('NT', [])


Example VDEX file
=================

Flat with with relations
------------------------

Example of car manufacturers list (``car_manufacturers.vdex``).::

    <?xml version="1.0" encoding="utf-8"?>
    <vdex xmlns="http://www.imsglobal.org/xsd/imsvdex_v1p0"
          orderSignificant="false" language="en">
        <vocabIdentifier>your.package.car_manufacturers</vocabIdentifier>
        <term>
            <termIdentifier>ford</termIdentifier>
            <caption>
                <langstring language="en">Ford</langstring>
                <langstring language="es">Una miedra de coche</langstring>
            </caption>
        </term>
        <term>
            <termIdentifier>bmw</termIdentifier>
            <caption>
                <langstring language="en">BMW</langstring>
                <langstring language="es">Be-eMe-uWe, mierda</langstring>
            </caption>
        </term>

        <relationship>
            <sourceTerm>bmw</sourceTerm>
            <targetTerm vocabIdentifier="your.package.car_models">very-special-bmw-model</targetTerm>
            <relationshipType source="http://www.imsglobal.org/vocabularies/iso2788_relations.xml">NT</relationshipType>
        </relationship>

        ...

    </vdex>

List of car models (``car_models.vdex``).::

    <?xml version="1.0" encoding="utf-8"?>
    <vdex xmlns="http://www.imsglobal.org/xsd/imsvdex_v1p0"
          orderSignificant="false" language="en">
        <vocabIdentifier>your.package.car_models</vocabIdentifier>

        <term>
            <termIdentifier>very-special-bmw-model</termIdentifier>
            <caption>
                <langstring language="en">Very special BMW model</langstring>
                <langstring language="es">Un modelo de Be-eMe-uWe</langstring>
            </caption>
        </term>

        <relationship>
            <sourceTerm>very-special-bmw-model</sourceTerm>
            <targetTerm vocabIdentifier="your.package.car_manufacturers">bmw</targetTerm>
            <relationshipType source="http://www.imsglobal.org/vocabularies/iso2788_relations.xml">BT</relationshipType>
        </relationship>

    ...

    </vdex>

Hierachical Tree
----------------

example of a tree vocabulary::

    <vdex xmlns="http://www.imsglobal.org/xsd/imsvdex_v1p0" orderSignificant="true">
      <vocabIdentifier>beeeurope</vocabIdentifier>
      <vocabName>
        <langstring language="en">European Honey Bees</langstring>
      </vocabName>
      <term>
        <termIdentifier>nwe</termIdentifier>
        <caption>
          <langstring language="en">North-west of Europe</langstring>
        </caption>
        <term>
          <termIdentifier>nwe.1</termIdentifier>
          <caption>
            <langstring language="en">A. m. iberica</langstring>
          </caption>
        </term>
        <term>
          <termIdentifier>nwe.2</termIdentifier>
          <caption>
            <langstring language="en">A. m. intermissa</langstring>
          </caption>
        </term>
        <term>
          <termIdentifier>nwe.3</termIdentifier>
          <caption>
            <langstring language="en">A. m. lihzeni</langstring>
          </caption>
        </term>
        <term>
          <termIdentifier>nwe.4</termIdentifier>
          <caption>
            <langstring language="en">A. m. mellifera</langstring>
          </caption>
        </term>
        <term>
          <termIdentifier>nwe.5</termIdentifier>
          <caption>
            <langstring language="en">A. m. sahariensis</langstring>
          </caption>
        </term>
      </term>
      <term>
        <termIdentifier>swe</termIdentifier>
        <caption>
          <langstring language="en">South-west of Europe</langstring>
        </caption>
        <term>
          <termIdentifier>swe.1</termIdentifier>
          <caption>
            <langstring language="en">A. m. carnica</langstring>
          </caption>
        </term>
        <term>
       <term>
          <termIdentifier>swe.2</termIdentifier>
          <caption>
            <langstring language="en">A. m. cecropia</langstring>
          </caption>
        </term>
        <term>
          <termIdentifier>swe.3</termIdentifier>
          <caption>
            <langstring language="en">A. m. ligustica</langstring>
          </caption>
        </term>
        <term>
          <termIdentifier>swe.4</termIdentifier>
          <caption>
            <langstring language="en">A. m. macedonica</langstring>
          </caption>
        </term>
        <term>
          <termIdentifier>swe.5</termIdentifier>
          <caption>
            <langstring language="en">A. m. ruttneri</langstring>
          </caption>
        </term>
        <term>
          <termIdentifier>swe.6</termIdentifier>
          <caption>
            <langstring language="en">A. m. sicula</langstring>
          </caption>
        </term>
      </term>
    </vdex>


Where can I complain / help / send rum?
=======================================

:Home + Source: https://github.com/collective/collective.vdexvocabulary
:Report Issues: https://github.com/collective/collective.vdexvocabulary/issues
:Send rum: contact rok@garbas.si for more info


Credit
======

* Rok Garbas, http://garbas.si, <rok@garbas.si>, Author

* Seantis gmbh, http://www.seantis.ch
  Thank you for initial idea with seantis.vdex where got the idea and then
  reimplement and extend it.

* Jens W Klein, http://kleinundpartner.at, <jens@bluedynamics.com>,
  Cleanup, Treevocabulary/ i18n-support


TODO
====

* fetch vocab(s) via url (new directive)

* load vocabs view entry_points

* store vocabs (or changed vocabs in zodb), will probably also need diff and merge option

* write test and get decent test coverage

* write documentation

* make ZCML optional

* make through the web vdex editor (this would probably need sponsoring)

* add relation support to TreeVocabulary


History
=======

0.2dev
------

* A bunch of refactoring in order to add a new vocab type: TreeVocabulary.
  As the name suggests, treevocabulary supports
  ``zope.schema.interfaces.ITreeVocabulary``. It has better i18n-support using
  own i18n-domains for the caption and description of a term.
  [jensens]


0.1.2 (2014-01-07)
------------------

* don't use context to determine current language, but use getSite.
  context may be adapter or other object without acquisition
  (eg. in forms with ignoreContext=True).

* depend on "setuptools", not "distribute"


0.1.1 (2010-10-11)
------------------

* added **History**, **How to access relations (from code)** and **Example
  VDEX file** section to README. [garbas]

* moved code to http://github.com/collective/collective.vdexvocabulary. [garbas]

* BUG(Fixed): when vdex file was loaded it failed if there were not terms. [garbas]


0.1 (2010-06-23)
----------------

* add documentation and clean up code a little bit. [garbas]


0.1a1 (2010-04-29)
------------------

* initial release. [garbas]


.. _`ISO2788`: http://www.imsglobal.org/vocabularies/iso2788_relations.xml
.. _`IMS VDEX`: http://en.wikipedia.org/wiki/IMS_VDEX
