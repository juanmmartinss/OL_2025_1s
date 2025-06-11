import pulp
from pulp import PULP_CBC_CMD

def resolver_regua_golomb(n):

    #Limite superior para o comprimento da régua
    L = n ** 2  
    
    model = pulp.LpProblem("Régua_de_Golomb", pulp.LpMinimize)

    #Variáveis de decisão
    x = pulp.LpVariable.dicts("x", range(1, L + 1), cat="Binary")

    #Variáveis para linearização
    y = {}
    for i in range(1, L):
        for k in range(i + 1, L + 1):
            y[(i, k)] = pulp.LpVariable(f"y_{i}_{k}", cat="Binary")

    
    #Função objetivo: minimizar o comprimento da régua (t)
    t = pulp.LpVariable("t", lowBound=0, cat="Integer")

    model += t

    #Restrição: t >= i * x[i]
    for i in range(1, L + 1):
        model += t >= i * x[i]


    #Restrição: número total de marcas (exceto a 0) deve ser n - 1
    model += pulp.lpSum(x[i] for i in range(1, L + 1)) == n - 1

    #Restrição: distâncias entre marcas devem ser diferentes
    for d in range(1, L):
        model += x.get(d, 0) + pulp.lpSum(y[i, i + d] for i in range(1, L - d + 1)) <= 1

    #Linearização das variáveis y
    for i in range(1, L):
        for k in range(i + 1, L + 1):
            model += x[i] + x[k] - y[i, k] <= 1
            model += y[i, k] <= x[i]
            model += y[i, k] <= x[k]

    model.solve(PULP_CBC_CMD(msg=0))

    if pulp.LpStatus[model.status] == "Optimal":
        comprimento = int(pulp.value(t))
        marcas = [0] + [i for i in range(1, L + 1) if x[i].varValue == 1]
        return comprimento, marcas
    else:
        return None, None

#Loop para rodar para n = 6, 8, 15
for n in [6, 8, 15]:
    print(f"\nResolvendo para n = {n}...")
    comprimento, marcas = resolver_regua_golomb(n)
    if comprimento is not None:
        print(f"Comprimento mínimo da régua: {comprimento}")
        print(f"Marcas encontradas: {marcas}")
    else:
        print("Não encontrou solução ótima.")
