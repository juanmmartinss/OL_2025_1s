"""
EcoRecipiente – modelo de planejamento de produção, transporte e estoque
-----------------------------------------------------------------------
Requisitos:
    pip install pulp     # resolvedor linear open-source CBC

Convém rodar com Python 3.8+.
"""

import pulp as pl

# ── 1. Conjuntos ─────────────────────────────────────────
plants   = [1, 2, 3, 4, 5]
quarters = [1, 2, 3, 4]
types    = [35, 42]

# ── 2. Parâmetros ────────────────────────────────────────
# 2.1 Demanda (Tabela 1) – valores em unidades de 100 000 recipientes
D = {
    # tipo 35
    (1, 35, 1): 138, (1, 35, 2): 142, (1, 35, 3): 139, (1, 35, 4): 140,
    (2, 35, 1):  82, (2, 35, 2):  84, (2, 35, 3):  83, (2, 35, 4):  84,
    (3, 35, 1):  32, (3, 35, 2):  33, (3, 35, 3):  34, (3, 35, 4):  36,
    (4, 35, 1):  61, (4, 35, 2):  66, (4, 35, 3):  67, (4, 35, 4):  75,
    # tipo 42
    (1, 42, 1):  284, (1, 42, 2):  278, (1, 42, 3):  305, (1, 42, 4):  322,
    (2, 42, 1):  226, (2, 42, 2):  255, (2, 42, 3):  272, (2, 42, 4):  289,
    (3, 42, 1):  141, (3, 42, 2):  160, (3, 42, 3):  175, (3, 42, 4):  188,
    (4, 42, 1):  134, (4, 42, 2):  116, (4, 42, 3):  126, (4, 42, 4):  130,
    (5, 42, 1): 1168, (5, 42, 2): 1138, (5, 42, 3): 1204, (5, 42, 4): 1206,
}

# 2.2 Máquinas (Tabela 2)
# id, planta, tipo, custo produção, dias-máquina por unidade
M = [
    ("D5_35", 1, 35, 760, 0.097),
    ("D5_42", 1, 42, 454, 0.037),
    ("D6_35", 1, 35, 879, 0.103),
    ("D6_42", 1, 42, 476, 0.061),
    ("C4_35", 1, 35, 733, 0.080),
    ("C4_42", 1, 42, 529, 0.068),

    ("T_42",  2, 42, 520, 0.043),
    ("U2_35", 2, 35, 790, 0.109),
    ("U2_42", 2, 42, 668, 0.056),
    ("K4_35", 2, 35, 758, 0.119),

    ("K4_42", 3, 42, 509, 0.061),
    ("J6_35", 3, 35, 799, 0.119),
    ("J6_42", 3, 42, 521, 0.056),
    ("T0_35", 3, 35, 888, 0.140),  # máquina “70” renomeada p/ identificador válido
    ("T0_42", 3, 42, 625, 0.093),

    ("I_35", 4, 35, 933, 0.113),
    ("I_42", 4, 42, 538, 0.061),

    ("V1_42", 5, 42, 503, 0.061),
]

# 2.3 Disponibilidade de dias de operação (Tabela 3)
A = {
    "C4": {1: 88, 2: 89, 3: 89, 4: 88},
    "D5": {1: 88, 2: 89, 3: 89, 4: 88},
    "D6": {1: 72, 2: 63, 3: 58, 4: 65},
    "U2": {1: 81, 2: 88, 3: 87, 4: 55},
    "T" : {1: 88, 2: 75, 3: 89, 4: 88},
    "K4": {1: 88, 2: 89, 3: 89, 4: 88},
    "J6": {1: 37, 2: 89, 3: 39, 4: 86},
    "T0": {1: 54, 2: 84, 3: 85, 4: 73},
    "I" : {1: 42, 2: 71, 3: 70, 4: 68},
    "V1": {1: 88, 2: 89, 3: 89, 4: 88},
}

# 2.4 Custos de transporte (Tabela 4) – $ por unidade
c_trans = {
    (1, 2): 226, (1, 3): 274, (1, 4):  93, (1, 5): 357,
    (2, 1): 226, (2, 3): 371, (2, 4): 310, (2, 5): 443,
    (3, 1): 274, (3, 2): 371, (3, 4): 227, (3, 5): 168,
    (4, 1):  93, (4, 2): 310, (4, 3): 227, (4, 5): 715,
    (5, 1): 357, (5, 2): 443, (5, 3): 168, (5, 4): 715,
}

