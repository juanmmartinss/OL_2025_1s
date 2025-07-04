#!/usr/bin/env python3
"""
---------------------------------------------------------------
Problema 1.4 – Fábrica de Bobinas de Papel
---------------------------------------------------------------
"""

import sys
from pulp import (
        LpProblem, LpVariable, LpInteger,
        LpMinimize, lpSum, value, PULP_CBC_CMD
    )

TYPES = 5
PATTERNS = [
    (5, 0, 0, 0, 0),   # 1
    (2, 0, 0, 1, 0),   # 2
    (1, 1, 0, 0, 1),   # 3
    (0, 2, 2, 0, 0),   # 4
    (0, 0, 1, 1, 0),   # 5
    (0, 0, 0, 0, 1),   # 6
    (0, 3, 0, 0, 0),   # 7
    (0, 1, 0, 1, 0),   # 8
    (0, 0, 1, 0, 0),   # 9
    (1, 0, 0, 1, 0)    # 10
]

DEMAND = (18, 31, 25, 15, 14)      

def solve_cutting_stock(exact=True):
    """
    Resolve o modelo:
        exact = True   →  restrições com '='   (sem estoque)
        exact = False  →  restrições com '≥'  (com estoque)
    Retorna (status, total_mestre, lista_x_padroes, producao_final)
    """
    tag = "NO_STOCK" if exact else "WITH_STOCK"
    prob = LpProblem(f"CuttingStock_{tag}", LpMinimize)

    x = {
        j: LpVariable(f"x_{j+1}", lowBound=0, cat=LpInteger)
        for j in range(len(PATTERNS))
    }

    # objetivo: minimizar bobinas-mestre
    prob += lpSum(x[j] for j in x), "Minimize_master_rolls"

    # restrições de demanda por tipo
    for i in range(TYPES):
        coef = [PATTERNS[j][i] for j in range(len(PATTERNS))]
        if exact:    
            prob += lpSum(coef[j] * x[j] for j in range(len(PATTERNS))) == DEMAND[i], \
                    f"demand_type_{i+1}"
        else:         
            prob += lpSum(coef[j] * x[j] for j in range(len(PATTERNS))) >= DEMAND[i], \
                    f"demand_type_{i+1}"

    status = prob.solve(PULP_CBC_CMD(msg=False))

    qty_patterns = [int(value(x[j])) for j in range(len(PATTERNS))]
    total_master = sum(qty_patterns)

    # produção resultante
    produced = [0]*TYPES
    for j, q in enumerate(qty_patterns):
        for i in range(TYPES):
            produced[i] += PATTERNS[j][i] * q

    return status, total_master, qty_patterns, produced

def pretty_print(title, res):
    status, n_master, qty, produced = res
    print("\n", "="*10, title, "="*10)
    if status != 1:            
        print("Problema INVIÁVEL (status =", status, ")")
        return
    print(f"Bobinas-mestre usadas : {n_master}")
    print("Padrões escolhidos    :")
    for j, q in enumerate(qty, start=1):
        if q:
            print(f"Padrão {j:2d}  →  {q}")
    print("Produção final        :", produced)
    print("Demanda               :", list(DEMAND))
    exced = [produced[i] - DEMAND[i] for i in range(TYPES)]
    print("Excedente (+) / Falta (-):", exced)
    print("="*38)

def main():
    res1 = solve_cutting_stock(exact=True)
    pretty_print("VARIANTE 1  (demanda exata)", res1)

    res2 = solve_cutting_stock(exact=False)
    pretty_print("VARIANTE 2  (pode estocar)", res2)


if __name__ == "__main__":
    main()
