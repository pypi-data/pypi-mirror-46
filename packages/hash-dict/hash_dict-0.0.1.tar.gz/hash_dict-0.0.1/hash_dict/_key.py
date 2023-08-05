# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from .comparer import IEqualityComparer

def cache(name: str):
    def decorator(func):
        def wrapper(self):
            try:
                return getattr(self, name)
            except AttributeError:
                setattr(self, name, func(self))
            return getattr(self, name)
        return wrapper
    return decorator

class BoxedKey:
    '''
    wrap a key with given equality comparer.
    '''
    __slots__ = ('_comparer', '_obj', '_hashcode', '_cmpvalue')

    def __init__(self, comparer: IEqualityComparer, obj):
        self._comparer = comparer
        self._obj = obj

    @cache('_hashcode')
    def __hash__(self):
        return self._comparer.get_hash(self.get_cmpvalue())

    def __eq__(self, other):
        return self._comparer.equals(self.get_cmpvalue(), other.get_cmpvalue())

    def unbox(self):
        'get the origin object'
        return self._obj

    @cache('_cmpvalue')
    def get_cmpvalue(self):
        return self._comparer.get_cmpvalue(self._obj)
