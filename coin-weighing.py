#! python3
# -*- mode: Python; python-indent-offset: 2; coding: utf-8 -*-

from __future__ import print_function

# this program can output the decision tree for 4 kinds of coin
# weighing puzzle, where we have a collection of <n> coins, one of
# which is counterfeit and is either lighter or heavier than the
# remaining coins (which all weigh the same), and we must determine by
# comparative weighings which of the coins is counterfeit, and whether
# it is heavier or lighter.
#
# type 1 = find the suspect coin from a collection of <n> coins.
#
# type 2 = find the suspect coin from a collection of <n> coins, where
# an additional known good reference coin is provided.
#
# type 3 = find the suspect coin from a collection of <n> coins, where
# some of the coins are red, and some of the coins are black. there is
# either 1 or 2 more red coins than black coins. if the suspect coin
# is red it is heavy, and if it is black it is light.
#
# type 4 = find the suspect lighter coin from a collection of <n> coins.
#
# additionally we can also solve the following problem:
#
# type 1* = find the suspect coin from a collection of <n> coins, but
# we don't need to know if it is heavier or lighter.
#
# this is solved by putting one of the coins aside and treating the
# remaining <n-1> coins as a "type 1" problem. if all weighings
# balance (and we reach the "impossible" leaf of the decision tree),
# then all the coins are good, apart from the one set aside, so it
# must be counterfeit. and so this problem is the same as solving a
# "type 1" problem with <n-1> coins.
#
# the program is run as:
#
#  % python3 coin-weighing.py <n> <p>
#
# where <n> is the number of coins/weighings, and <p> is the problem number (1-4)
#
# if the <n> parameter is given as "w<k>" then the maximum number of
# coins for <k> weighings is used to construct the decision tree.
#
# similarly the <n> parameter can be specified as "n<n>" for the number of coins

from enigma import (irange, divc, arg, nl, printf)

IMP = "(impossible)"

# divide a list into thirds
# such that the first two thirds are equal size
def thirds(ss):
  (i, r) = divmod(len(ss), 3)
  if r == 2: i += 1
  j = 2*i
  return (ss[:i], ss[i:j], ss[j:])

def output_weighing(p, w, A, B):
  printf("{p}[{w}] weighing {w}:")
  printf("{p}[{w}] A = {A}", A=sorted(A))
  printf("{p}[{w}] B = {B}", B=sorted(B))

# find the light suspect coin
def solve_lighter(coins, w=0, p=''):
  n = len(coins)
  if n < 1:
    printf("{p}-> {IMP}")
  elif n == 1:
    printf("{p}[{w}] -> {coins[0]}L")
  elif n == 2 or n == 3:
    w += 1
    (A, B) = ([coins[0]], [coins[1]])
    output_weighing(p, w, A, B)
    printf("{p}[{w}] A < B -> {A[0]}L")
    printf("{p}[{w}] A > B -> {B[0]}L")
    printf("{p}[{w}] A = B -> \\")
    printf("{IMP}" if n == 2 else "{coins[2]}L")
  else:
    # divide the coins into three piles
    (A, B, C) = thirds(coins)
    w += 1
    output_weighing(p, w, A, B)
    printf("{p}[{w}] A < B:")
    w1 = solve_lighter(A, w, p + "  ")
    printf("{p}[{w}] A > B:")
    w2 = solve_lighter(B, w, p + "  ")
    printf("{p}[{w}] A = B:")
    w3 = solve_lighter(C, w, p + "  ")
    w = max(w1, w2, w3)
  return w

# find suspect coin in reds (if heavier), or in blacks (if lighter)
def solve_red_black(reds, blacks, red='H', black='L', good=-1, w=0, p=''):
  #printf("solve_red_black(reds={reds}, blacks={blacks}, red={red!r}, black={black!r}, good={good})")
  ns = (nr, nb) = (len(reds), len(blacks))
  assert nr - nb in {1, 2}
  if ns == (1, 0):
    printf("{p}[{w}] -> \\")
    x = reds[0]
    printf("{x}{red}" if x != good else IMP)
  elif nr == 2:
    # weigh the two reds
    w += 1
    (r0, r1) = (reds[0], reds[1])
    output_weighing(p, w, [r0], [r1])
    printf("{p}[{w}] A < B -> \\")
    x = (r1 if red == 'H' else r0)
    printf("{x}{red}" if x != good else IMP)
    printf("{p}[{w}] A > B -> \\")
    x = (r0 if red == 'H' else r1)
    printf("{x}{red}" if x != good else IMP)
    printf("{p}[{w}] A = B -> \\")
    printf("{blacks[0]}{black}" if nb == 1 and blacks[0] != good else IMP)
  else:
    # divide the reds into 3 piles
    k = divc(nr, 3)
    (r1, r2, r3) = (reds[:k], reds[k:2*k], reds[2*k:])
    # divide the blacks into 3 corresponding piles
    i = len(r1) - 1
    j = i + len(r2) - 1
    (b1, b2, b3) = (blacks[:i], blacks[i:j], blacks[j:])
    #printf("[{red} {reds} -> {r1}, {r2}, {r3}]")
    #printf("[{black} {blacks} -> {b1}, {b2}, {b3}]")
    w += 1
    output_weighing(p, w, r1 + b1, r2 + b2)
    printf("{p}[{w}] A < B:")
    (rs, bs) = ((r2, b1) if red == 'H' else (r1, b2))
    w1 = solve_red_black(rs, bs, red, black, good, w, p + "  ")
    printf("{p}[{w}] A > B:")
    (rs, bs) = ((r1, b2) if red == 'H' else (r2, b1))
    w2 = solve_red_black(rs, bs, red, black, good, w, p + "  ")
    printf("{p}[{w}] A = B:")
    if len(b3) > len(r3):
      w3 = solve_red_black(b3, r3 , black, red, good, w, p + "  ")
    else:
      # increase the reds with a known good red
      gd = r1[0]
      w3 = solve_red_black([gd] + r3, b3, red, black, gd, w, p + "  ")
    w = max(w1, w2, w3)
  return w

