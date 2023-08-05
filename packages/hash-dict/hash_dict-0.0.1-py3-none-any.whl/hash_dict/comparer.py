# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
# a comparer like csharp
# ----------

from abc import abstractmethod, ABC

class IEqualityComparer(ABC):
    'the base equality comparer interface'

    def get_cmpvalue(self, obj):
        '''
        get the cmpvalue use for hash and equal compare.
        '''
        return obj

    @abstractmethod
    def get_hash(self, obj):
        '''
        get the hash from object.

        obj is return value of `get_cmpvalue()`
        '''
        raise NotImplementedError

    @abstractmethod
    def equals(self, left, right):
        '''
        compare two values is equals or not.

        `left` and `right` are return value of `get_cmpvalue()`
        '''
        raise NotImplementedError


class ObjectComparer(IEqualityComparer):
    ' default comparer implemention for object '

    instance: IEqualityComparer = None

    def get_hash(self, obj):
        return hash(obj)

    def equals(self, obj1, obj2):
        return obj1 == obj2

ObjectComparer.instance =  ObjectComparer()

class AnyComparer(IEqualityComparer):
    '''
    default comparer implemention for any object,
    whatever the object is hashable or not.
    '''

    instance: IEqualityComparer = None

    def get_hash(self, obj):
        try:
            return hash(obj)
        except:
            pass

        try:
            return hash(type(obj))
        except:
            pass

        return 110 # call police!

    def equals(self, left, right):
        return left == right

AnyComparer.instance = AnyComparer()


class IgnoreCaseStringComparer(IEqualityComparer):
    ' default ignore case comparer implemention for string '

    def get_hash(self, obj: str):
        return hash(obj)

    def equals(self, left, right):
        return left == right

    def get_cmpvalue(self, obj: str):
        return obj.upper()


class StringComparers:
    ' a collection  of comparers for string '

    IgnoreCaseComparer = IgnoreCaseStringComparer()
