# The Computer Language Benchmarks Game
# http://benchmarksgame.alioth.debian.org/
#
# contributed by Antoine Pitrou
# modified by Dominique Wahli and Daniel Nanz
# modified by Joerg Baumann

import sys
import multiprocessing as mp
from typing import Any, List, Tuple, Generator

def make_tree(d: int) -> '(Tuple | Tuple[None,None])':

    if d > 0:
        d -= 1
        return (make_tree(d), make_tree(d))
    return (None, None)


def check_tree(node: Tuple) -> int:

    (l, r) = node
    if l is None:
        return 1
    else:
        return 1 + check_tree(l) + check_tree(r)


def make_check(itde, make=make_tree, check=check_tree) -> int:

    i : int; d : int
    i, d = itde
    return check(make(d))


def get_argchunks(i: int, d: int, chunksize: int = 5000) -> Generator[List, None, None]:

    assert chunksize % 2 == 0
    chunk: List = []
    k : int
    for k in range(1, i + 1):
        chunk.extend([(k, d)])
        if len(chunk) == chunksize:
            yield chunk
            chunk = []
    if len(chunk) > 0:
        yield chunk


def main(n: int, min_depth: int = 4) -> None:

    max_depth: int = max(min_depth + 2, n)
    stretch_depth: int = max_depth + 1
    if mp.cpu_count() > 1:
        pool = mp.Pool()
        chunkmap : Any = pool.map
    else:
        chunkmap = map

    print('stretch tree of depth {0}\t check: {1}'.format(
          stretch_depth, make_check((0, stretch_depth))))

    long_lived_tree: Tuple = make_tree(max_depth)

    mmd : int = max_depth + min_depth
    d : int
    for d in range(min_depth, stretch_depth, 2):
        i : int = 2 ** (mmd - d)
        cs : int = 0
        argchunk : List
        for argchunk in get_argchunks(i,d):
            cs += sum(chunkmap(make_check, argchunk))
        print('{0}\t trees of depth {1}\t check: {2}'.format(i, d, cs))

    print('long lived tree of depth {0}\t check: {1}'.format(
          max_depth, check_tree(long_lived_tree)))


if __name__ == '__main__':
    main(int(sys.argv[1]))