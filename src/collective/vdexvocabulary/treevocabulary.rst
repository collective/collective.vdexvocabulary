The TreeVocabulary
------------------

A tree like (or also flat)  vocabulary for zope toolkit.

First the imports::

    >>> from collective.vdexvocabulary.treevocabulary import VDexTreeVocabulary    
    >>> import os
    >>> testfile = os.path.join(VDEXDIR, 'treetest.vdex')
    
Create a vocabulary from a file::    
    
    >>> vdex_vocab = VDexTreeVocabulary(testfile)

Some checks, root level::          
    
    >>> len(vdex_vocab._terms)
    2
    
And all::

    >>> len(vdex_vocab.term_by_value)
    13

    >>> len(vdex_vocab.term_by_token)
    13        
    
    >>> len(vdex_vocab.path_by_value)
    13
    
Look at some details::               
    
    >>> pprint(vdex_vocab.path_by_value)
    {'nwe': ['nwe'],
     'nwe.1': ['nwe', 'nwe.1'],
     'nwe.2': ['nwe', 'nwe.2'],
     'nwe.3': ['nwe', 'nwe.3'],
     'nwe.4': ['nwe', 'nwe.4'],
     'nwe.5': ['nwe', 'nwe.5'],
     'swe': ['swe'],
     'swe.1': ['swe', 'swe.1'],
     'swe.2': ['swe', 'swe.2'],
     'swe.3': ['swe', 'swe.3'],
     'swe.4': ['swe', 'swe.4'],
     'swe.5': ['swe', 'swe.5'],
     'swe.6': ['swe', 'swe.6']}
     
    >>> 'nwe.4' in vdex_vocab
    True

    >> interact(locals())    