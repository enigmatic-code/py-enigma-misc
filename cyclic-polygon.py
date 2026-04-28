#! python3
# -*- mode: Python; python-indent-offset: 2; coding: utf-8 -*-

from __future__ import print_function

# plot a cyclic polygon (from the angles made at the centre)

from math import (radians, sin, cos)
from enigma import (
  flatten, tuples, chunk, point_dist, line_param, line_bisect, line_intersect,
  args, seq2str, sprintf, printf
)
from plot import Plot

def fmt(xs, f):
  s = sprintf("{{x:{f}}}")
  return seq2str(sprintf(s) for x in xs)

angles = args([26, 58, 154, 122], 0, float)
printf("angles = {angles}; sum = {t:.2f}", angles=fmt(angles, ".2f"), t=sum(angles))

R = 1

# calculate locations of the vertices
((x, y), t) = ((R, 0), 0)
pts = [(x, y)]
for a in angles:
  t += a
  r = radians(t)
  (x, y) = (R * cos(r), R * sin(r))
  pts.append((x, y))

vs = []
if 1:
  # determine tangent lines at the vertices
  pbs = list(line_bisect((0, 0), line_param((0, 0), p1)(2)) for p1 in pts)
  vs = list(line_intersect(p1, p2, p3, p4).pt for ((p1, p2), (p3, p4)) in tuples(pbs, 2))

def output_sides(pts, t=''):
  # output side lengths
  ds = list(point_dist(p1, p2) for (p1, p2) in tuples(pts))
  delta = sum(a - b for (a, b) in chunk(ds, 2, pad=1, value=0))
  # delta = 0 => the quad is tangential (i.e. has an incircle)
  if t: t += ' '
  msg = ("[0 <-> tangential]" if len(ds) == 4 else "[0 <- tangential]")
  printf("{t}sides = {ds}; delta = {delta:.4f} {msg}", ds=fmt(ds, ".4f"))

p = Plot(width=600, height=600, xscale=256.0, yscale=256.0, xoffset=1.125, yoffset=1.09375)

# plot the inner (contact) polygon [tag = 2]
# this is a cyclic polygon inscribed in a circle
p.line(flatten(pts), colour="black", tag=2)
output_sides(pts, "inner")

# the outer polygon [tag = 3]
# this is a tangential polygon with the circle inscribed in it
if vs:
  vs.append(vs[0])
  p.line(flatten(vs), colour="red", tag=3)
  output_sides(vs, "outer")

# the circle (= incircle of the outer polygon; = circumcircle of inner polygon) [tag = 1]
p.circle((0, 0), R, fill=None, width=1, tag=1)

# points (inner polygon and circumcentre) [tag = 4]
for pt in pts + [(0, 0)]:
  p.circle(pt, 0.01, fill="black", tag=4)

p.display()
