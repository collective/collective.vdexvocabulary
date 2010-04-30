from setuptools import setup, find_packages
import os

version = '0.1a1'

setup(name='collective.vdexvocabulary',
      version=version,
      description="ims vdex vocabularies as zope vocabulary",
      long_description=open("README.txt").read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone vdex zope vocabulary',
      author='Rok Garbas',
      author_email='rok@garbas.si',
      url='http://github.com/garbas/collective.vdexvocabulary',
      license='GPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'':'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'imsvdex',
          'zope.interface',
          'zope.component',
          'zope.schema',
          'zope.i18nmessageid',
      ],
      )
