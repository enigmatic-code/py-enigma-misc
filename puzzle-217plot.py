#! python3
# -*- mode: Python; python-indent-offset: 2; coding: utf-8 -*-

from math import (sin, cos)
from enigma import (irange, fdiv, two_pi, hypot, find_max, call, printf)
from plot import Plot

p = Plot(xscale=1.5, yscale=1.5, xoffset=269, yoffset=99)

R = 100.0  # radius of the moat
Nq = 0.25  # size of N's steps
Mq = Nq * 4.0  # size of M's steps

# draw the moat
p.circle((0, 0), R, fill="white", outline="blue", width=2)

# normalise an angle in the interval [0, two_pi]
def normalise(a):
  while a < 0: a += two_pi
  while a > two_pi: a -= two_pi
  return a

# difference between two angles
def diff(a, b):
  (a, b) = (normalise(a), normalise(b))
  return min(normalise(a - b), normalise(b - a))

# polar to cartesian coordinates
cart = lambda t, r=R, dx=0, dy=0: (R * cos(t) + dx, R * sin(t) + dy)

# move M
def moveM(M, Nx, Ny):
  # M moves one way or the other around the circle
  # go which ever way brings you closer to N
  t = fdiv(Mq, R)
  Ms = [normalise(M + t), normalise(M - t)]
  return min(Ms, key=(lambda t: call(hypot, cart(t, R, -Nx, -Ny))))

# move N
def moveN(Nx, Ny, M):
  # for angle t calculate the advantage N has in reaching that point on the moat before M
  def f(t):
    # calculate N's steps
    Ns = fdiv(call(hypot, cart(t, R, -Nx, -Ny)), Nq)
    # calculate M's steps
    Ms = fdiv(R * diff(M, t), Mq)
    # return the advantage
    return Ms - Ns

  # find the point with the maximum advantage
  r = find_max(f, 0, two_pi)
  # make 1 step towards the optimal point on the moat
  (dx, dy) = cart(r.v, R, -Nx, -Ny)
  f = fdiv(Nq, hypot(dx, dy))
  return (Nx + f * dx, Ny + f * dy)


# starting positions (N = (x, y), M = angle)
(Nx, Ny) = (0, 0)
M = 0
r = 0.7  # radius of points

# plot the starting positions
p.circle((Nx, Ny), 3 * r, fill="green", outline="green")
p.circle(cart(M), 3 * r, fill="red", outline="red")

# limit the total number of steps
for _ in irange(10000):
  # plot M's position
  (Mx, My) = cart(M)
  p.circle((Mx, My), r, fill="red", outline="red")

  # move N, and plot N's new position
  (Nx, Ny) = moveN(Nx, Ny, M)
  p.circle((Nx, Ny), r, fill="green", outline="green")

  # move M, and check for a collision
  M = moveM(M, Nx, Ny)
  d = hypot(Mx - Nx, My - Ny)
  if not (d > Mq):
    printf("N caught")
    break

  if not (hypot(Nx, Ny) < R):
    printf("N escapes [by {d}]")
    break

p.display()
