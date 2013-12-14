mergedict - A Python `dict` with a merge() method
===================================================

A MergeDict is a `dict` with a `merge()` method.
`merge()` is like `dict.update()`...

::

    from mergedict import MergeDict

    d1 = MergeDict({'a': 1, 'b': 'one'})
    d1.merge({'a':2, 'c': [2]})

    assert d1 == {'a': 2, 'c': [2], 'b': 'one'}


A MergeDict can be subclassed to create custom "merge" operations
based on the type of an item value.


::

    from mergedict import MergeDict

    class SumDict(MergeDict):
          @MergeDict.dispatch(int)
          def merge_int(this, other):
              return this + other

    d2 = SumDict({'a': 1, 'b': 'one'})
    d2.merge({'a':2, 'b': 'two'})

    assert d2 == {'a': 3, 'b': 'two'}


`mergedict` module comes with a `ConfigDict` that will
extend/update lists/sets/dicts.

::

    from mergedict import ConfigDict

    d3 = ConfigDict({'a': 1, 'my_list': [1, 2]})
    d3.merge({'a':2, 'my_list': [3, 4]})

    assert d3 == {'a': 2, 'my_list': [1, 2, 3, 4]}




Project Details
===============

- Project management on github - https://github.com/schettino72/mergedict/


license
=======

The MIT License
Copyright (c) 2013 Eduardo Naufel Schettino

see LICENSE file


developers / contributors
==========================

- Eduardo Naufel Schettino


install
=======

::

 $ pip install pyterm

or download and::

 $ python setup.py install


tests
=======

To run the tests::

  $ py.test


CHANGES
==========

0.1.0 *2013-12-15*
-------------------

- initial release
