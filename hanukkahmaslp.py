import sys
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, PULP_CBC_CMD

factories = {}
countries = {}
children = []

def parse_input():
    global factories, countries, children
    lines = sys.stdin.read().strip().splitlines()
    
    n, m, t = map(int, lines[0].split())
    
    for i in range(1, n + 1):
        factory_id, country_id, stock = map(int, lines[i].split())
        factories[factory_id] = {'country': country_id, 'stock': stock}
    
    for i in range(n + 1, n + m + 1):
        country_id, max_export, min_delivery = map(int, lines[i].split())
        countries[country_id] = {'max_export': max_export, 'min_delivery': min_delivery, 'current_delivery': 0}
    
    for i in range(n + m + 1, n + m + t + 1):
        data = list(map(int, lines[i].split()))
        child_id = data[0]
        country_id = data[1]
        factories_list = data[2:]
        children.append({"id": child_id, "country": country_id, "factories": factories_list})
    
    return n, m, t

def solve_lp():
    prob = LpProblem("MerryHanukkah", LpMaximize)
    
    x = {}
    for child in children:
        for factory in child["factories"]:
            x[(child["id"], factory)] = LpVariable(f"x_{child['id']}_{factory}", cat="Binary")

    prob += lpSum(x[(child["id"], factory)] for child in children for factory in child["factories"])
    
    for factory_id, factory in factories.items():
        prob += lpSum(x[(child["id"], factory_id)] for child in children if factory_id in child["factories"]) <= factory["stock"], f"Factory_{factory_id}_stock"
    
    for country_id, country in countries.items():
        prob += lpSum(x[(child["id"], factory_id)] 
                  for child in children 
                  for factory_id in child["factories"]
                  if factories[factory_id]["country"] == country_id 
                  and factory_id in factories) <= country["max_export"]
        
    for country_id, country in countries.items():
        prob += lpSum(x[(child["id"], factory_id)] for child in children if child["country"] == country_id for factory_id in child["factories"]) >= country["min_delivery"], f"Country_{country_id}_min_delivery"
    
    for child in children:
        prob += lpSum(x[(child["id"], factory_id)] for factory_id in child["factories"]) <= 1
    
    solver = PULP_CBC_CMD(msg=False)
    prob.solve(solver)
    
    if prob.status == 1: 
        return int(prob.objective.value())
    else:
        return -1

if __name__ == "__main__":
    import sys
    n, m, t = parse_input()
    
    if n == 0:
        print(-1)

    elif t == 0:
        print(0)

    else:
        result = solve_lp()
        print(result)
