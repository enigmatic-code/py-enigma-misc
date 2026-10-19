#! python3
# -*- mode: Python; py-indent-offset: 2; -*-

from __future__ import print_function

# 64ms

from enigma import (irange, inf, printf)

# throws from a pair of dice
def throws(d1, d2, fn=sorted, op=lambda a, b: a + b):
  return fn(op(a, b) for a in d1 for b in d2)

# generate pairs of <n> sided dice, that can throw the scores <ts>
# n = number of faces on each die
# d1 = numbers (in ascending order) on die 1 (so far)
# d2 = numbers (in ascending order) on die 2 (so far)
# ss = throws that can be made (so far)
# ts = throws that need to be made (all)
# m = max(ts)
# k = minimum difference between adjacent numbers
# invalid = numbers that cannot be used on a die
def solve(n, d1, d2, ss, ts, m, k, invalid):
  (n1, n2) = (len(d1), len(d2))
  # check ordering
  if n1 == n2 and d1 > d2: return
  # are we done?
  if n2 == n:
    if ss.issuperset(ts):
      yield (d1, d2)
  else:
    # check it is possible to make the remaining numbers
    if n * n - n1 * n2 < len(ts) - len(ss): return
    # add a number to the die with the fewest numbers allocated
    for i in irange(d2[-1] + k, inf):
      # will it exceed the maximum?
      if i + d1[-1] > m: break
      # check the number is valid
      if i in invalid: continue
      # the throws this makes with the other die
      s = set(i + j for j in d1)
      if s.issubset(ts):
        for r in solve(n, d2 + [i], d1, ss.union(s), ts, m, k, invalid): yield r

# generate pairs of <n> sided dice, that can throw the scores <ts>
# n = number of faces on each die
# ts = throws that need to be made by throwing the dice
# s = lowest starting number for a die (probably 0 or 1)
# k = minimum difference between adjacent numbers (probably 0 or 1)
# invalid = numbers that cannot be used on a die
def dice(n, ts, s=1, k=1, invalid=set()):
  # the minimal throw
  m = min(ts)
  # choose a number for the first die
  for a in irange(s, m // 2):
    b = m - a
    if a in invalid or b in invalid: continue
    (d1, d2) = ([a], [b])
    for r in solve(n, d1, d2, throws(d1, d2, fn=set), ts, max(ts), k, invalid): yield r


if __name__ == "__main__":

  sicherman = 1
  uniform = 1

  if sicherman:
    # standard dice
    d = (1, 2, 3, 4, 5, 6)
    # throws for a pair of standard dice
    standard = throws(d, d)

    # find equivalent pairs
    for (d1, d2) in dice(6, set(standard), s=1, k=0):
      if throws(d1, d2) == standard:
        printf("1: {d1} x {d2}")
    printf()

  if uniform:

    uniform = [
      1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6,
      7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12, 12,
    ]
    for (d1, d2) in dice(6, set(uniform), s=0, k=0):
      if throws(d1, d2) == uniform:
        printf("2: {d1} x {d2}")
    printf()
