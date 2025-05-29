# ---------------------------------------------------------------
#  Problema da Galeria de Arte — colocação mínima de câmeras
#  Modelo:   x_v  = 1 se põe câmera no vértice  v
#            y_e  = 1 se põe câmera na aresta   e
#  Restrição: para cada aresta (u,v)  →  x_u + x_v + y_(u,v) ≥ 1
#  Objetivo:  minimizar  Σ x_v + Σ y_e
# ---------------------------------------------------------------

from itertools import combinations
import sys

V = [1, 2, 3, 4, 5, 6, 7, 8]   
E = [(1, 2), (1, 4), (2, 3), (2, 6), (3, 5),
     (4, 6), (5, 6), (6, 7), (7, 8), (4, 8)]

try:
    from pulp import (LpProblem, LpVariable, LpBinary,
                      LpMinimize, lpSum, value, PULP_CBC_CMD)

    prob = LpProblem("Art_Gallery", LpMinimize)


    x = LpVariable.dicts("x", V, cat=LpBinary)                
    y = LpVariable.dicts("y", E, cat=LpBinary)               

    # função-objetivo
    prob += lpSum(x[v] for v in V) + lpSum(y[e] for e in E)

    for (u, v) in E:
        prob += x[u] + x[v] + y[(u, v)] >= 1, f"cover_{u}_{v}"

    status = prob.solve(PULP_CBC_CMD(msg=False))
    if status != 1:                       
        raise RuntimeError("Solver nao encontrou solucao otima.")

    sel_nodes  = [v for v in V       if value(x[v]) > 0.5]
    sel_edges  = [e for e in E       if value(y[e]) > 0.5]
    num_cam    = len(sel_nodes) + len(sel_edges)

    print(f"\nSolução ótima com {num_cam} camera(s)")
    print("Cameras nos vertices :", sel_nodes or "nenhuma")
    print("Cameras nas arestas  :", sel_edges or "nenhuma")
