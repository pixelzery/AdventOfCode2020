# taken from https://github.com/hltk/advent-of-code-2020-python

import collections
import copy
import functools
import itertools
import math
import more_itertools
import networkx as nx
import operator
import re
import sys

from pprint import pprint

# from typing import *

from itertools import (
    accumulate,
    chain,
    combinations,
    count,
    cycle,
    filterfalse,
    groupby,
    islice,
    permutations,
    product,
    repeat,
    starmap,
    tee,
    zip_longest,
)

from more_itertools import (
    chunked,
    consume,
    first_true,
    flatten,
    grouper,
    ilen,
    ncycles,
    nth,
    pairwise,
    partition,
    powerset,
    quantify,
    repeatfunc,
    roundrobin,
    substrings,
    substrings_indexes,
    take,
    unique_everseen,
    unique_justseen,
    unzip,
    windowed,
)

from collections import (
    Counter,
    defaultdict,
    deque,
)


# Interact with queue using get, put, empty

from queue import (
    PriorityQueue,
    Queue,
)

from functools import (
    partial,
    reduce,
)

from math import (
    ceil,
    floor,
    sqrt,
    prod,
)


sys.setrecursionlimit(100000)


def dotproduct(vec1, vec2):
    return sum(map(operator.mul, vec1, vec2))


def vec_add(vec1, vec2):
    return (a + b for a, b in zip(vec1, vec2))


def vec_sub(vec1, vec2):
    return (a - b for a, b in zip(vec1, vec2))


def gen_grid(*dims, default=None):
    if len(dims) == 1:
        return [default for x in range(dims[0])]
    v = gen_grid(*dims[1:], default=default)
    return [copy.deepcopy(v) for _ in range(dims[0])]


def ints(line, non_negative=False):
    if non_negative:
        reg = r"\d+"
    else:
        reg = r"-?\d+"
    return [int(x) for x in re.findall(reg, line)]


def starfilter(predicate, iterable):
    for t in iterable:
        if predicate(*t):
            yield t

def valid_coords(i, j, n, m):
    return 0 <= i < n and 0 <= j < m


def adjacent_difference(it, f=operator.sub):
    return starmap(lambda x, y: f(y, x), pairwise(it))

try:
    memoize = functools.cache
except AttributeError:
    memoize = functools.lru_cache(maxsize=None)

from collections import Counter

class GridUtils:
    OFFSETS = [
        (-1, 0),
        (-1, 1),
        (0, 1),
        (1, 1),
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, -1)
    ]

    def __init__(self, grid):
        self.grid = grid

    def adjacents(self, row, col):
        for row_off, col_off in self.OFFSETS:
            if row + row_off < 0 or col + col_off < 0:
                continue
            try:
                yield self.grid[row + row_off][col + col_off]
            except IndexError:
                pass

    def ray_iter(self, row, col, row_off, col_off, stop_cond=None):
        while True:
            if row + row_off < 0 or col + col_off < 0:
                break
            try:
                ret = self.grid[row + row_off][col + col_off]
                yield ret
                if stop_cond is not None:
                    if stop_cond(ret):
                        break
            except IndexError:
                break
            row += row_off
            col += col_off

    def ray(self, row, col, row_off, col_off, stop_cond=None, default=None):
        final_val = default
        for val in self.ray_iter(row, col, row_off, col_off, stop_cond):
            final_val = val
        return final_val

    def adjacent_rays_iter(self, row, col, stop_cond=None, default=None):
        generators = []
        for row_off, col_off in self.OFFSETS:
            generators.append(self.ray_iter(row, col, row_off, col_off, stop_cond))

        stopped = 0
        while stopped < len(generators):
            ret = []
            for generator in generators:
                try:
                    ret.append(next(generator))
                except StopIteration:
                    ret.append(default)
            yield ret

    def adjacent_rays_dfs(self, row, col, stop_cond=None):
        for row_off, col_off in self.OFFSETS:
            yield list(self.ray_iter(row, col, row_off, col_off, stop_cond))

    def adjacent_rays(self, row, col, stop_cond=None, default=None):
        for row_off, col_off in self.OFFSETS:
            yield self.ray(row, col, row_off, col_off, stop_cond, default)

def lcm(*denominators):
    # https://stackoverflow.com/a/49816058/5013267
    return reduce(lambda a,b: a*b // math.gcd(a,b), denominators)