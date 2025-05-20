#!/usr/bin/env python3
# ---------------------------------------------------------------
#  Problema da Galeria de Arte — colocação mínima de câmeras
#  Modelo:   x_v  = 1 se põe câmera no vértice  v
#            y_e  = 1 se põe câmera na aresta   e
#  Restrição: para cada aresta (u,v)  →  x_u + x_v + y_(u,v) ≥ 1
#  Objetivo:  minimizar  Σ x_v + Σ y_e
# ---------------------------------------------------------------

from itertools import combinations
import sys

# ---------- 1.  Definição do grafo ----------
V = [1, 2, 3, 4, 5, 6, 7, 8]                    # vértices (cantos)
E = [(1, 2), (1, 4), (2, 3), (2, 6), (3, 5),   # arestas (corredores)
     (4, 6), (5, 6), (6, 7), (7, 8), (4, 8)]

# ---------- 2.  Tentamos usar PuLP ----------
try:
    from pulp import (LpProblem, LpVariable, LpBinary,
                      LpMinimize, lpSum, value, PULP_CBC_CMD)

    prob = LpProblem("Art_Gallery", LpMinimize)

    # variáveis binárias
    x = LpVariable.dicts("x", V, cat=LpBinary)                   # câmeras em vértices
    y = LpVariable.dicts("y", E, cat=LpBinary)                   # câmeras em arestas

    # função-objetivo
    prob += lpSum(x[v] for v in V) + lpSum(y[e] for e in E)

    # restrições de cobertura
    for (u, v) in E:
        prob += x[u] + x[v] + y[(u, v)] >= 1, f"cover_{u}_{v}"

    # resolução
    status = prob.solve(PULP_CBC_CMD(msg=False))
    if status != 1:                       # 1 = “Optimal” no PuLP
        raise RuntimeError("Solver não encontrou solução ótima.")

    sel_nodes  = [v for v in V       if value(x[v]) > 0.5]
    sel_edges  = [e for e in E       if value(y[e]) > 0.5]
    num_cam    = len(sel_nodes) + len(sel_edges)

    print(f"\n► Solução ótima com {num_cam} câmera(s)")
    print("  – Câmeras nos vértices :", sel_nodes or "nenhuma")
    print("  – Câmeras nas arestas  :", sel_edges or "nenhuma")

except ModuleNotFoundError:
    # ---------- 3.  fallback brute-force (dispensa bibliotecas) ----------
    print("Pacote 'pulp' não encontrado — usando busca exaustiva "
          "(ok para grafos pequenos).", file=sys.stderr)

    universe = list(range(len(V) + len(E)))      # índices de itens possíveis
    best = None

    for k in range(1, len(universe) + 1):
        for combo in combinations(universe, k):
            chosen_nodes = {V[i]            for i in combo if i < len(V)}
            chosen_edges = {E[i - len(V)]   for i in combo if i >= len(V)}
            if all( (e in chosen_edges) or
                    (e[0] in chosen_nodes) or
                    (e[1] in chosen_nodes) for e in E):
                best = (k, chosen_nodes, chosen_edges)
                break
        if best:
            break

    k, chosen_nodes, chosen_edges = best
    print(f"\n► Solução ótima com {k} câmera(s)")
    print("  – Câmeras nos vértices :", sorted(chosen_nodes) or "nenhuma")
    print("  – Câmeras nas arestas  :", sorted(chosen_edges) or "nenhuma")