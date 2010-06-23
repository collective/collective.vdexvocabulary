.. contents::


What this package do?
---------------------

IMS VDEX is a standard for exchanging vocabularies. collective.vdexvocabulary
create bridge between vdex vocabularies and zope vocabularies, so you can
easily use it in systems like Plone / Zope.


Whats so special about it?
--------------------------

Imagine you have big vocabularies with a lot of relations. I'm talking +10.000 
terms with +30.000 relations. So this would be perfect use case to use
collective.vdexvocabulary. Also there are other stuff which I didn't found in
other vocabulary packages for Plone/Zope: 

 * i18n support (as it is defined in IMS VDEX)
 * proper order also with unicode charecters (if zope.ucol is installed)
 * easy registration using zcml
 * relations as it specified in IMS VDEX standard


How do I use it?
----------------

In your configure.zcml add::

    <configure
        ...
        xmlns:vdex="http://namespaces.zope.org/vdex"
        ...>

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

      <vdex:vocabulary directory="path-to/my-vdex-vocabularies"


Where can I complain / help / send rum?
---------------------------------------

:Source: git://github.com/garbas/collective.vdexvocabulary.git
:Report Issues: http://github.com/garbas/collective.vdexvocabulary/issues
:Home page: http://github.com/garbas/collective.vdexvocabulary
:Send rum: contact rok@garbas.si for more info


Credit
------

 * Rok Garbas, http://garbas.si, <rok@garbas.si>, Author
 * Seantis gmbh, http://www.seantis.ch
    Thank you for initial idea with seantis.vdex where got the idea and then
    reimplement and extend it.



TODO
----

 * write test and get decent test coverage
 * write documentation
 * make ZCML optional
 * make through the web vdex editor (this would probably need sponsoring)

