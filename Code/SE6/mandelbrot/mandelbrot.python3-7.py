# The Computer Language Benchmarks Game
# http://benchmarksgame.alioth.debian.org/
#
# contributed by Joerg Baumann

from contextlib import closing
from itertools import islice
from multiprocessing.pool import IMapUnorderedIterator
from os import cpu_count
from sys import argv, stdout
from typing import Any, Generator, List, Tuple


def pixels(y: int, n: int, abs : Any) -> Generator[int, None, None]:
    range7: bytearray = bytearray(range(7))
    pixel_bits: bytearray = bytearray(128 >> pos for pos in range(8))
    c1: float = 2. / float(n)
    c0: complex = -1.5 + 1j * y * c1 - 1j
    x: int = 0
    while True:
        pixel: int = 0
        c: complex = x * c1 + c0
        for pixel_bit in pixel_bits:
            z: complex = c
            for _ in range7:
                for _ in range7:
                    z = z * z + c
                if abs(z) >= 2.: break
            else:
                pixel += pixel_bit
            c += c1
        yield pixel
        x += 8

def compute_row(p: 'Tuple[int,int]') -> 'Tuple[int, bytearray]':
    y: int; n: int
    y, n = p

    result : bytearray = bytearray(islice(pixels(y, n, abs), (n + 7) // 8))
    result[-1] &= 0xff << (8 - n % 8)
    return y, result

def ordered_rows(rows: IMapUnorderedIterator, n: int) -> Generator[None, None, None]:
    order: List[None] = [None] * n
    i :int = 0
    j : int = n
    while i < len(order):
        if j > 0:
            row = next(rows)
            order[row[0]] = row
            j -= 1

        if order[i]:
            yield order[i]
            order[i] = None
            i += 1

def compute_rows(n, f):
    row_jobs: 'Generator[Tuple[int,int], None, None]' = ((y, n) for y in range(n))

    if cpu_count() < 2:
        yield from map(f, row_jobs)
    else:
        from multiprocessing import Pool
        with Pool() as pool:
            unordered_rows: Any = pool.imap_unordered(f, row_jobs)
            yield from ordered_rows(unordered_rows, n)

def mandelbrot(n: int) -> None:
    write = stdout.buffer.write

    with closing(compute_rows(n, compute_row)) as rows:
        write("P4\n{0} {0}\n".format(n).encode())
        for row in rows:
            write(row[1])

if __name__ == '__main__':
    mandelbrot(int(argv[1]))