import sys
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, PULP_CBC_CMD

def parse_input():
    lines = sys.stdin.read().strip().splitlines()
    n, m, t = map(int, lines[0].split())
    
    factories = {}
    countries = {}
    children = []
    country_children_count = {i: 0 for i in range(1, m + 1)}  # Track how many children per country
    
    # Parse countries first
    for i in range(n + 1, n + m + 1):
        country_id, max_export, min_delivery = map(int, lines[i].split())
        max_export = max(0, max_export)
        min_delivery = max(0, min_delivery)
        countries[country_id] = {
            'max_export': max_export, 
            'min_delivery': min_delivery
        }
    
    # Parse factories and only add them if they are active (stock > 0) and their country is active (max_export > 0)
    for i in range(1, n + 1):
        factory_id, country_id, stock = map(int, lines[i].split())
        if stock > 0 and countries[country_id]["max_export"] > 0:  # Only active factories
            factories[factory_id] = {'country': country_id, 'stock': stock}
    
    # Parse children and filter out factories that don't exist
    for i in range(n + m + 1, n + m + t + 1):
        data = list(map(int, lines[i].split()))
        child_id = data[0]
        country_id = data[1]
        valid_factories = [f for f in data[2:] if f in factories]  # Only consider valid factories
        
        # If child has valid factories, add to children list
        if valid_factories:
            children.append({"id": child_id, "country": country_id, "factories": valid_factories})
            country_children_count[country_id] += 1  # Count child for country
    
    return n, m, t, factories, countries, children, country_children_count


def solve_lp():
    n, m, t, factories, countries, children, country_children_count = parse_input()
    
    # Handle edge cases first
    if n == 0:  # No factories
        return -1
    if t == 0:  # No children
        return 0
    
    # Create problem
    prob = LpProblem("MerryHanukkah", LpMaximize)
    
    # Decision variables
    x = {}
    for child in children:
        for factory_id in child["factories"]:
            if factory_id in factories:  # Only create variables for valid factories
                x[f"{child['id']}_{factory_id}"] = LpVariable(
                    f"x_{child['id']}_{factory_id}", 
                    cat="Binary"
                )
    
    # Objective: Maximize satisfied children
    prob += lpSum(lpSum(x.get(f"{child['id']}_{factory_id}", 0)
                       for factory_id in child["factories"]
                       if factory_id in factories)
                  for child in children)
    
    # Factory stock constraints
    for factory_id, factory in factories.items():
        prob += lpSum(x.get(f"{child['id']}_{factory_id}", 0)
                     for child in children
                     if factory_id in child["factories"]) <= factory["stock"]
    
    # One toy per child
    for child in children:
        prob += lpSum(x.get(f"{child['id']}_{factory_id}", 0)
                     for factory_id in child["factories"]
                     if factory_id in factories) <= 1
    
    # Country export constraints
    for country_id in countries:
        prob += lpSum(x.get(f"{child['id']}_{factory_id}", 0)
                     for child in children
                     for factory_id in child["factories"]
                     if factory_id in factories and factories[factory_id]["country"] == country_id
                     ) <= countries[country_id]["max_export"]
    
    # Minimum delivery constraints
    for country_id, country in countries.items():
        prob += lpSum(lpSum(x.get(f"{child['id']}_{factory_id}", 0)
                           for factory_id in child["factories"]
                           if factory_id in factories)
                     for child in children
                     if child["country"] == country_id) >= country["min_delivery"]
    
    # Solve with tighter tolerances
    solver = PULP_CBC_CMD(msg=False)
    status = prob.solve(solver)
    
    if status != 1:  # Not optimal
        return -1
        
    objective_value = int(round(prob.objective.value()))
    return max(0, objective_value)  # Ensure we never return negative values

if __name__ == "__main__":
    result = solve_lp()
    print(result)