from setuptools import setup, find_packages

version = '0.2dev'

setup(
    name='collective.vdexvocabulary',
    version=version,
    description="IMS VDEX Vocabularies as Zope Vocabulary",
    long_description=open("README.rst").read(),
    # Get more strings from
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
       "Framework :: Zope2",
       "Framework :: Zope2",
       "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    keywords='plone vdex zope vocabulary',
    author='Rok Garbas',
    author_email='rok@garbas.si',
    url='http://github.com/collective/collective.vdexvocabulary',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'imsvdex',
        'zope.schema',
        'zope.interface',
        'zope.component',
        'zope.configuration',
        'zope.i18n',
        'zope.i18nmessageid',
    ],
    test_suite="tests.test_suite",
    extras_require={
        'test': [
            'ipdb',
            'interlude',
        ]
    },
)
