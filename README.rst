What this package do?
=====================

`IMS VDEX`_ is a standard for exchanging vocabularies. collective.vdexvocabulary
create bridge between vdex vocabularies and zope vocabularies, so you can
easily use it in systems like Plone / Zope.


.. contents::


Whats so special about it?
==========================

Imagine you have big vocabularies with a lot of relations. I'm talking +10.000 
terms with +30.000 relations. So this would be perfect use case to use
collective.vdexvocabulary. Also there are other stuff which I didn't found in
other vocabulary packages for Plone/Zope: 

 * i18n support (as it is defined in IMS VDEX)
 * proper order also with unicode charecters (if zope.ucol is installed)
 * easy registration using zcml
 * relations as it specified in IMS VDEX standard


How do I use it?
================

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

To make registration of vocabularies even easier you can also register 
several vocabularies and just point to directory::

    <configure
        ...
        xmlns:vdex="http://namespaces.zope.org/vdex"
        ...>

      <vdex:vocabulary directory="path-to/my-vdex-vocabularies" />

vdex files in ``path-to/my-vdex-vocabularies`` directory should have ending
``.vdex`` to be recognized by ``vdex:vocabulary`` ZCML directive.


Example VDEX file
=================

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

How to access relations (from code)
===================================

Relations are defined by `ISO2788`_.

To get listing of BMW car models from above VDEX example you have to::

    from zope.schema.vocabulary import getVocabularyRegistry

    vr = getVocabularyRegistry()
    car_manufacturers = vr.get(self.context, 'your.package.car_manufacturers')
    car_models = vr.get(self.context, 'your.package.car_models')

    bmw = car_manufacturers.getTerm('bmw')
    bmw_car_models = bmw.related.get('NT', [])


Where can I complain / help / send rum?
=======================================

:Source: git://github.com/garbas/collective.vdexvocabulary.git
:Report Issues: http://github.com/collective/collective.vdexvocabulary/issues
:Home page: http://github.com/collective/collective.vdexvocabulary
:Send rum: contact rok@garbas.si for more info


Credit
======

 * Rok Garbas, http://garbas.si, <rok@garbas.si>, Author
 * Seantis gmbh, http://www.seantis.ch
    Thank you for initial idea with seantis.vdex where got the idea and then
    reimplement and extend it.


TODO
====

 * fetch vocab(s) via url (new directive)
 * load vocabs view entry_points
 * store vocabs (or changed vocabs in zodb), will probably also need diff and merge option
 * write test and get decent test coverage
 * write documentation
 * make ZCML optional
 * make through the web vdex editor (this would probably need sponsoring)


History
=======

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
