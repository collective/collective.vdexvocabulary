Changelog
=========

0.2.2 (2015-09-01)
------------------

- Newer lxml doesn't allow accessing ``_root`` anymore.
  This switches to ``getroot()``.
  [pilz]


0.2.1 (2015-06-22)
------------------

- Plone 4.3 compatibility
  [ale-rt]

- lxml compatibility (imsvdex dropped elementtree in favour of lxml)
  [ale-rt]

- entry point for z3c.autoinclude
  [ale-rt]


0.2 (2014-11-03)
----------------

- A bunch of refactoring in order to add a new vocab type: TreeVocabulary.
  As the name suggests, treevocabulary supports
  ``zope.schema.interfaces.ITreeVocabulary``. It has better i18n-support using
  own i18n-domains for the caption and description of a term.
  [jensens]


0.1.2 (2014-01-07)
------------------

- don't use context to determine current language, but use getSite.
  context may be adapter or other object without acquisition
  (eg. in forms with ignoreContext=True).
  [naro]

- depend on "setuptools", not "distribute"
  [nutjob]


0.1.1 (2010-10-11)
------------------

- added **History**, **How to access relations (from code)** and **Example
  VDEX file** section to README.
  [garbas]

- moved code to http://github.com/collective/collective.vdexvocabulary.
  [garbas]

- BUG(Fixed): when vdex file was loaded it failed if there were not terms.
  [garbas]


0.1 (2010-06-23)
----------------

- add documentation and clean up code a little bit.
  [garbas]


0.1a1 (2010-04-29)
------------------

- initial release.
  [garbas]

