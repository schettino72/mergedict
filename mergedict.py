"""mergedict - A Python `dict` with a merge() method."""

# The MIT License

# Copyright (c) 2013 Eduardo Naufel Schettino

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

__version__ = (0, 3, 0)

import sys
import inspect
from functools import singledispatch

class MergeDict(dict):
    """Base class for a dict that implements a merge() method.

    What exactly merge() depends on the subclass...
    """

    def __init__(self, *args, **kwargs):
        super(MergeDict, self).__init__(*args, **kwargs)
        # register singlesingle dispatch methods
        self.merge_value = singledispatch(self.merge_value)

        # python 2 version
        if sys.version_info[0] < 3: # pragma: no cover
            for name, val in inspect.getmembers(self.__class__):
                _type = getattr(val, 'merge_dispatch', None)
                if _type:
                    self.merge_value.register(_type, val.__func__)
            return

        # python 3 version
        for name, val in inspect.getmembers(self.__class__, inspect.isfunction):
            _type = getattr(val, 'merge_dispatch', None)
            if _type:
                self.merge_value.register(_type, val)



    def merge(self, *args, **kwargs):
        """merge other dict into self"""
        class Sentinel: pass

        if args:
            if len(args) > 1:
                msg = "merge() expected at most 1 arguments, got {}."
                raise TypeError(msg.format(len(args)))
            other = args[0]
        else:
            other = kwargs

        for key, other_value in other.items():
            this_value = self.get(key, Sentinel)
            if this_value is Sentinel:
                self[key] = other_value
            else:
                self[key] = self.merge_value(this_value, other_value)


    class dispatch:
        """decorator to mark methods as single dispatch functions."""
        def __init__(self, _type):
            self._type = _type
        def __call__(self, func):
            func.merge_dispatch = self._type
            return func

    @staticmethod
    def merge_value(this, other):
        """default merge operation, just replace the value"""
        return other



class ConfigDict(MergeDict):
    """A MergeDict that on merge() extend/update lists/sets/dicts.

    Other values are over-written as in dict.update()
    """

    @MergeDict.dispatch(list)
    def merge_list(this, other):
        this.extend(other)
        return this

    @MergeDict.dispatch(set)
    def merge_set(this, other):
        this.update(other)
        return this

    @MergeDict.dispatch(dict)
    def merge_dict(this, other):
        this.update(other)
        return this

