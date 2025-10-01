#! python3
# -*- mode: Python; python-indent-offset: 2; coding: utf-8 -*-

from math import (atan2, radians, cos, sin, acos, asin, degrees)
from enigma import (sqrt, fdiv, irange, irangef, static, hypot, identity, arg, printf)
from plot import Plot

n = arg(12, 0, float) # size of box
endl = arg(1, 1, int) # left end
endr = arg(endl, 2, int) # right end
# endl or endr = -1 -> normal packing

# separation of triangular units
r3 = sqrt(3)
sep = 1 + sqrt(4 * r3 - 3)
printf("[sep = {sep}]")

# co-ordinates (x, y) are represented by z = complex(x, y)

# centre of circle touching z1, z2
def touch(z1, z2, i=1):
  z = z2 - z1
  d = abs(z)
  l = 0.5 * d # if the radii are the same
  h = sqrt(4 - l * l)
  t = sorted([
    (z1.real + (l * z.real + h * z.imag) / d, z1.imag + (l * z.imag - h * z.real) / d),
    (z1.real + (l * z.real - h * z.imag) / d, z1.imag + (l * z.imag + h * z.real) / d),
  ])[i]
  return complex(*t)

# circle touching z and the ceiling
def upper(z):
  if z.imag == 3: return horiz(z)
  t = asin(0.5 * (3 - z.imag))
  return complex(z.real + 2 * cos(t), 3)

# circle touching z and the floor
def lower(z):
  if z.imag == 1: return horiz(z)
  t = asin(0.5 * (z.imag - 1))
  return complex(z.real + 2 * cos(t), 1)

# touching z horizontally
horiz = lambda z, k=1: z + 2 * k

# initial circles
(Zd, Zu) = (complex(1 - sep, 1), complex(-1, 3))

# list of points for alternating up/down patterns
def pattern(s):
  # initial circles
  zs = [Zd, Zu]
  # and more circle according to the pattern
  for x in s:
    z = None
    if x == "T":
      z = touch(zs[-2], zs[-1])
    elif x == "L":
      z = lower(zs[-2])
    elif x == "U":
      z = upper(zs[-2])
    elif x == "1":
      z = complex(0, 3 - r3)
    zs.append(z)
  return zs[2:]

patterns = {
  0: "", # d = 0
  1: "1", # d = 1
  2: "LT", # d = 1.9844409958083957
  3: "TTL", # d = 2.9819695331350355 = [0] + sep
  4: "LTTU", # d = 3.9688819916167914
  5: "TTLUT", # d = 4.966410528943431 = [2] + sep
  6: "LTTULT", # d = 5.955198000698861
  7: "TTLUTTL", # d = 6.950851524751827 = [4] + sep
  8: "LTTULTTU", # d = 7.94151400978093
  9: "TTLUTTLUT", # d = 8.937167533833897 = [6] + sep
  10: "LTTULTTULT", # d = 9.92923227673198
  11: "TTLUTTLUTTL", # d = 10.923483542915964 = [8] + sep
  12: "LTTULTTULTTU", # d = 11.916950543683033
  # I haven't found any end units n > 12 that are better than [n - 3] + sep
  13: "TTLUTTLUTTLUT", # d = 12.911201809867016 = [10] + sep
  14: "TTLTTULTTULTTU", # d = 13.905453076051 = [11] + sep
  15: "TTLUTTLUTTLUTTL", # d = 14.898920076818069 = [12] + sep
  16: "TTLTTULTTULTTULT", # d = 15.893171343002052 = [13] + sep
  17: "TTLTLUTULUTTLUTTL", # d = 16.887422609186032 = [14] + sep
  18: "TTLTTULTTULTTULTTU", # d = 17.880889609953105 = [15] + sep
  19: "TTLTLUTULUTTLUTTLUT", # d = 18.875140876137085 = [16] + sep
  20: "TTLTLUTULTLULTTULTTU", # d = 19.869392142321068 = [17] + sep
}

# find the extents of the end units, and indicate excluded ones
ends = dict()
for k in sorted(patterns.keys()):
  zs = pattern(patterns[k])
  d = (max(z.real for z in zs) + 1 if zs else 0)
  s = (' XXX' if k > 2 and not(ends[k - 3][0] + sep - d > 1e-9) else '')
  printf("[end {k}: d = {d}]{s}")
  ends[k] = (d, zs)


# draw the diagram
p = Plot(xscale=32.0, yscale=32.0, xoffset=0.7109375, yoffset=6.8125)

# draw the bounding box
N = 2 * n
p.polygon((0, 0, 0, 4, N, 4, N, 0), fill="white", outline="black")

@static(n=set(), s=set())
def circle(x, y, fill="yellow", outline="black"):
  #fill=None
  if x < 1 or x > N - 1 or y < 1 or y > 3: printf("!!! ESCAPE: ({x}, {y}) !!!")
  p.circle((x, y), 1, fill=fill, outline=outline)
  # check for no overlaps, and record circles by their centre
  ps = list((x1, y1) for (x1, y1) in circle.s if 0.00001 < hypot(x - x1, y - y1) < 1.99999)
  if ps: printf("!!! OVERLAP: ({x}, {y}) -> {ps} !!!")
  circle.s.add((x, y))
  circle.n.add((int(100 * x), int(100 * y)))

# standard packing (n repeats, starting at x0)
def standard(n, x0=0):
  for i in irangef(0, n - 1):
    x = x0 + 2 * i + 1
    circle(x, 1)
    circle(x, 3)

# triangular units (d repeats, starting at x0)
def triangular(d, x0=0):
  for i in irange(0, d - 1):
    x = x0 + i * sep
    if i % 2 == 0:
      circle(x + 1, 1)
      circle(x + sep - 1, 3, fill="cyan")
      if i < d - 1: circle(x + sep, 3 - r3, fill="cyan")
    else:
      circle(x + 1, 3, fill="cyan")
      circle(x + sep - 1, 1)
      if i < d - 1: circle(x + sep, 1 + r3)

# place circles in xys starting at x0, in space xd
def draw(zs, x0, xd, flipx=0, flipy=0):
  fx = (identity if flipx else (lambda x: xd - x))
  fy = (identity if flipy else (lambda y: 4 - y))
  for z in zs:
    circle(x0 + fx(z.real), fy(z.imag), fill="red")

if endl == -1 or endr == -1:
  # standard packing
  printf("[standard]")
  standard(n)

else:
  # ends
  (d1, zs1) = ends[endl]
  (d2, zs2) = ends[endr]
  # left end
  draw(zs1, 0, d1)
  x = d1
  # repeating section
  (u, r) = divmod(2 * n - d1 - d2, sep)
  u = int(u)
  printf("[{endl}+{endr}, {u} units + {r}]")
  triangular(u, d1)
  # right end
  draw(zs2, d1 + u * sep, d2, flipx=1, flipy=(u % 2 == 1))

k = len(circle.n)
a = k - 2 * int(n)
printf("{k} coins [a={a:+d}]")

p.display()
