import sys
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, PULP_CBC_CMD

factories = {}
countries = {}
children = []

def parse_input():
    global factories, countries, children
    lines = sys.stdin.read().strip().splitlines()
    
    factory_lines = lines[1:n+1]
    country_lines = lines[n+1:n+m+1]
    children_lines = lines[n+m+1:n+m+t+1]
    
    # Process factories - use list comprehension for better performance
    for line in factory_lines:
        factory_id, country_id, stock = map(int, line.split())
        factories[factory_id] = {'country': country_id, 'stock': stock}
    
    # Process countries
    for line in country_lines:
        country_id, max_export, min_delivery = map(int, line.split())
        countries[country_id] = {
            'max_export': max_export, 
            'min_delivery': min_delivery, 
            'current_delivery': 0
        }
    
    # Process children - extend is faster than append in a loop
    children.extend(
        {"id": data[0], "country": data[1], "factories": data[2:]}
        for data in (map(int, line.split()) for line in children_lines)
    )
    
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
