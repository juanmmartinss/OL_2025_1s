import pulp

prob = pulp.LpProblem("Antenas", pulp.LpMaximize)

x1 = pulp.LpVariable('Local A', lowBound=0, cat='Continuous')
x2 = pulp.LpVariable('Local B', lowBound=0, cat='Continuous')
x3 = pulp.LpVariable('Local C', lowBound=0, cat='Continuous')
x4 = pulp.LpVariable('Local D', lowBound=0, cat='Continuous')
x5 = pulp.LpVariable('Local E', lowBound=0, cat='Continuous')

a1 = x3 + x4 + x5
prob += (a1 <= 1)

a2 = x1
prob += (a2 <= 1)

a3 = x2
prob += (a3 <= 1)

a4 = x1 + x2
prob += (a4 <= 1)

a5 = x3 + x5
prob += (a5 <= 1)

a6 = x3 + x4 + x5
prob += (a6 <= 1)

antenaDE = x4 + x5
prob += (antenaDE == 0 or antenaDE == 2)

Z = a1 + a2 + a3 + a4 + a5 + a6

prob += Z

optimization_result = prob.solve()
print("Status:", pulp.LpStatus[prob.status])
print("Objective value:", pulp.value(prob.objective))

print("Local A:", x1.varValue)
print("Local B:", x2.varValue)
print("Local C:", x3.varValue)
print("Local D:", x4.varValue)
print("Local E:", x5.varValue)