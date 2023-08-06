#!/usr/bin/env python


from __future__ import print_function
from builtins import object
class Thing(object):
    __slots__ = 'foo bar'.split()

    def put(self, something, other):
        self.foo = something
        self.bar = other

import functools

t = Thing()


f_put = functools.partial(t.put, 'astring')

f_put('another_str')
print(t)
print(t.foo)
print(t.bar)

# d = {}
# f_put2 = functools.partial(d[], 'astring')
