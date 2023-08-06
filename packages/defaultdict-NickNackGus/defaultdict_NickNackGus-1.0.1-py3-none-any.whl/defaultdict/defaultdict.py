#!/usr/bin/env python3

"""NickNackGus's DefaultDict package.

Usage:
from defaultdict import DefaultDict
"""

import copy

class DefaultDict(dict):
    """A dict-like object with a deep-copied default value."""

    def __init__(self, init={}, default=0):
        """Create a DefaultDict.

        init is the initial dict, and may contain any key/value pairs.
        default is an object to be deep copied when no value is found.
        """
        if isinstance(init, type(self)):
            self.default = init._default
        else:
            self.default = default

        super().__init__(init)

    def __getitem__(self, key):
        """Returns the value for the key, or the default value.

        Accessing a key with no value creates a deep copy of the default value,
        sets the value of the current key to the result, and returns that value.
        """
        result = super().__getitem__(key)
        self[key] = result
        return result

    def __missing__(self, key):
        """Returns a deep copy of the default value."""
        return copy.deepcopy(self.default)

    def __repr__(self):
        """Return repr(self)."""
        return 'DictWithDefault(init={}, default={})'.format(dict.__repr__(self), repr(self.default))
