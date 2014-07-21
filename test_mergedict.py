from mergedict import MergeDict, ConfigDict

import pytest


class TestMergeDict():
    def test_default_merge_is_like_update(self):
        d1 = MergeDict({'a': 1, 'b': 'one', 'c': [1]})
        d1.merge({'a':2, 'c': [2]})
        assert d1 == {'a': 2, 'b': 'one', 'c': [2]}

    def test_custom_merge(self):
        class SumDict(MergeDict):
            @MergeDict.dispatch(int)
            def merge_int(this, other):
                return this + other

        d1 = SumDict({'a': 1, 'b': 'one', 'c': [1]})
        d1.merge({'a':2, 'c': [2]})
        assert d1 == {'a': 3, 'b': 'one', 'c': [2]}

        # make sure subclass doesnt mess up with MergeDict
        d2 = MergeDict({'a': 1, 'b': 'one', 'c': [1]})
        d2.merge({'a':2, 'c': [2]})
        assert d2 == {'a': 2, 'b': 'one', 'c': [2]}


    def test_hierarchy(self):
        class SumDict(MergeDict):
            @MergeDict.dispatch(int)
            def merge_int(this, other):
                return this + other

        class ConcatDict(SumDict):
            @MergeDict.dispatch(str)
            def merge_str(this, other):
                return this + other

        d1 = ConcatDict({'a': 1, 'b': 'one', 'c': [1]})
        d1.merge({'a':2, 'b': '-two'})
        assert d1 == {'a': 3, 'b': 'one-two', 'c': [1]}


    def test_update_error_two_args(self):
        config = MergeDict({'foo': 'bar'})
        pytest.raises(TypeError, config.merge, {'foo': 'baz'}, {'foo': 'baz2'})

    def test_merge_keyword(self):
        config = MergeDict({'foo': 'bar'})
        config.merge(foo='baz')
        assert config['foo'] == 'baz'



def test_ConfigDict():
    d1 = ConfigDict({
            'a': 1,
            'b': 'one',
            'c': [1],
            'd': {'foo': 'x1', 'bar': 'x2'},
            'e': set((3, 5)),
            })
    d1.merge({
            'a': 2,
            'c': [1, 2],
            'd': {'bar': 'y2', 'baz': 'y3'},
            'e': set((3, 6)),
            'f': 'func',
            })
    assert d1 == {
        'a': 2,
        'b': 'one',
        'c': [1, 1, 2],
        'd': {'foo': 'x1', 'bar': 'y2', 'baz': 'y3'},
        'e': set((3, 5, 6)),
        'f': 'func',
        }

