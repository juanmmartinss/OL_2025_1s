import pulp

prob = pulp.LpProblem("Bases_SAMU", pulp.LpMinimize)

x1 = pulp.LpVariable('Local 1', lowBound=0, cat='Continuous')
x2 = pulp.LpVariable('Local 2', lowBound=0, cat='Continuous')
x3 = pulp.LpVariable('Local 3', lowBound=0, cat='Continuous')
x4 = pulp.LpVariable('Local 4', lowBound=0, cat='Continuous')
x5 = pulp.LpVariable('Local 5', lowBound=0, cat='Continuous')

Z = x1 + x2 + x3 + x4 + x5

prob += Z

Sul = x1 + x2
prob += (Sul >= 1)

Central = x1 + x2 + x3 + x4
prob += (Central >= 1)

Sudeste = x2 + x5
prob += (Sudeste >= 1)

Oeste = x3 + x4 + x5
prob += (Oeste >= 1)

Norte = x4 + x5
prob += (Norte >= 1)

optimization_result = prob.solve()
print("Status:", pulp.LpStatus[prob.status])
print("Objective value:", pulp.value(prob.objective))

print("Local 1:", x1.varValue)
print("Local 2:", x2.varValue)
print("Local 3:", x3.varValue)
print("Local 4:", x4.varValue)
print("Local 5:", x5.varValue)