# The Computer Language Benchmarks Game
# http://benchmarksgame.alioth.debian.org/

# Contributed by Sebastien Loisel
# Fixed by Isaac Gouy
# Sped up by Josh Goldfoot
# Dirtily sped up by Simon Descarpentries
# Concurrency by Jason Stitt
# 2to3

from multiprocessing import Pool
from math            import sqrt

from sys             import argv
from typing import Any, Generator, List, Tuple

def eval_A (i: Any, j: Any) -> float:
    return 1.0 / ((i + j) * (i + j + 1) / 2 + i + 1)

def eval_A_times_u (u: 'List') -> 'List[float]':
    args: Generator[Tuple[int, List[float]], None, None] = ((i,u) for i in range(len(u)))
    return pool.map(part_A_times_u, args)

def eval_At_times_u (u: 'List') -> 'List[float]':
    args: Generator[Tuple[int, List[float]], None, None] = ((i,u) for i in range(len(u)))
    return pool.map(part_At_times_u, args)

def eval_AtA_times_u (u: 'List') -> 'List[float]':
    return eval_At_times_u (eval_A_times_u (u))

def part_A_times_u(xxx_todo_changeme: 'Tuple[int, List[float]]') -> float:
    (i,u) = xxx_todo_changeme
    partial_sum: float = 0
    j: int; u_j: float
    for j, u_j in enumerate(u):
        partial_sum += eval_A (i, j) * u_j
    return partial_sum

def part_At_times_u(xxx_todo_changeme1: 'Tuple[int, List[float]]') -> float:
    (i,u) = xxx_todo_changeme1
    partial_sum: float = 0
    j: int; u_j: float
    for j, u_j in enumerate(u):
        partial_sum += eval_A (j, i) * float(u_j)
    return partial_sum

def main() -> None:
    n: int = int(argv[1])
    u: List = [1] * n

    dummy: int
    for dummy in range (10):
        v: List[float] = eval_AtA_times_u (u)
        u = eval_AtA_times_u (v)

    vBv : float; vv: float
    vBv = vv = 0

    ue : float; ve : float
    for ue, ve in zip (u, v):
        vBv += ue * ve
        vv  += ve * ve

    print("%0.9f" % (sqrt(vBv/vv)))

if __name__ == '__main__':
    pool = Pool(processes=4)
    main()