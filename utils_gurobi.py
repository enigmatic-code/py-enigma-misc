#! python3
# -*- mode: Python; python-indent-offset: 2; -*-

from __future__ import print_function

import gurobipy as gp
from gurobipy import GRB

def hitting_set(ss, verbose=0):
  # find elements in the universe
  vs = sorted(set().union(*ss))
  if not vs: return set()

  # map elements to indices (0-indexed)
  m = dict((v, j) for (j, v) in enumerate(vs))
  # map the sets to sets of indices
  jss = set(frozenset(m[v] for v in s) for s in ss)
  # can't hit the empty set
  if not all(jss): return None

  # construct the model
  model = gp.Model()
  if verbose:
    model.setParam(GRB.Param.DisplayInterval, 60) # 60s log interval
  else:
    model.setParam(GRB.Param.OutputFlag, 0) # disable output
  model.setParam(GRB.Param.Presolve, 2) # aggressive presolve
  model.setParam(GRB.Param.MIPFocus, 2) # focus on optimal solution
  #model.setParam(GRB.Param.Symmetry, 1)

  # decision variables: x[j] = 1 if element j is in the hitting set
  xs = list(
    model.addVar(vtype=GRB.BINARY, name="x" + str(j))
      for j in range(len(vs))
  )

  # each set must be hit
  for js in jss:
    model.addConstr(sum(xs[j] for j in js) >= 1)

  # objective: minimise the size of the hitting set
  model.setObjective(sum(xs), GRB.MINIMIZE)

  # solve the model
  model.optimize()

  # return elements in the hitting set
  return set(vs[j] for (j, x) in enumerate(xs) if x.X)

# for convenience, will only produce one hitting set
def hitting_sets(ss, verbose=0):
  yield hitting_set(ss, verbose=verbose)

if __name__ == "__main__":
  ss = [{1, 2, 3}, {2, 4}, {3, 4}, {4, 5}]
  hs = hitting_set(ss)
  print(hs)
