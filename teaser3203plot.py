#! python3

from math import (sin, cos, tan, radians, pi, sqrt)
from enigma import (P2, join, sq, fdiv, polygon_area, arg, printf)
from plot import Plot

tris = circs = rects = ()

v = arg(3, 0, int)

r3 = sqrt(3)
x = 5 * sqrt(2) * (r3 - 1)
ngon_area = lambda n, a=1: fdiv(n * sq(a), 4 * tan(fdiv(pi, n)))

# area used by the towers
V = 2 * pi * sq(9.5)

if v == 1:
  A = 0.25 * (28 + 23) * 5 * r3 * sq(x)
  printf("[{v}] trapezium circuit [A = {A:.2f}, X = {X:.2f}]", X=A - V)
  # (isosceles) trapezium circuit [110.42 sq units enclosed]
  tris = join([
    "LRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRL", # 28 straight
    "RRRRR", # 5 turn
    "LRLRLRLRL", # 5 straight
    "RRR", # 3 turn
    "LRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRL", # 23 straight
    "RRR", # 3 turn
    "LRLRLRLRL", # 5 straight
    "RRRRR", # 5 turn
  ])
  circs = [(3.40, 3.15, 1.9), (25.10, 3.15, 1.9)]
  rects = [(-0.26, -0.95, 28, 1.9)]

if v == 2:
  A = 2 * (ngon_area(12, x) + ngon_area(3, x))
  # nicer solution [21.19 sq units enclosed]
  printf("[{v}] dumbbell circuit [A = {A:.2f}, X = {X:.2f}]", X=A - V)
  tris = join([
    "LRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRL", # 29 straight
    "LL",
    "RRLRRLRRLRRLRRLRRLRRLRRLRRLRR", # turn
    "LL",
    "LRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRL", # 29 straight
    "LL",
    "RRLRRLRRLRRLRRLRRLRRLRRLRRLRR", # turn
    "LL",
  ])
  circs = [(-3.09, 0.97, 1.9), (32.59, 0.97, 1.9)]
  rects = [(0.26, -0.95, 28, 1.9)]

if v == 3:
  # alternative solution
  printf("[{v}] modified dumbbell circuit")
  tris = join([
    "LRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRL", # 28 straight
    "RRLRRLRRLRRLRRLRRLRRLRRLRLRLL", # turn
    "LRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRLRL", # 28 straight
    "RRLRRLRRLRRLRRLRRLRRLRRLRLRLL", # turn
  ])
  circs = [(-4.12, -0.83, 1.9), (28.20, 2.90, 1.9)]
  rects = [(0.26, -0.95, 28, 1.9)]

###############################################################################

p = Plot(xscale=16.0, yscale=16.0, xoffset=3.2734375, yoffset=15.875)

(z, d) = (P2(0, 0), 15)
b = sqrt(6) - sqrt(2)

for (x, y, w, h) in rects:
  p.polygon((x, y, x + w, y, x + w, y + h, x, y + h), fill="lightgrey")

pt = lambda z, r, d: P2(z.x + r * cos(radians(d)), z.y + r * sin(radians(d)))

vs = list()
for t in tris:
  if t == 'L':
    A = pt(z, 1, d - 90)
    B = pt(z, 1, d + 90)
    C = pt(A, 2, d + 60)
    p.line(A + B + C + A)
    vs.append(B)
    z = pt(A, 1, d + 60)
    d -= 30
  elif t == 'R':
    A = pt(z, 1, d + 90)
    B = pt(z, 1, d - 90)
    C = pt(A, 2, d - 60)
    p.line(A + B + C + A)
    z = pt(A, 1, d - 60)
    d += 30

for (x, y, r) in circs:
  p.circle((x, y), r, outline="green", fill="green")

A = polygon_area(vs) * sq(5)  # 1 unit = 5 m
printf("poly internal area = {A:.2f} [X = {X:.2f}]", X=A - V)

printf("{n} triangles", n=len(tris))
printf("-> {tris!r}")

p.display()
