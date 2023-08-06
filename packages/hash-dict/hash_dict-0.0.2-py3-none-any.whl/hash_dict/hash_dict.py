# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from typing import Dict
from collections import defaultdict
from collections.abc import MutableMapping

from .comparer import IEqualityComparer, ObjectComparer
from ._key import BoxedKey

class HashDict(MutableMapping):
    '''
    a dict use give comparer.
    if comparer is `None`, use default `ObjectComparer()`
    '''

    def __init__(self, comparer: IEqualityComparer = None):
        if comparer is None:
            self._comparer = ObjectComparer.instance
        elif not isinstance(comparer, IEqualityComparer):
            raise TypeError('comparer should be IEqualityComparer')
        else:
            self._comparer = comparer

        self._data: Dict[BoxedKey, object] = {}

    def __getitem__(self, key):
        return self._data[BoxedKey(self._comparer, key)]

    def __setitem__(self, key, value):
        self._data[BoxedKey(self._comparer, key)] = value

    def __delitem__(self, key):
        del self._data[BoxedKey(self._comparer, key)]

    def __iter__(self):
        for boxed_key in self._data:
            yield boxed_key.unbox()

    def __len__(self):
        return len(self._data)

    def setdefault(self, key, value):
        '''
        Insert key with a value of default if key is not in the dictionary.

        Return the value for key if key is in the dictionary, else default.
        '''
        # overwrite to ensure this is atomic
        return self._data.setdefault(BoxedKey(self._comparer, key), value)

    def copy(self):
        'Make a shallow copy'
        new_one = HashDict(self._comparer)
        new_one.update(self)
        return new_one

    @staticmethod
    def fromkeys(iterable, value=None, *, comparer: IEqualityComparer = None):
        'Create a new dictionary with keys from iterable and values set to value.'
        new_one = HashDict(comparer)
        for item in iterable:
            new_one[item] = value
        return new_one
