Introduction
============

so one of packages that should be released at this point, since it missing
documentation, tests and some more documentation. But I have it laying around
for almost half a year now and is been havily used on many projects, so I
decided to release it as alpha. Maybe if there is someone who will kick my 
ass to write to documentation or do it by himself.

Source: http://github.com/garbas/collective.vdexvocabulary


What this package do?
---------------------

IMS VDEX is a standard for exchanging vocabularies. collective.vdexvocabulary
create bridge between vdex vocabularies and zope vocabularies, so you can
easily use it in systems like Plone / Zope.


Whats so special about it?
--------------------------

Imagine you have big vocabularies with a lot of relations. I'm talking 10.000
and more here. So this would be perfect use case to use collective.vdexvocabulary.
Also there are other stuff which I didn't found in other vocabulary packages for
Plone/Zope: 

 * i18n support
 * proper order also with unicode charecters
 * easy registration using zcml


Credits
-------

 * Rok Garbas, http://garbas.si, <rok@garbas.si>, Author
 * Seantis gmbh, http://www.seantis.ch
    Thank you for initial idea with seantis.vdex where got the idea and then
    reimplement and extend it.



TODO
====

 * write test and get decent test coverage
 * write documentation