# 2.5 Capacidade de estoque (Tabela 5) – unidades de 100 000 recipientes
Smax = {
    (1, 1): 376, (1, 2): 325, (1, 3): 348, (1, 4): 410,
    (2, 1):  55, (2, 2):  47, (2, 3):  62, (2, 4):  58,
    (3, 1): 875, (3, 2): 642, (3, 3): 573, (3, 4): 813,
    (4, 1):  10, (4, 2):  15, (4, 3):  30, (4, 4):  24,
    (5, 1): 103, (5, 2): 103, (5, 3):  30, (5, 4): 410,
}

# 2.6 Custos de manuseio (Tabela 6)
c_hand = {
    (1, 35): 85, (1, 42): 70,
    (2, 35): 98, (2, 42): 98,
    (3, 35): 75, (3, 42): 75,
    (4, 35): 90, (4, 42): 80,
    # planta 5 só produz/estoca tipo 42
    (5, 42): 67,
}

# ── 3. Modelo PuLP ───────────────────────────────────────
mdl = pl.LpProblem("EcoRecipiente", pl.LpMinimize)

# 3.1 Variáveis de decisão
x = pl.LpVariable.dicts(
        name="Prod",
        indices=[(m, q) for m, *_ in M for q in quarters],
        lowBound=0
    )

y = pl.LpVariable.dicts(
        name="Ship",
        indices=[(i, j, t, q) for i in plants for j in plants if i != j
                for t in types for q in quarters
                if not (t == 35 and 5 in (i, j))],  # regra: tipo 35 não passa na planta 5
        lowBound=0
    )

I = pl.LpVariable.dicts(
        name="Inv",
        indices=[(p, t, q) for p in plants for t in types for q in range(0, 5)],
        lowBound=0
    )

# 3.2 Funções auxiliares
def prod_ptq(p, t, q):
    """Produção total da planta p, tipo t, trimestre q."""
    return pl.lpSum(
        x[(m, q)]
        for (m, plnt, tp, _, _) in M
        if plnt == p and tp == t
    )

# 3.3 Restrições
# 3.3.1 Inventário inicial zero
for p in plants:
    for t in types:
        mdl += I[(p, t, 0)] == 0, f"IniInv_{p}_{t}"

# 3.3.2 Balanço de fluxo
for p in plants:
    for t in types:
        for q in quarters:
            inflow = prod_ptq(p, t, q) + pl.lpSum(
                y[(i, p, t, q)] for i in plants if i != p and (i, p, t, q) in y
            )
            outflow = pl.lpSum(
                y[(p, j, t, q)] for j in plants if j != p and (p, j, t, q) in y
            )
            mdl += (
                I[(p, t, q-1)] + inflow - D.get((p, t, q), 0) - outflow
                == I[(p, t, q)]
            ), f"Balance_{p}_{t}_{q}"

# 3.3.3 Capacidade de estoque
for p in plants:
    for q in quarters:
        mdl += (
            pl.lpSum(I[(p, t, q)] for t in types) <= Smax[(p, q)]
        ), f"Storage_{p}_{q}"

# 3.3.4 Disponibilidade de dias de máquina
for (m, p, tp, _, days_per_unit) in M:
    base = m.split('_')[0]   # D5_35 → D5,  T0_42 → T0
    for q in quarters:
        mdl += (
            days_per_unit * x[(m, q)] <= A[base][q]
        ), f"Days_{m}_{q}"

# 3.4 Função-objetivo
Z_prod = pl.lpSum(
    cost * x[(m, q)]
    for (m, _, _, cost, _) in M
    for q in quarters
)

Z_ship = pl.lpSum(
    c_trans[(i, j)] * y[(i, j, t, q)]
    for (i, j, t, q) in y
)

Z_inv = pl.lpSum(
    c_hand.get((p, t), 0) * I[(p, t, q)]
    for (p, t, q) in I if q > 0   # ignora trimestre 0
)

mdl += Z_prod + Z_ship + Z_inv, "TotalCost"

# ── 4. Resolução ─────────────────────────────────────────
solver = pl.PULP_CBC_CMD(msg=1)   # msg=0 se não quiser logs
status = mdl.solve(solver)

# ── 5. Resultados ────────────────────────────────────────
print("\nStatus:", pl.LpStatus[status])
print("Custo total mínimo: ${:,.2f}".format(pl.value(mdl.objective)))

print("\nProdução por máquina (apenas >0):")
for (m, q), var in x.items():
    if var.value() > 1e-6:
        print(f"  {m:<6s}  Trim {q}: {var.value():.2f}")

print("\nInventário final (Trim 4, apenas >0):")
for p in plants:
    for t in types:
        inv_final = I[(p, t, 4)].value()
        if inv_final > 1e-6:
            print(f"  Planta {p}, Tipo {t}: {inv_final:.2f}")
