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
    
    # Create variables only for valid factory-child combinations
    x = {}
    for child in children:
        for factory in child["factories"]:
            if factory in factories:  # Verify factory exists
                x[(child["id"], factory)] = LpVariable(f"x_{child['id']}_{factory}", cat="Binary")
    
    # Objective: maximize satisfied children
    prob += lpSum(x[(child["id"], factory)] 
                for child in children 
                for factory in child["factories"] 
                if (child["id"], factory) in x)
    
    # Factory stock constraints
    for factory_id, factory in factories.items():
        prob += lpSum(x[(child["id"], factory_id)] 
                    for child in children 
                    if (child["id"], factory_id) in x) <= factory["stock"]
    
    # Country export constraints
    for country_id, country in countries.items():
        prob += lpSum(x[(child["id"], factory_id)]
                    for child in children
                    for factory_id in child["factories"]
                    if factories.get(factory_id, {}).get('country') == country_id
                    and (child["id"], factory_id) in x) <= country["max_export"]
        
    # Country minimum delivery constraints
    for country_id, country in countries.items():
        prob += lpSum(x[(child["id"], factory_id)]
                    for child in children
                    if child["country"] == country_id
                    for factory_id in child["factories"]
                    if (child["id"], factory_id) in x) >= country["min_delivery"]
    
    # One toy per child at most
    for child in children:
        prob += lpSum(x[(child["id"], factory_id)]
                    for factory_id in child["factories"]
                    if (child["id"], factory_id) in x) <= 1
    
    # Solve with CBC solver, suppressing output
    solver = PULP_CBC_CMD(msg=False)
    prob.solve(solver)
    
    # Return result
    if prob.status == 1:
        return int(prob.objective.value())
    return -1

if __name__ == "__main__":
    n, m, t = parse_input()
    
    if n == 0:
        print(-1)

    elif t == 0:
        print(0)

    else:
        result = solve_lp()
        print(result)
