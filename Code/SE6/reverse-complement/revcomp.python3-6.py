# The Computer Language Benchmarks Game
# http://benchmarksgame.alioth.debian.org/
#
# contributed by Joerg Baumann

from sys import stdin, stdout
from os import cpu_count
from typing import Any, Generator

reverse_translation : bytes = bytes.maketrans(
   b'ABCDGHKMNRSTUVWYabcdghkmnrstuvwy',
   b'TVGHCDMKNYSAABWRTVGHCDMKNYSAABWR')

def reverse_complement(header, sequence) -> tuple : 
   t = sequence.translate(reverse_translation, b'\n\r ')
   output : bytearray = bytearray()
   trailing_length : int = len(t) % 60
   if trailing_length: output += b'\n' + t[:trailing_length]
   for i in range(trailing_length, len(t), 60):
      output += b'\n'+ t[i:i+60]
   return header, output[::-1]

def read_sequences(file) -> Generator :
   for line in file:
      if line[0] == ord('>'):
         header = line
         sequence : bytearray = bytearray()
         for line in file:
            if line[0] == ord('>'):
               yield header, sequence
               header = line
               sequence : bytearray = bytearray()
            else:
               sequence += line
         yield header, sequence
         break

def reverse_and_print_task(q, c, v) -> None :
   while True:
      i = q.get()
      if i == None: break
      h, r = reverse_complement(*data[i])
      with c:
         while i != v.value:
            c.wait()
      write(h); write(r); flush()
      with c:
         v.value = i + 1
         c.notify_all()

if __name__=='__main__' :
   write = stdout.buffer.write
   flush = stdout.buffer.flush

   s : Generator = read_sequences(stdin.buffer)
   data : tuple = next(s)
   if cpu_count() == 1 or len(data[1]) < 1000000:
      from itertools import starmap
      def merge(v, g) -> Generator[Any, Any, None]:
         yield v; yield from g
      for h, r in starmap(reverse_complement, merge(data, s)):
         write(h); write(r)
   else:
      from multiprocessing import Process, Queue, Value, Condition
      from ctypes import c_int

      data : tuple = [data] + list(s)
      q, c, v = (Queue(), Condition(), Value(c_int, 0))
      processes : list = [Process(target=reverse_and_print_task, args=(q, c, v))
         for _ in range(min(len(data), cpu_count()))]

      for p in processes: p.start()
      for i in range(len(data)): q.put(i)
      for p in processes: q.put(None)
      for p in processes: p.join()