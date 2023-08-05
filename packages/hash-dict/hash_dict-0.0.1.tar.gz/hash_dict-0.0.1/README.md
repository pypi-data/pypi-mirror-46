# hash-dict

![GitHub](https://img.shields.io/github/license/Cologler/hash-dict-python.svg)
[![Build Status](https://travis-ci.com/Cologler/hash-dict-python.svg?branch=master)](https://travis-ci.com/Cologler/hash-dict-python)
[![PyPI](https://img.shields.io/pypi/v/hash-dict.svg)](https://pypi.org/project/hash-dict/)

Allow python dict use comparer.

Uou can easy to create your own comparers.

## Usage

For example, for str ignore case:

``` py
from hash_dict import HashDict, StringComparers

data = HashDict(StringComparers.IgnoreCaseComparer)
data['a'] = 1
assert list(data) == ['a']
assert data['a'] == 1
assert data['A'] == 1
```

### Unhashable

How about some strange unhashable object?

You can use `AnyComparer` to handle it 👍.