# find suspect coin with extra known good coin
def solve_test_coin(coins, good, w=0, p=''):
  n = len(coins)
  if n < 1:
    printf("{p}-> {IMP}")
  elif n == 1:
    # weigh the coin against the known good coin
    w += 1
    x = coins[0]
    output_weighing(p, w, [good], [x])
    printf("{p}[{w}] A < B -> {x}H")
    printf("{p}[{w}] A > B -> {x}L")
    printf("{p}[{w}] A = B -> {IMP}")
  else:
    # divide the coins into 3 piles
    i = n // 3
    j = 2*i + 1
    (c1, c2, c3) = (coins[:i], coins[i:j], coins[j:])
    #printf("-> {c1} {c2} {c3}")
    w += 1
    output_weighing(p, w, [good] + c1, c2)
    printf("{p}[{w}] A < B:")
    w1 = solve_red_black(c2, c1, 'H', 'L', -1, w, p + "  ")
    printf("{p}[{w}] A > B:")
    w2 = solve_red_black(c2, c1, 'L', 'H', -1, w, p + "  ")
    printf("{p}[{w}] A = B:")
    w3 = solve_test_coin(c3, good, w, p + "  ")
    w = max(w1, w2, w3)
  return w

# find suspect coin
def solve_general(coins, w=0, p=''):
  n = len(coins)
  if n < 3:
    printf("{p}-> {IMP}")
  else:
    # divide the coins into 3 piles
    (c1, c2, c3) = thirds(coins)
    #printf("-> {c1} {c2} {c3}")
    w += 1
    output_weighing(p, w, c1, c2)
    printf("{p}[{w}] A < B:")
    w1 = solve_red_black(c1 + [c3[0]], c2, 'L', 'H', -1, w, p + "  ")
    printf("{p}[{w}] A > B:")
    w2 = solve_red_black(c1 + [c3[0]], c2, 'H', 'L', -1, w, p + "  ")
    printf("{p}[{w}] A = B:")
    w3 = solve_test_coin(c3, c1[0], w, p + "  ")
    w = max(w1, w2, w3)
  return w

# number of coins (or weighings) and problem type
n = arg("n13", 0, prompt="number of coins (n<int>; or weighings w<int>)")
p = arg("1", 1, prompt="problem type (1-4)")
printf("[arg = {n}; problem = {p} (of 1-4)]")

# parse the n parameter
def fn(n, f):
  # n<n> = <n> coins; w<n> = <n> weighings
  if n.startswith('n'): return int(n[1:])
  if n.startswith('w'): return f(int(n[1:]))
  # old style: <n> = n<n>; -<n> = w<n>
  n = int(n)
  return (f(-n) if n < 0 else n)

if p == "1":
  # solve the general case
  n = fn(n, (lambda k: (3**k - 3) // 2))
  printf("---{nl}find suspect coin from {n} coins{nl}---")
  coins = list(irange(1, n))
  printf("coins = {coins}")
  w = solve_general(coins)
  printf("---{nl}{n} coins -> {w} weighings")

if p == "2":
  # solve with a known good coin (0)
  n = fn(n, (lambda k: (3**k - 1) // 2))
  printf("---{nl}find suspect coin from {n} coins, with an extra known good coin (0){nl}---")
  coins = list(irange(1, n))
  printf("coins = {coins}")
  w = solve_test_coin(coins, 0)
  printf("---{nl}{n} coins -> {w} weighings")

if p == "3":
  # solve red/black
  n = fn(n, (lambda k: 3**k))
  r = ((n + 2) // 2 if n > 0 else 0)
  b = n - r
  printf("---{nl}find suspect coin from {n} coins, where {r} coins are red and {b} coins are black{nl}if the suspect coin is red it is heavy, if it is black it is light{nl}---")
  (reds, blacks) = (list(irange(1, r)), list(irange(r + 1, n)))
  printf("reds = {reds}{nl}blacks = {blacks}")
  w = solve_red_black(reds, blacks)
  printf("---{nl}{n} coins -> {w} weighings")

if p == "4":
  # solve lighter
  n = fn(n, (lambda k: 3**k))
  printf("---{nl}find suspect lighter coin from {n} coins{nl}---")
  coins = list(irange(1, n))
  printf("coins = {coins}")
  w = solve_lighter(coins)
  printf("---{nl}{n} coins -> {w} weighings")
