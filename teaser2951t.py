#! python3
# -*- mode: Python; python-indent-offset: 2; coding: utf-8 -*-

import random
from enigma import (number, irange, subsets, diff, ordered, fraction, fdiv, arg, printf)

# prisms that project over another prism when placed side by side
overhangs = {
  3: [],
  4: [],
  5: [3, 6, 7, 9, 10],
  6: [3, 7],
  7: [3],
  8: [3],
  9: [3, 6, 7, 10],
  10: [3, 7],
}

# over(x, y) = "x goes over y"
over = lambda x, y: y in overhangs[x]

# possible prisms
prisms = sorted(overhangs.keys())

# record special choices
special = set()

# choose the central prism
for x in prisms:
  # and choose a left and right prism that are overhung by x
  for (l, r) in subsets(overhangs[x], size=2):
    # check there is a rearrangement that traps the new centre prism
    if over(l, r) or over(r, l):
      special.add(ordered(x, l, r))

printf("{n} special sets", n=len(special))


# record the total number of choices, and the number of that give two special sets
t = n = 0

# choose the first set of 3 prisms
for s1 in subsets(prisms, size=3):
  # is it a special set?
  p1 = (ordered(*s1) in special)

  # choose the second set of 3 prisms
  for s2 in subsets(diff(prisms, s1), size=3):
    # is it a special set?
    p2 = (ordered(*s2) in special)
    if p1 and p2: n += 1
    t += 1

# output the solution
(a, b) = fraction(n, t)
printf("chance = {n} / {t} = {a} / {b}")


# run some random trials

N = number(arg("1_000_000", 0))

n = 0
for _ in irange(1, N):

  # choose six prisms at random
  s = random.sample(prisms, 6)

  # check if the first three and second three are "special"
  if ordered(*s[:3]) in special and ordered(*s[3:]) in special:
    n += 1

printf("{n} of {N} trials = {f:.3%} [expected = {x:.3%}]", f=fdiv(n, N), x=fdiv(a, b))
