# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from typing import Set
from collections.abc import MutableSet

from .comparer import IEqualityComparer, ObjectComparer
from ._key import BoxedKey

class HashSet(MutableSet):
    def __init__(self, comparer: IEqualityComparer = None):
        if comparer is None:
            self._comparer = ObjectComparer.instance
        elif not isinstance(comparer, IEqualityComparer):
            raise TypeError('comparer should be IEqualityComparer')
        else:
            self._comparer = comparer

        self._data: Set[BoxedKey] = set()

    def add(self, value):
        return self._data.add(BoxedKey(self._comparer, value))

    def discard(self, value):
        return self._data.discard(BoxedKey(self._comparer, value))

    def __contains__(self, value):
        return BoxedKey(self._comparer, value) in self._data

    def __iter__(self):
        for boxed_key in self._data:
            yield boxed_key.unbox()

    def __len__(self):
        return len(self._data)
