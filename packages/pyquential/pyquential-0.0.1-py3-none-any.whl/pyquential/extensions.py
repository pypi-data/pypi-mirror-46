from functools import reduce
from itertools import repeat, islice
from multiprocessing import Pool, cpu_count

import numpy as np
import pandas as pd
from lantern import grid
from functional import seq
from forbiddenfruit import curse


def _seq(self):
    return seq(self)


def _unzip(self):
    return zip(*self)


def _zip(self):
    return zip(self)


def _keys(self):
    return list(self.keys())


def _values(self):
    return list(self.values())


def _map(self, fun):
    return map(fun, self)


def _filter(self, fun):
    return filter(fun, self)


def _len(self):
    return len(self)


def _max(self):
    return max(self)


def _min(self):
    return min(self)


def _sum(self):
    return sum(self)


def _sort(self, desc=False):
    return sorted(self, reverse=desc)


def _flatten(self):
    return reduce(lambda a, b: [*a, *b], list(self))


def _reduce(self, fun):
    return reduce(fun, self)


def _list(self):
    return list(self)


def _pmap(self, fun, args=None):
    pool = Pool(cpu_count())
    return pool.starmap(fun, zip(self, *(repeat(arg) for arg in args))) if args else pool.map(fun, self)


def _grid(self, style='qgrid'):
    return grid(self, style)


def _preduce(self, fun):
    it = self
    pool = Pool(cpu_count())
    for i in range(int(np.ceil(np.log2(len(it))))):
        it = pool.imap(fun, _chunk(it, 2))
    return list(it)[0]


def _psum(self):
    return _preduce(self, _adder)


def _chunk(self, size):
    it = iter(self)
    return iter(lambda: tuple(islice(it, size)), ())


def _adder(x):
    l = list(x)
    return l[0] if len(x) == 1 else l[0] + l[1] if len(l) == 2 else sum(l)


def pyquentialize():
    iterable_types = [list, tuple, np.ndarray, dict, pd.Series, type({}.keys()), type({}.values())]

    for t in iterable_types:
        curse(t, 'seq', _seq)
        curse(t, 'map', _map)
        curse(t, 'filter', _filter)
        curse(t, 'zip', _zip)
        curse(t, 'unzip', _unzip)
        curse(t, 'len', _len)
        curse(t, 'sorted', _sort)
        curse(t, 'reduce', _reduce)
        curse(t, 'chunk', _chunk)

        curse(t, 'pmap', _pmap)
        curse(t, 'preduce', _preduce)
        curse(t, 'psum', _psum)

        if t != np.ndarray:
            curse(t, 'maximum', _max)
            curse(t, 'minimum', _min)
            curse(t, 'sum', _sum)
            curse(t, 'flatten', _flatten)
            curse(t, 'list', _list)

    curse(dict, 'lkeys', _keys)
    curse(dict, 'lvalues', _values)

    pd.DataFrame.grid = _grid
